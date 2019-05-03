#!/usr/bin/env python3
import os
from flask import Flask, render_template, send_from_directory, redirect
from flask_reggie import Reggie
from pogomap import PogoMap
import json
import time
import logging
import signal
import sys

app = Flask(__name__)
Reggie(app)


@app.route("/get_entities/<regex('(gyms(_eligible)?)|(pokestop(_eligible)?)|((not_)?in_pogo)|unverified'):type>/")
def get_entities(type):
    response = pogomap.query(type)
    return response.json


@app.route("/<regex('[0-9a-zA-Z]{32}'):key>/")
def map_key(key):
    return render_template("index.html", key=key)


@app.route("/")
def map():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon/favicon.ico", code=301)


logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

pogomap = PogoMap(
    db_host=os.environ["DB_HOST"],
    db_user=os.environ["DB_USER"],
    db_pass=os.environ["DB_PASS"],
    db_name=os.environ["DB_NAME"]
)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5775)
