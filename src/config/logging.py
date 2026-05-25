import logging


class LoggingConfigurator:
    """Configures application logging."""

    def configure(self) -> None:
        """Applies the default logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
        )
