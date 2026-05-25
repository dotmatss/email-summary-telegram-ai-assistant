from datetime import UTC, datetime


class DateTimeProvider:
    """Provides date and time values."""

    def utc_now(self) -> datetime:
        """Returns the current UTC datetime.

        Returns:
            Current timezone-aware UTC datetime.
        """
        return datetime.now(tz=UTC)
