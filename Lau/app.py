import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#from sqlalchemy import Table, MetaData

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

############ Otro Método
# # esto funciona************
engine = create_engine("mysql+pymysql://root:D14n4P4rd0@127.0.0.1:3306/fifa_db?charset=utf8mb4")

#####reflect an existing database into a new model
Base = automap_base()
# # # # # reflect the tables
Base.prepare(engine, reflect=True)
session = Session(engine)

# # # # # Save references to each table
fifa = Base.classes.fifa



app = Flask(__name__)

#################################################
# Database Setup
#################################################
# password = "D14n4P4rd0"
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:{password}@localhost:3306/fifa_db?charset=utf8mb4"
# engine = create_engine(f'mysql+pymysql://{app.config["SQLALCHEMY_DATABASE_URI"]}')
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# fifa_db = Base.classes.fifa_db

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/fifa")
# def player():
#     stmt = session.query(fifa).statement
#     df = pd.read_sql_query(stmt, session.bind)
#     data = {
#         "id": df.player_id.values.tolist(),
#         "Name": df.player_name.values.tolist(),
#         "Age": df.age.values.tolist(),
#         "Nationality": df.nationality.values.tolist(),
#         "Overall": df.overall.values.tolist(),
#         "Potencial": df.potencial.values.tolist(),
#         "Club": df.club.values.tolist(),
#         "Value": df.player_value.values.tolist(),
#         "Wage": df.wage.values.tolist(),
#         "Relase_clause": df.relase_clause.values.tolist()
#     }
    
#     return jsonify(data)

@app.route("/names")
def teamn():
    # stmt = db.session.query(fifa.club).distinct().all()
    df = pd.read_sql_query('SELECT DISTINCT club FROM fifa', session.bind) #quite db.
    club = []
    for index, row in df.iterrows():
        t = {'club':row['club']}
        club.append(t)
    return jsonify(club)

@app.route("/names/<value>")
def theteam(value):
    # stmt = db.session.query(fifa.club).distinct().all()
    # df = pd.read_sql_query(f"SELECT player_name, overall, wage, player_value FROM fifa WHERE club = '{value}' ORDER BY overall DESC", session.bind)
    df = pd.read_sql_query(f"SELECT player_name, overall, wage, aggression FROM fifa WHERE club = '{value}' ORDER BY overall DESC", db.session.bind)
    club = []
    for index, row in df.iterrows():
        t = {'player_name':row['player_name'], 'overall':row['overall'], 
        'wage':row['wage'], 'aggression':row['aggression']}
        club.append(t)
    return jsonify(club)

@app.route("/names/player/<value>")
def theplayer(value):
    df = pd.read_sql_query(f"SELECT player_name, overall, wage, aggression, nationality FROM fifa WHERE player_name = '{value}'", db.session.bind)
    p = {
        'player_name':df.player_name.values.tolist(),
        'overall':df.overall.values.tolist(),
        'aggression':df.aggression.values.tolist(),
        'wage':df.wage.values.tolist(),
        'nationality': df.nationality.values.tolist()
    }
    return jsonify(p)



if __name__ == "__main__":
    app.run()
