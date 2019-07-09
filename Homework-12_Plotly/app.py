# import necessary libraries
# import pandas as pd
# import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import MetaData
from sqlalchemy import inspect
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql import text

from flask import (
    Flask,
    render_template,
    jsonify, 
    request)

# Database Setup

engine = create_engine("sqlite:///dataSets/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Name = Base.classes.samples
Otu = Base.classes.otu
sample_metaData = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

app = Flask(__name__)

# Routes

# Route to return to the homepage!

@app.route("/")
def index():
    return render_template('index.html')

# Route to return list of sample names
@app.route("/names")
def sample_names():
    inspector = inspect(engine)
    columns = inspector.get_columns('samples')
    print(columns)
    sample_names = []
    for column in columns[1:]:
        names = column["name"]
        sample_names.append(names)
    return jsonify(sample_names)
    
# #Route to return a List of OTU descriptions.
@app.route('/otu')
def description():
    results = session.query(Otu.lowest_taxonomic_unit_found).all()
    otu_description = list(np.ravel(results))
    return jsonify(otu_description)

# Route to return MetaData for a given sample
@app.route('/metadata/<sample>')
def metadata(sample):
    bbtype, sample_number = sample.split("_")
    sample_data = session.query(sample_metaData).filter(sample_metaData.SAMPLEID== sample_number).all()
    sample_details = {}
    for each in sample_data:
        sample_details["AGE"] = each.AGE
        sample_details["BBTYPE"] = each.BBTYPE
        sample_details["ETHNICITY"] = each.ETHNICITY
        sample_details["GENDER"] = each.GENDER
        sample_details["LOCATION"] = each.LOCATION
        sample_details["SAMPLEID"] = each.SAMPLEID
    return jsonify(sample_details)
        
    
    
#Route to return Weekly Washing Frequency as a number
@app.route('/wfreq/<sample>')
def washing_freq(sample):
    bbtype, sample_number = sample.split("_")
    washing_freq = session.query(sample_metaData.WFREQ).filter(sample_metaData.SAMPLEID == sample_number).all()
    return jsonify(washing_freq )


# #Route to return OTU IDs and Sample Values for a given sample
@app.route('/samples/<sample>')
def top_ten_samples(sample):
    bacteria = {}
    result1 = session.query(Otu.otu_id).all()
    bacteria["Otu Id"] = result1

    sql = "SELECT  otu_id,{0} FROM {1} order by {0} desc".format(sample, 'Samples')
    samplesData = session.query('otu_id',sample).from_statement(text(sql)).all()
    bacteria = {}
    otuIdList = []
    sampleList =[]
    for sample in samplesData:
        otuIdList.append(sample[0])
        sampleList.append(sample[1])	

    bacteria['otu_ids'] = otuIdList
    bacteria['sample_values'] = sampleList

    bacteriaList = []
    bacteriaList.append(bacteria)
    return jsonify(bacteriaList)

if __name__ == '__main__':
    app.run()