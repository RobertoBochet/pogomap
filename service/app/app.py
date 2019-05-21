#!/usr/bin/env python3
import logging
import os

import flask
import flask_reggie

from ResponseJSON import ResponseJSON
from pogomap import PogoMap
from pogomap.exceptions import *

app = flask.Flask(__name__)
flask_reggie.Reggie(app)


@app.route("/get_entities/<string:entity_type>/")
def get_entities(entity_type=None):
    try:
        entities = pogomap.get_entities(entity_type)

        return ResponseJSON(payload=entities, payload_name="entities")

    except InvalidEntity as e:
        logging.info("Exception {}".format(type(e).__name__))
        return ResponseJSON(exception=e)


@app.route("/set_entities/", methods=["POST"])
def set_entities():
    if "key" not in flask.request.json:
        return ResponseJSON(error="Must be provided an authentication key")

    if not pogomap.is_editor_key_valid(flask.request.json["key"]):
        return ResponseJSON(error="Invalid authentication key")

    if "id" not in flask.request.json or "type" not in flask.request.json or "is_eligible" not in flask.request.json:
        return ResponseJSON(error="Must be provided id, type and is_eligible")

    try:
        new_entity = pogomap.set_entity(id=flask.request.json["id"], type=flask.request.json["type"],
                                        is_eligible=flask.request.json["is_eligible"])

        return ResponseJSON(payload=new_entity, payload_name="entity")

    except Exception as e:
        logging.info("Exception {}".format(type(e).__name__))
        return ResponseJSON(exception=e)


@app.route("/add_entities/", methods=["POST"])
def add_entities():
    if "key" not in flask.request.json:
        return ResponseJSON(error="Must be provided an authentication key")

    if not pogomap.is_editor_key_valid(flask.request.json["key"]):
        return ResponseJSON(error="Invalid authentication key")

    if "entities" not in flask.request.json:
        return ResponseJSON(error="Must be provided some entities")

    try:
        pogomap.add_entities(flask.request.json["entities"])

        return ResponseJSON()

    except Exception as e:
        logging.info("Exception {}".format(type(e).__name__))
        return ResponseJSON(exception=e)



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
