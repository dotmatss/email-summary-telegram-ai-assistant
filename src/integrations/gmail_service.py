from typing import Protocol


class GmailService(Protocol):
    """Contract for Gmail provider operations."""

    def list_recent_messages(self, limit: int = 10) -> list[dict[str, str]]:
        """Lists recent Gmail messages.

        Args:
            limit: Maximum number of messages to return.

        Returns:
            Recent message records.
        """
        ...

    def get_message(self, message_id: str) -> dict[str, str]:
        """Gets one Gmail message by identifier.

        Args:
            message_id: Gmail message identifier.

        Returns:
            Message record.
        """
        ...

    def create_draft(self, to: str, subject: str, body: str) -> dict[str, str]:
        """Creates a Gmail draft.

        Args:
            to: Recipient email address.
            subject: Draft subject.
            body: Draft body.

        Returns:
            Draft payload.
        """
        ...

    def send_email(self, to: str, subject: str, body: str) -> dict[str, str]:
        """Sends an email through Gmail.

        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Email body.

        Returns:
            Sent email provider payload.
        """
        ...
