import base64
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config.config import settings


class GmailClient:
    """Client boundary for Gmail API operations."""

    _SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/gmail.send",
    ]

    def list_recent_messages(self, limit: int = 10) -> list[dict[str, str]]:
        """Lists recent Gmail messages.

        Args:
            limit: Maximum number of messages to return.

        Returns:
            Recent message records.
        """
        service = self._build_service()
        result = (
            service.users()
            .messages()
            .list(userId="me", maxResults=limit, labelIds=["INBOX"])
            .execute()
        )
        messages = result.get("messages", [])
        return [
            self._get_message(service=service, message_id=message["id"])
            for message in messages
        ]

    def get_message(self, message_id: str) -> dict[str, str]:
        """Gets one Gmail message by identifier.

        Args:
            message_id: Gmail message identifier.

        Returns:
            Message record.
        """
        return self._get_message(service=self._build_service(), message_id=message_id)

    def create_draft(self, to: str, subject: str, body: str) -> dict[str, str]:
        """Creates a Gmail draft.

        Args:
            to: Recipient email address.
            subject: Draft subject.
            body: Draft body.

        Returns:
            Created draft payload.
        """
        service = self._build_service()
        raw_message = self._build_raw_message(to=to, subject=subject, body=body)
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body={"message": {"raw": raw_message}})
            .execute()
        )
        message = draft.get("message", {})
        return {
            "id": draft.get("id", ""),
            "message_id": message.get("id", ""),
        }

    def send_email(self, to: str, subject: str, body: str) -> dict[str, str]:
        """Sends an email through Gmail.

        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Email body.

        Returns:
            Sent message payload.
        """
        service = self._build_service()
        raw_message = self._build_raw_message(to=to, subject=subject, body=body)
        sent_message = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )
        return {
            "id": sent_message.get("id", ""),
            "thread_id": sent_message.get("threadId", ""),
            "label_ids": sent_message.get("labelIds", []),
        }

    def _build_service(self) -> Any:
        """Builds an authenticated Gmail API service."""
        credentials = self._load_credentials()
        try:
            return build("gmail", "v1", credentials=credentials)
        except HttpError as exc:
            raise RuntimeError("Unable to build Gmail API service.") from exc

    def _load_credentials(self) -> Credentials:
        """Loads, refreshes, or creates OAuth credentials for Gmail."""
        if not settings.gmail_credentials_file:
            raise RuntimeError(
                "GMAIL_CREDENTIALS_FILE must point to a Google OAuth client JSON file."
            )

        credentials_path = self._resolve_credentials_path(Path(settings.gmail_credentials_file))
        token_path = Path(settings.gmail_token_file)
        credentials = self._read_token(token_path)

        if credentials and credentials.valid:
            return credentials

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not credentials_path.exists():
                raise RuntimeError(f"Gmail credentials file does not exist: {credentials_path}")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path),
                scopes=self._SCOPES,
            )
            credentials = flow.run_local_server(port=0)

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(credentials.to_json(), encoding="utf-8")
        return credentials

    @staticmethod
    def _resolve_credentials_path(configured_path: Path) -> Path:
        """Resolves the configured client secret path with a local fallback."""
        if configured_path.exists():
            return configured_path

        candidates = sorted(Path("credentials").glob("client_secret_*.json"))
        if len(candidates) == 1:
            return candidates[0]

        return configured_path

    @staticmethod
    def _read_token(token_path: Path) -> Credentials | None:
        """Reads cached OAuth credentials when available."""
        if not token_path.exists():
            return None
        return Credentials.from_authorized_user_file(str(token_path), GmailClient._SCOPES)

    @staticmethod
    def _build_raw_message(to: str, subject: str, body: str) -> str:
        """Builds a URL-safe base64 encoded MIME email."""
        message = EmailMessage()
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        return base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    def _get_message(self, service: Any, message_id: str) -> dict[str, str]:
        """Fetches and normalizes a Gmail message."""
        message = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        payload = message.get("payload", {})
        headers = {
            header.get("name", "").lower(): header.get("value", "")
            for header in payload.get("headers", [])
        }
        return {
            "id": message.get("id", ""),
            "thread_id": message.get("threadId", ""),
            "sender": headers.get("from", ""),
            "to": headers.get("to", ""),
            "subject": headers.get("subject", ""),
            "snippet": message.get("snippet", ""),
            "body": self._extract_plain_text(payload),
        }

    def _extract_plain_text(self, payload: dict[str, Any]) -> str:
        """Extracts a plain text body from a Gmail message payload."""
        if payload.get("mimeType") == "text/plain":
            return self._decode_body(payload)

        for part in payload.get("parts", []):
            if part.get("mimeType") == "text/plain":
                return self._decode_body(part)
            nested_text = self._extract_plain_text(part)
            if nested_text:
                return nested_text

        return ""

    @staticmethod
    def _decode_body(part: dict[str, Any]) -> str:
        """Decodes a Gmail message body part."""
        data = part.get("body", {}).get("data")
        if not data:
            return ""
        padded_data = data + "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(padded_data.encode("utf-8")).decode(
            "utf-8",
            errors="replace",
        )
