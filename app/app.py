#!/usr/bin/env python3
import os
from flask import Flask, render_template
from flask_reggie import Reggie
from pogomap import PogoMap
import json
import time

reggie = Reggie()
app = Flask(__name__)
reggie.init_app(app)


@app.route("/getentities/<regex('(gyms(_eligible)?)|(pokestop(_eligible)?)|((not)?inpogo)|unverified'):type>/")
def get_entities(type):
    respose = None
    return json.dumps(respose)


@app.route('/<regex("[0-9a-zA-Z]+"):key>/')
def map_key(key):
    return render_template("index.html",key=key)

@app.route('/')
def map():
    return render_template("index.html")

@app.route('/map.js')
def map_js():
    return render_template("map.js")

@app.route('/map.css')
def map_css():
    return render_template("map.css")

@app.route("/layers/<path:path>")
def layers(path):
    return render_template("/layers/"+path)

if __name__ == '__main__':
    while True:
        try:
            pogomap = PogoMap(
                db_host = os.environ["DB_HOST"],
                db_user = os.environ["DB_USER"],
                db_pass = os.environ["DB_PASS"],
                db_name = os.environ["DB_NAME"]
            )
            print("connected")
            break
        except:
#            print("waiting to connection")
            time.sleep(1)

    app.run(debug=True,host='0.0.0.0',port=5775)
