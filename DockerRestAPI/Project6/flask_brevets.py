"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

import flask
import pymongo
#from flask import request

import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)

# TODO - Changed the IP
client = MongoClient("172.18.0.2", 27017)


db = client.tododb

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

db_table = []

change = 0

@app.route('/_new')
def _new():
    for val in db_table:
        try:
            db.tododb.insert_one(val)
        except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in new collection
            continue

    result = 1
    if (db_table == []):
        result = 2
    return flask.jsonify(result=result)


@app.route('/_disp')
def _disp():
    _items = db.tododb.find()
    items = [item for item in _items]
    return render_template('test.html', items=items)


@app.route('/_clear')
def _clear():
    #clear database
    db.tododb.delete_many({})
    #clear table
    db_table.clear()

    result = 1
    return flask.jsonify(result=result)


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)

    time = request.args.get('time')
    date = request.args.get('date')
    dist = request.args.get('dist')

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    app.logger.debug("NOW: {}".format(arrow.now().isoformat))

    #Joining data together to form to iso format
    seq = (date, "T", time, ":00.000Z")
    iso = ''.join(seq)

    open_time = acp_times.open_time(km, dist, iso)
    close_time = acp_times.close_time(km, dist, iso)

    result = {"open": open_time, "close": close_time}


    db_table.append({'km':km, 'open_time':arrow.get(open_time).format("ddd M/D H:mm"),
                              'close_time':arrow.get(close_time).format("ddd M/D H:mm")})

    change = 1

    print(db_table)

    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
