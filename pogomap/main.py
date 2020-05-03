#!/usr/bin/env python3
import argparse
import logging

from webapp import WebApp

if __name__ == "__main__":
    # Get inline arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-k", "--google-api-key", dest="google_api_key", help="the google api key")
    parser.add_argument("-d", "--pg-host", dest="pg_host", help="postgres host")
    parser.add_argument("-u", "--pg-user", dest="pg_user", help="postgres user")
    parser.add_argument("-p", "--pg-pass", dest="pg_pass", help="postgres password")
    parser.add_argument("-n", "--pg-db-name", dest="pg_db_name", help="postgres database name")
    parser.add_argument("-f", "--flask-port", dest="flask_port", help="flask listening port")

    parser.add_argument("-v", dest="log_level", action="count", default=0,
                        help="number of -v specifics level of verbosity")
    parser.add_argument("--info", dest="log_level", action="store_const", const=2,
                        help="equal to -vv")
    parser.add_argument("--debug", dest="log_level", action="store_const", const=3,
                        help="equal to -vvv")

    # Parses args
    args = vars(parser.parse_args())
    # Remove None elements
    args = {k: args[k] for k in args if args[k] is not None}

    # Verbosity level map
    VERBOSITY_LEVELS = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }

    # Compute verbosity level
    args["log_level"] = VERBOSITY_LEVELS[args["log_level"]] if args["log_level"] < 4 else VERBOSITY_LEVELS[3]

    # Find flask port
    try:
        flask_port = args.pop("flask_port")
    except KeyError:
        flask_port = None

    # Create the web app
    app = WebApp(**args)

    # Run the web app
    app.run(debug=True, port=flask_port)
