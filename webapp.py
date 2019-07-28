import logging

import flask
import flask_reggie

from ResponseJSON import ResponseJSON
from pogomap import PogoMap
from pogomap.exceptions import InvalidEntity


class WebApp:
    def __init__(self, flask_port: int = 5775, **kwargs):
        # Retrieves logger
        self.logger = logging.getLogger(__name__)

        # Init map
        self.pogomap = PogoMap(**kwargs)

        # Init Flask
        self.flask = flask.Flask(__name__)

        # Init Flask regex
        flask_reggie.Reggie(self.flask)

        # Set url rules
        self.flask.add_url_rule("/get_entities/<string:entity_type>/", "get_entities", view_func=self.get_entities)
        self.flask.add_url_rule("/set_entities/", "set_entities", methods=["POST"], view_func=self.set_entities)
        self.flask.add_url_rule("/add_entities/", "add_entities", methods=["POST"], view_func=self.add_entities)
        self.flask.add_url_rule("/<regex('[0-9a-zA-Z]{32}'):key>/", "map_key", view_func=self.map_key)
        self.flask.add_url_rule("/", "map", view_func=self.map)
        self.flask.add_url_rule("/favicon.ico", "favicon", view_func=self.favicon)

        # Start flask
        self.flask.run(port=flask_port)

    def get_entities(self, entity_type: str = None):
        try:
            entities = self.pogomap.get_entities(entity_type)

            return ResponseJSON(payload=entities, payload_name="entities")

        except InvalidEntity as e:
            logging.info("Exception {}".format(type(e).__name__))
            return ResponseJSON(exception=e)

    def set_entities(self):
        if "key" not in flask.request.json:
            return ResponseJSON(error="Must be provided an authentication key")

        if not self.pogomap.is_editor_key_valid(flask.request.json["key"]):
            return ResponseJSON(error="Invalid authentication key")

        if "id" not in flask.request.json or \
                "type" not in flask.request.json or \
                "is_eligible" not in flask.request.json:
            return ResponseJSON(error="Must be provided id, type and is_eligible")

        try:
            new_entity = self.pogomap.set_entity(id=flask.request.json["id"], type=flask.request.json["type"],
                                                 is_eligible=flask.request.json["is_eligible"])

            return ResponseJSON(payload=new_entity, payload_name="entity")

        except Exception as e:
            self.logger.info("Exception {}".format(type(e).__name__))
            return ResponseJSON(exception=e)

    def add_entities(self):
        if "key" not in flask.request.json:
            return ResponseJSON(error="Must be provided an authentication key")

        if not self.pogomap.is_editor_key_valid(flask.request.json["key"]):
            return ResponseJSON(error="Invalid authentication key")

        if "entities" not in flask.request.json:
            return ResponseJSON(error="Must be provided some entities")

        try:
            self.pogomap.add_entities(flask.request.json["entities"])

            return ResponseJSON()

        except Exception as e:
            self.logger.info("Exception {}".format(type(e).__name__))
            return ResponseJSON(exception=e)

    def map_key(self, key: str):
        if self.pogomap.is_editor_key_valid(key):
            return flask.render_template("index.html", key=key)
        else:
            return "Key is not valid"

    def map(self):
        return flask.render_template("index.html")

    def favicon(self):
        return flask.redirect("/static/favicon/favicon.ico", code=301)
