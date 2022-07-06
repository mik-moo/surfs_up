
# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy as sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# access sqlite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# Create class variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session link
# session = Session(engine)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# define flask app
app = Flask(__name__)

# define welcome route
@app.route("/")

# routing info for the other data
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

# precipitation route
@app.route("/api/v1.0/precipitation")

# precipitation function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = db_session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   db_session.close()
   return jsonify(precip)

# stations route
@app.route("/api/v1.0/stations")

# stations function
def stations():
    results = db_session.query(Station.station).all()
    stations = list(np.ravel(results))
    db_session.close()
    return jsonify(stations=stations)

# temperature observations route
@app.route("/api/v1.0/tobs")

# temps function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = db_session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    db_session.close()
    return jsonify(temps=temps)

# temp stats routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# temp stats function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = db_session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        db_session.close()
        return jsonify(temps)

    results = db_session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    db_session.close()
    return jsonify(temps)

# run with out terminal
if __name__ == "__main__":
    app.run()