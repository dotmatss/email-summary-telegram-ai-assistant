from __future__ import annotations

import json
import os
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

import httpx
import streamlit as st

DEFAULT_API_BASE_URL = os.getenv(
    "ASSISTANT_API_BASE_URL",
    "http://127.0.0.1:8080/api/v1",
)


class AssistantApiClient:
    """Small API client for the Streamlit executive assistant UI."""

    def __init__(self, base_url: str) -> None:
        """Initializes the client.

        Args:
            base_url: Base FastAPI URL including the API version prefix.
        """
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Runs a GET request against the assistant API."""
        return self._request("GET", path, params=params)

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        """Runs a POST request against the assistant API."""
        return self._request("POST", path, json=payload)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        with httpx.Client(timeout=30.0) as client:
            response = client.request(method, f"{self.base_url}{path}", **kwargs)
            response.raise_for_status()
            if not response.content:
                return None
            return response.json()


def main() -> None:
    """Runs the Streamlit UI."""
    st.set_page_config(
        page_title="Email AI Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _apply_styles()
    _initialize_state()

    st.title("Email AI Assistant")
    st.caption("Review email workflows, meeting prep, follow-ups, and integrations.")

    api_client = _build_api_client()
    _render_sidebar(api_client)

    tabs = st.tabs(
        [
            "Email Review",
            "Gmail Flow",
            "Meetings",
            "Follow-ups",
            "Notifications",
            "Memory",
            "Vectors",
        ]
    )

    with tabs[0]:
        _render_email_review(api_client)
    with tabs[1]:
        _render_gmail_flow(api_client)
    with tabs[2]:
        _render_meetings(api_client)
    with tabs[3]:
        _render_followups(api_client)
    with tabs[4]:
        _render_notifications(api_client)
    with tabs[5]:
        _render_memory(api_client)
    with tabs[6]:
        _render_vectors(api_client)


def _initialize_state() -> None:
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid4())


def _build_api_client() -> AssistantApiClient:
    with st.sidebar:
        st.header("Connection")
        base_url = st.text_input("API base URL", value=DEFAULT_API_BASE_URL)
    return AssistantApiClient(base_url)


def _render_sidebar(api_client: AssistantApiClient) -> None:
    with st.sidebar:
        if st.button("Check API", use_container_width=True):
            _call_api(
                "Health check",
                lambda: api_client.get("/health"),
                success_message="API is reachable.",
            )
        st.divider()
        st.write("Run FastAPI first:")
        st.code("uvicorn src.main:app --reload --port 8020", language="powershell")


def _render_email_review(api_client: AssistantApiClient) -> None:
    st.subheader("Classify and draft a reply")
    left, right = st.columns([1, 1])

    with left:
        sender = st.text_input("Sender", value="alex@example.com", key="email_sender")
        subject = st.text_input(
            "Subject",
            value="Q3 planning follow-up",
            key="email_subject",
        )
        body = st.text_area(
            "Email body",
            value=(
                "Could you review the Q3 roadmap before tomorrow's planning call? "
                "We need your decision on the launch timeline."
            ),
            height=180,
            key="email_body",
        )
        tone = st.selectbox(
            "Reply tone",
            ["professional", "warm", "concise", "executive"],
            key="email_tone",
        )
        style_samples = st.text_area(
            "Writing style samples",
            value="Thanks for the context. I will review and follow up shortly.",
            height=100,
            key="email_style_samples",
        )

        classify_clicked = st.button("Classify", use_container_width=True)
        draft_clicked = st.button("Generate draft reply", use_container_width=True)

    with right:
        if classify_clicked:
            payload = {"sender": sender, "subject": subject, "body": body}
            _call_api(
                "Classification", lambda: api_client.post("/emails/classify", payload)
            )

        if draft_clicked:
            payload = {
                "sender": sender,
                "subject": subject,
                "body": body,
                "tone": tone,
                "writing_style_samples": _lines(style_samples),
            }
            _call_api(
                "Draft reply", lambda: api_client.post("/emails/draft-reply", payload)
            )


def _render_gmail_flow(api_client: AssistantApiClient) -> None:
    st.subheader("Real Gmail workflow")
    recent_tab, draft_tab, morning_tab, send_tab = st.tabs(
        ["Recent", "Draft from message", "Morning review", "Send"]
    )

    with recent_tab:
        limit = st.slider("Message limit", min_value=1, max_value=50, value=10)
        if st.button("Load recent messages", use_container_width=True):
            _call_api(
                "Recent messages",
                lambda: api_client.get("/emails/recent", params={"limit": limit}),
            )

    with draft_tab:
        message_id = st.text_input("Gmail message ID")
        tone = st.selectbox(
            "Tone", ["professional", "warm", "concise"], key="gmail_tone"
        )
        create_draft = st.toggle("Create Gmail draft", value=True)
        if st.button("Draft reply for message", use_container_width=True):
            payload = {
                "tone": tone,
                "writing_style_samples": [],
                "create_gmail_draft": create_draft,
            }
            _call_api(
                "Message draft",
                lambda: api_client.post(
                    f"/emails/messages/{message_id}/draft-reply", payload
                ),
            )

    with morning_tab:
        review_limit = st.slider("Review limit", min_value=1, max_value=50, value=10)
        review_tone = st.selectbox(
            "Review tone",
            ["professional", "warm", "concise"],
            key="review_tone",
        )
        create_drafts = st.toggle(
            "Create Gmail drafts", value=True, key="create_drafts"
        )
        if st.button("Run morning review", use_container_width=True):
            payload = {
                "limit": review_limit,
                "tone": review_tone,
                "writing_style_samples": [],
                "create_gmail_drafts": create_drafts,
            }
            _call_api(
                "Morning review",
                lambda: api_client.post("/emails/morning-review", payload),
            )

    with send_tab:
        to = st.text_input("To", value="alex@example.com", key="send_to")
        subject = st.text_input("Subject", value="Re: Q3 planning", key="send_subject")
        body = st.text_area(
            "Body", value="Thanks. I will review this today.", height=180
        )
        action = st.radio("Action", ["Create draft", "Send email"], horizontal=True)
        if st.button("Submit", use_container_width=True):
            payload = {"to": to, "subject": subject, "body": body}
            path = "/emails/drafts" if action == "Create draft" else "/emails/send"
            _call_api(action, lambda: api_client.post(path, payload))


def _render_meetings(api_client: AssistantApiClient) -> None:
    st.subheader("Meeting summaries and briefs")
    summary_tab, brief_tab = st.tabs(["Summary", "Pre-meeting brief"])

    with summary_tab:
        title = st.text_input("Meeting title", value="Product planning sync")
        transcript = st.text_area(
            "Transcript",
            value=(
                "Maya will finalize the launch checklist. Jordan will confirm pricing. "
                "The team agreed to review customer feedback before Friday."
            ),
            height=220,
        )
        if st.button("Summarize meeting", use_container_width=True):
            payload = {"title": title, "transcript": transcript}
            _call_api(
                "Meeting summary",
                lambda: api_client.post("/meetings/summaries", payload),
            )

    with brief_tab:
        title = st.text_input("Brief title", value="Customer renewal call")
        starts_at = st.datetime_input(
            "Starts at",
            value=datetime.now() + timedelta(days=1),
        )
        attendees = st.text_area(
            "Attendee emails", value="sam@example.com\nlee@example.com"
        )
        agenda = st.text_area(
            "Agenda", value="Renewal risks, expansion options, next steps"
        )
        if st.button("Create brief", use_container_width=True):
            payload = {
                "title": title,
                "starts_at": starts_at.isoformat(),
                "attendee_emails": _lines(attendees),
                "agenda": agenda,
            }
            _call_api(
                "Meeting brief", lambda: api_client.post("/meetings/briefs", payload)
            )


def _render_followups(api_client: AssistantApiClient) -> None:
    st.subheader("Follow-up tracking")
    create_col, list_col = st.columns([1, 1])

    with create_col:
        subject = st.text_input("Subject", value="Send Q3 roadmap decision")
        recipient = st.text_input("Recipient", value="alex@example.com")
        due_at = st.datetime_input("Due at", value=datetime.now() + timedelta(days=2))
        notes = st.text_area("Notes", value="Confirm launch timeline before planning.")
        if st.button("Create follow-up", use_container_width=True):
            payload = {
                "subject": subject,
                "recipient": recipient,
                "due_at": due_at.isoformat(),
                "notes": notes or None,
            }
            _call_api(
                "Created follow-up", lambda: api_client.post("/followups", payload)
            )

    with list_col:
        if st.button("Refresh follow-ups", use_container_width=True):
            _call_api("Follow-ups", lambda: api_client.get("/followups"))


def _render_notifications(api_client: AssistantApiClient) -> None:
    st.subheader("Telegram notification")
    message = st.text_area(
        "Message",
        value="Morning review is ready. Three replies need approval.",
        height=160,
    )
    chat_id = st.text_input("Chat ID override")
    if st.button("Send Telegram notification", use_container_width=True):
        payload = {"message": message, "chat_id": chat_id or None}
        _call_api(
            "Telegram notification",
            lambda: api_client.post("/notifications/telegram", payload),
        )


def _render_memory(api_client: AssistantApiClient) -> None:
    st.subheader("Chat history memory")
    conversation_id = st.text_input("Conversation ID", key="conversation_id")
    role = st.selectbox("Role", ["user", "assistant", "system"])
    content = st.text_area(
        "Message", value="Remember that Q3 launch reviews are urgent."
    )

    add_col, list_col = st.columns([1, 1])
    with add_col:
        if st.button("Store message", use_container_width=True):
            payload = {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
            }
            _call_api(
                "Stored message", lambda: api_client.post("/chat/messages", payload)
            )
    with list_col:
        if st.button("Load conversation", use_container_width=True):
            _call_api(
                "Conversation messages",
                lambda: api_client.get(
                    f"/chat/conversations/{conversation_id}/messages"
                ),
            )


def _render_vectors(api_client: AssistantApiClient) -> None:
    st.subheader("Vector document storage")
    st.info("Use numeric embeddings that match VECTOR_DIMENSION in your environment.")
    add_tab, search_tab = st.tabs(["Add document", "Search"])

    with add_tab:
        namespace = st.text_input("Namespace", value="briefs", key="add_namespace")
        content = st.text_area(
            "Content", value="Customer renewal notes and next steps."
        )
        embedding = st.text_area("Embedding", value="0.1, 0.2, 0.3")
        metadata = st.text_area("Metadata JSON", value='{"source": "streamlit"}')
        if st.button("Add vector document", use_container_width=True):
            payload = {
                "namespace": namespace,
                "content": content,
                "embedding": _parse_embedding(embedding),
                "metadata": _parse_metadata(metadata),
            }
            _call_api(
                "Vector document",
                lambda: api_client.post("/vectors/documents", payload),
            )

    with search_tab:
        namespace = st.text_input("Namespace", value="briefs", key="search_namespace")
        embedding = st.text_area("Query embedding", value="0.1, 0.2, 0.3")
        limit = st.slider("Limit", min_value=1, max_value=50, value=5)
        if st.button("Search vectors", use_container_width=True):
            payload = {
                "namespace": namespace,
                "embedding": _parse_embedding(embedding),
                "limit": limit,
            }
            _call_api(
                "Vector search", lambda: api_client.post("/vectors/search", payload)
            )


def _call_api(
    title: str,
    action: Callable[[], Any],
    success_message: str = "Request completed.",
) -> None:
    try:
        with st.spinner("Working..."):
            result = action()
    except httpx.ConnectError:
        st.error("Could not connect to the API. Start FastAPI and check the base URL.")
    except httpx.HTTPStatusError as exc:
        st.error(f"API returned {exc.response.status_code}.")
        _render_json(exc.response.text)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        st.error(str(exc))
    else:
        st.success(success_message)
        st.markdown(f"**{title}**")
        _render_json(result)


def _render_json(value: Any) -> None:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            st.code(value)
            return
    st.json(value)


def _lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _parse_embedding(value: str) -> list[float]:
    cleaned = value.strip()
    if not cleaned:
        return []
    if cleaned.startswith("["):
        parsed = json.loads(cleaned)
        if not isinstance(parsed, list):
            raise ValueError("Embedding JSON must be a list of numbers.")
        return [float(item) for item in parsed]
    return [float(item.strip()) for item in cleaned.split(",") if item.strip()]


def _parse_metadata(value: str) -> dict[str, str]:
    if not value.strip():
        return {}
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Metadata must be a JSON object.")
    return {str(key): str(item) for key, item in parsed.items()}


def _apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.75rem;
        }
        [data-testid="stJson"] {
            border: 1px solid rgba(49, 51, 63, 0.16);
            border-radius: 8px;
            padding: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
