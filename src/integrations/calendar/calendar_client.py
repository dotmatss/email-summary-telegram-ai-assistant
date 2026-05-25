from datetime import datetime


class CalendarClient:
    """Client boundary for Google Calendar API operations."""

    def list_events(self, starts_after: datetime, limit: int = 10) -> list[dict[str, str]]:
        """Lists calendar events.

        Args:
            starts_after: Lower bound for event start time.
            limit: Maximum number of events to return.

        Returns:
            Calendar event records.
        """
        return []
