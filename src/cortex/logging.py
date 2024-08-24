import logging
from rich.logging import RichHandler
from rich.console import Console


def set_logger(
    name: str = 'cortex',
    log_level: int = logging.INFO,
) -> logging.Logger:
    """Set up a logger with a specified name and log level.

    Args:
        name (str): The name of the logger.
        log_level (int): The log level for this logger.

    Returns:
        logging.Logger: The logger object.

    """
    # Create a logger with a specified name.
    logger = logging.getLogger(name)

    # Set the log level for this logger.
    logger.setLevel(log_level)

    # Create a RichHandler for console output.
    console_handler = RichHandler(
        console=Console(),
        rich_tracebacks=True,
        log_time_format='[%X]',
        # tracebacks_show_locals=True,
        keywords=[name],
    )

    # Create a formatter.
    formatter = logging.Formatter('%(name)-8s %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevent logging from propagating to the root logger.
    logger.propagate = False

    return logger


# Global library logger.
logger = set_logger()
