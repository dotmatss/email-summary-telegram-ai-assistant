from email.utils import parseaddr
from typing import Any

from src.agents.email_agent import EmailAgent
from src.schemas.email import DraftReplyRequest, EmailClassificationRequest
from src.integrations.gmail_service import GmailService


class EmailReviewGraphBuilder:
    """Builds a LangGraph workflow for morning email review."""

    def __init__(self, gmail_service: GmailService, email_agent: EmailAgent) -> None:
        """Initializes the graph builder.

        Args:
            gmail_service: Gmail provider service.
            email_agent: Email agent.
        """
        self._gmail_service = gmail_service
        self._email_agent = email_agent

    def build(self) -> Any:
        """Builds the compiled morning review graph."""
        from langgraph.graph import END, StateGraph

        graph = StateGraph(dict)
        graph.add_node("load_messages", self._load_messages)
        graph.add_node("classify_messages", self._classify_messages)
        graph.add_node("draft_replies", self._draft_replies)
        graph.add_node("create_gmail_drafts", self._create_gmail_drafts)
        graph.set_entry_point("load_messages")
        graph.add_edge("load_messages", "classify_messages")
        graph.add_edge("classify_messages", "draft_replies")
        graph.add_edge("draft_replies", "create_gmail_drafts")
        graph.add_edge("create_gmail_drafts", END)
        return graph.compile()

    def _load_messages(self, state: dict[str, Any]) -> dict[str, Any]:
        """Loads recent Gmail messages into graph state."""
        return {
            **state,
            "messages": self._gmail_service.list_recent_messages(
                limit=state["request"].limit
            ),
        }

    def _classify_messages(self, state: dict[str, Any]) -> dict[str, Any]:
        """Classifies every message in graph state."""
        classifications = []
        for message in state["messages"]:
            request = EmailClassificationRequest(
                sender=self._extract_email(message.get("sender", "")),
                subject=message.get("subject") or "(no subject)",
                body=message.get("body") or message.get("snippet") or "(empty)",
            )
            classifications.append(self._email_agent.classify(request).model_dump())
        return {**state, "classifications": classifications}

    def _draft_replies(self, state: dict[str, Any]) -> dict[str, Any]:
        """Drafts replies for important and urgent messages."""
        drafts = []
        review_request = state["request"]
        for message, classification in zip(
            state["messages"],
            state["classifications"],
            strict=False,
        ):
            if classification["category"] not in {"important", "urgent"}:
                drafts.append(None)
                continue

            request = DraftReplyRequest(
                sender=self._extract_email(message.get("sender", "")),
                subject=message.get("subject") or "(no subject)",
                body=message.get("body") or message.get("snippet") or "(empty)",
                tone=review_request.tone,
                writing_style_samples=review_request.writing_style_samples,
            )
            drafts.append(self._email_agent.draft_reply(request).model_dump())
        return {**state, "drafts": drafts}

    def _create_gmail_drafts(self, state: dict[str, Any]) -> dict[str, Any]:
        """Creates Gmail drafts for drafted replies when enabled."""
        review_request = state["request"]
        if not review_request.create_gmail_drafts:
            return {
                **state,
                "gmail_drafts": [None for _ in state["messages"]],
            }

        gmail_drafts = []
        for message, draft in zip(state["messages"], state["drafts"], strict=False):
            if not draft:
                gmail_drafts.append(None)
                continue
            gmail_drafts.append(
                self._gmail_service.create_draft(
                    to=self._extract_email(message.get("sender", "")),
                    subject=draft["subject"],
                    body=draft["body"],
                )
            )
        return {**state, "gmail_drafts": gmail_drafts}

    @staticmethod
    def _extract_email(value: str) -> str:
        """Extracts an email address from a header value."""
        _, address = parseaddr(value)
        return address or value or "unknown@example.com"
