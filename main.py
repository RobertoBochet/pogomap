#!/usr/bin/env python3
import argparse
import logging

import log
from webapp import WebApp

if __name__ == "__main__":
    # Set logging format
    log.intial_setup()

    # Get inline arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--pg-host", dest="pg_host", help="postgres host")
    parser.add_argument("-u", "--pg-user", dest="pg_user", help="postgres user")
    parser.add_argument("-p", "--pg-pass", dest="pg_pass", help="postgres password")
    parser.add_argument("-n", "--pg-db-name", dest="pg_db_name", help="postgres database name")
    parser.add_argument("-f", "--flask-port", dest="flask_port", help="flask listening port")

    parser.add_argument("-v", dest="verbosity_level", action="count", default=0,
                        help="number of -v specifics level of verbosity")
    parser.add_argument("--info", dest="verbosity_level", action="store_const", const=2,
                        help="equal to -vv")
    parser.add_argument("--debug", dest="verbosity_level", action="store_const", const=3,
                        help="equal to -vvv")

    # Parses args
    args = vars(parser.parse_args())
    # Remove None elements
    args = {k: args[k] for k in args if args[k] is not None}

    # Verbosity level map
    verbosity_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }

    # Find verbosity level
    try:
        verbosity_level = verbosity_levels[args.pop("verbosity_level")]
    except KeyError:
        verbosity_level = verbosity_levels[3]

    # Set verbosity level
    log.setup_log_levels(verbosity_level)

    # Create the web app
    bot = WebApp(**args)
