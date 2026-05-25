from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerFactory:
    """Creates background schedulers."""

    def create(self) -> BackgroundScheduler:
        """Creates the APScheduler background scheduler.

        Returns:
            Configured background scheduler.
        """
        return BackgroundScheduler(timezone="UTC")
