# dependencies and necesities
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

# variables for bases
measurement = Base.classes.measurement
station = Base.classes.station

# make a flask app for everything to come
app = Flask(__name__)

# main page routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Precipitation and Temperature Information API.<br/>"
        f"Here are the available API calls:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date<br/>"
    )

# precip API call
@app.route("/api/v1.0/precipitation")
def precipitation():
    last12 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last12).all()
    precip = {date: prcp for date, prcp in precip_query}

    return jsonify(precip)

# station API call
@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(station.station, station.name).all()
    station = list(np.ravel(station_query))

    return jsonify(station)

# temperature API call
@app.route("/api/v1.0/tobs")
def temperature():
    last12 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp = session.query(measurement.date, measurement.tobs).filter(measurement.date >= last12).all()
    tobs = list(np.ravel(temp))

    return jsonify(tobs)

# start date API call
@app.route("/api/v1.0/start")
def temp_start(start):
    start_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    temp = list(np.ravel(start_query))

    return jsonify(temp)

# date range API call
@app.route("/api/v1.0/start/end")
def temp_date_range(start, end):
    start_end_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    temp =list(np.ravel(start_end_query))

    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)