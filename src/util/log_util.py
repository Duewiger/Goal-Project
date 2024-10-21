
""" Module for logging utility functions. """

from datetime import datetime

def log_print(message, log_type="DEBUG"):
    """ Prints a message for logs. Prepends the datetime.
    Args:
        message (str): The string message to log.
        log_type (str): The type of log. Usually "NOTICE", "WARNING", "ERROR"
            or "DEBUG".
    """

    log_str = (
        f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] "
        f"[{log_type}] {message}"
    )

    print(log_str, file=open(log_type + ".log", "a"))

