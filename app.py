import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
# * `/api/v1.0/precipitation`
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.

    results = session.query(Measurement.date,Measurement.prcp).all()

    all_prcps = dict(results.date,results.prcp)

    return jsonify(all_prcps)


@app.route("/api/v1.0/stations")
# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.
def stations():

    stat_names = session.query(Station.name).all()
    return jsonify(stat_names)

# @app.route("/api/v1.0/tobs")
# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.

def tobs():
    last_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>'2016-08-23').all()
    return jsonify(last_year)


@app.route("/api/v1.0/<start>")
def startw(start):
    start_date = start
    end_date='2017-08-23'
    start_end=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(start_end)


@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    start_date = start
    end_date=end
    start_end=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(start_end)


if __name__ == '__main__':
    app.run(debug=True)





