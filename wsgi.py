import os

from webapp import WebApp


def gunicorn_entry():
    """Entry point for Gunicorn

    It retrieves the option from envs and return an initialized instance of WebApp"""

    env = {}

    env["pg_host"] = os.getenv("PG_HOST")
    env["pg_user"] = os.getenv("PG_USER")
    env["pg_pass"] = os.getenv("PG_PASS")
    env["pg_db_name"] = os.getenv("PG_DB_NAME")
    env["log_level"] = os.getenv("LOG_LEVEL")

    # Remove None env
    env = {k: env[k] for k in env if env[k] is not None}

    # Return initialized WebApp
    return WebApp(**env)
