import logging


def intial_setup():
    # Set format for the log
    logging.basicConfig(format="%(levelname)s|%(name)s|%(message)s")


def setup_log_levels(log_level: int, modules_log_level: int = logging.ERROR):
    # Set log level for application logger
    logging.getLogger("webapp").setLevel(log_level)

    # Set log level for modules
    logging.getLogger("flask").setLevel(modules_log_level)
    logging.getLogger("werkzeug").setLevel(modules_log_level)
