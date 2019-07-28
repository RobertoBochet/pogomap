import logging
from typing import Union

VERBOSITY_LEVELS = {
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG
}

def intial_setup():
    # Set format for the log
    logging.basicConfig(format="%(levelname)s|%(name)s|%(message)s")


def setup_log_levels(log_level: Union[int,str], modules_log_level: Union[int,str] = logging.ERROR):
    if isinstance(log_level, str):
        log_level = VERBOSITY_LEVELS[log_level]

    if isinstance(modules_log_level, str):
        modules_log_level = VERBOSITY_LEVELS[modules_log_level]

    # Set log level for application logger
    logging.getLogger("webapp").setLevel(log_level)

    # Set log level for modules
    logging.getLogger("flask").setLevel(modules_log_level)
    logging.getLogger("werkzeug").setLevel(modules_log_level)
