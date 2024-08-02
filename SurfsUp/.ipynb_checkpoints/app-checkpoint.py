# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


# 1) precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Calculate the date one year from the last date in data set.
        query_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

        # Perform a query to retrieve the data and precipitation scores
        results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()
       
        # Create a dictionary to store the date and precipitation values
        prcp_last_year = {}

        # Iterate through the query results and populate the dictionary
        for date, prcp in results:
            if prcp is not None:
                prcp_last_year[date] = prcp

        return jsonify(prcp_last_year)


# 2) stations route
@app.route("/api/v1.0/stations")
def stations():
        #return jsonified list of stations from the dataset
        results = session.query(Station.station).all()

        # Convert list of tuples into normal list
        station_names = list(np.ravel(results))

        return jsonify(station_names)


# 3) tobs route
@app.route("/api/v1.0/tobs")
def tobs():
        query_date_2 = dt.date(2017, 8, 18) - dt.timedelta(days = 365)
        results_2 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date_2).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

        # Create a dictionary to store the date and temperature values
        temp_last_year = {}

        # Iterate through the query results and populate the dictionary
        for date, temp in results_2:
            if temp is not None:
                temp_last_year[date] = temp

        return jsonify(temp_last_year)


# 4) <start> route
@app.route("/api/v1.0/<start>")
def start(start):
        stats = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        
        stats_result = session.query(*stats).\
        filter(Measurement.date >= start)\
        .all()

        return jsonify(stats_result)
    




if __name__ == '__main__':
    app.run(debug=True)
