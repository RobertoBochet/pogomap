#!/usr/bin/env python3
import logging
import os

import flask
import flask_reggie
from Response import Response
from pogomap import PogoMap
from pogomap.exceptions import *

app = flask.Flask(__name__)
flask_reggie.Reggie(app)


@app.route("/get_entities/<string:entity_type>/")
def get_entities(entity_type=None):
    try:
        entities = pogomap.get_entities(entity_type)

        response = Response(payload=entities, payload_name="entities")

    except InvalidEntity as e:
        logging.info("Exception {}".format(type(e).__name__))
        response = Response(exception=e)

    return app.response_class(response=response.to_json(), mimetype="application/json")


@app.route("/set_entities/")
def set_entities():
    return "ciao"


@app.route("/<regex('[0-9a-zA-Z]{32}'):key>/")
def map_key(key):
    if pogomap.is_editor_key_valid(key):
        return flask.render_template("index.html", key=key)
    else:
        return "Key is not valid"


@app.route("/")
def map():
    return flask.render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return flask.redirect("/static/favicon/favicon.ico", code=301)


logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

pogomap = PogoMap(
    db_host=os.environ["DB_HOST"],
    db_user=os.environ["DB_USER"],
    db_pass=os.environ["DB_PASS"],
    db_name=os.environ["DB_NAME"]
)

if __name__ == "__main__":
    app.run(debug=True)
