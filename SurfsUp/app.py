# Import the dependencies.
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
Base.prepare(autoload_with=engine)

# Save references to each table to the classes named station and measurement.
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"//api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
        
@app.route("/api/v1.0/precipitation")
def precipationpy():
    start_date = "2016-08-23"
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary
    sel = [measurement.date, func.sum(measurement.prcp)]
    precip = session.query(*sel).\
        filter(measurement.date >= start_date).\
        group_by(measurement.date).\
        order_by(measurement.date.desc()).all()
    
    # Convert the result to a dictionary
    precip_dict = {date: prcp for date, prcp in precip}
    
    session.close()
    #Return the JSON representation of your dictionary.
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stationpy():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    sel = [measurement.station]

    # Return a JSON list of stations from the dataset.
    station_list = session.query(*sel).\
        group_by(measurement.station).all()
    
    session.close()
    station_list = list(np.ravel(station_list)) 
    
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobspy():
    start_date = "2016-08-23"
    most_active_station = 'USC00519281'
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary
    sel = [measurement.date,Measurement.tobs]
    temp = session.query(*sel).\
    filter(measurement.date >= start_date).\
    filter(measurement.station == most_active_station).\
    group_by(measurement.date).\
    order_by(measurement.date).all()
    
    session.close()
    #Return the JSON representation of your dictionary.
    # Initialize an empty dictionary
    tobs_dict = {}

    for date, observation in temp:
        if date not in tobs_dict:
            tobs_dict[date] = []
        tobs_dict[date].append(observation)

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def startpy(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    session.close()

    min_temp, avg_temp, max_temp = query_result[0]

    # Create a dictionary with the results
    temp_stats = {
        "min": min_temp,
        "avg": avg_temp,
        "max": max_temp
    }

    return(temp_stats)
    
@app.route("/api/v1.0/<start>/<end>")
def startendpy(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    # Create a dictionary with the results
    temp_stats = {
        "min": min_temp,
        "avg": avg_temp,
        "max": max_temp
    }

    return(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)