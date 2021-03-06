import logging
from os.path import join, dirname, abspath
from typing import Union

import flask
import flask_reggie
from flask import Flask

import log
from ResponseJSON import ResponseJSON
from pogomap import PogoMap
from pogomap.exceptions import InvalidEntity


class WebApp(Flask):
    def __init__(self, google_api_key: str, log_level: Union[int, str] = logging.ERROR,
                 **kwargs):
        super(WebApp, self).__init__("pogomap",
                                     template_folder=join(dirname(abspath(__file__)), 'templates'),
                                     static_folder=join(dirname(abspath(__file__)), 'static'))

        # Init log
        log.intial_setup()
        log.setup_log_levels(log_level)

        # Retrieves logger
        self.logger = logging.getLogger(__name__)

        # Save google api key
        self.google_api_key = google_api_key

        # Init map
        self.pogomap = PogoMap(**kwargs)

        # Init Flask regex
        flask_reggie.Reggie(self)

        # Set url rules
        self.add_url_rule("/get_entities/<string:entity_type>/", "get_entities", view_func=self.get_entities)
        self.add_url_rule("/set_entities/", "set_entities", methods=["POST"], view_func=self.set_entities)
        self.add_url_rule("/add_entities/", "add_entities", methods=["POST"], view_func=self.add_entities)
        self.add_url_rule("/remove_entities/", "remove_entities", methods=["POST"], view_func=self.remove_entities)
        self.add_url_rule("/<regex('[0-9a-zA-Z]{32}'):key>/", "map_key", view_func=self.map_key)
        self.add_url_rule("/", "map", view_func=self.map)
        self.add_url_rule("/favicon.ico", "favicon", view_func=self.favicon)

        self.logger.info("The web app is ready")

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
            new_entity = self.pogomap.set_entity(entity_id=flask.request.json["id"],
                                                 entity_type=flask.request.json["type"],
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
            new_portals = self.pogomap.add_entities(flask.request.json["entities"])

            return ResponseJSON(payload_name="entities", payload=new_portals)

        except Exception as e:
            import traceback;traceback.print_exc()
            self.logger.info("Exception {}".format(type(e).__name__))
            return ResponseJSON(exception=e)

    def remove_entities(self):
        if "key" not in flask.request.json:
            return ResponseJSON(error="Must be provided an authentication key")

        if not self.pogomap.is_editor_key_valid(flask.request.json["key"]):
            return ResponseJSON(error="Invalid authentication key")

        if "entities" not in flask.request.json:
            return ResponseJSON(error="Must be provided some entities")

        try:
            self.pogomap.remove_entities(flask.request.json["entities"])

            return ResponseJSON()

        except Exception as e:
            self.logger.info("Exception {}".format(type(e).__name__))
            return ResponseJSON(exception=e)

    def map_key(self, key: str):
        if self.pogomap.is_editor_key_valid(key):
            return flask.render_template("index.html", google_api_key=self.google_api_key, key=key)
        else:
            return "Key is not valid"

    def map(self):
        return flask.render_template("index.html", google_api_key=self.google_api_key)

    @classmethod
    def favicon(cls):
        return flask.redirect("/static/favicon/favicon.ico", code=301)
