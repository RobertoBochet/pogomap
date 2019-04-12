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

reggie = Reggie()
app = Flask(__name__)
reggie.init_app(app)


@app.route("/getentities/<regex('(gyms(_eligible)?)|(pokestop(_eligible)?)|((not)?inpogo)|unverified'):type>/")
def get_entities(type):
	respose = None
	return json.dumps(respose)


@app.route("/<regex('[0-9a-zA-Z]+'):key>/")
def map_key(key):
	return render_template("index.html",key=key)

@app.route('/')
def map():
	return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return redirect("/static/favicon/favicon.ico", code=301)
    #return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

	pogomap = PogoMap(
		db_host = os.environ["DB_HOST"],
		db_user = os.environ["DB_USER"],
		db_pass = os.environ["DB_PASS"],
		db_name = os.environ["DB_NAME"]
	)

	app.run(debug=False,host='0.0.0.0',port=5775)
