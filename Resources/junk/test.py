from flask import Flask, render_template, redirect, jsonify, url_for
from sqlalchemy import create_engine
from config import db_password, db_user, db_name, endpoint
import pandas as pd



app = Flask(__name__)

connection_string = f"postgresql://{db_user}:{db_password}@{endpoint}:5432/{db_name}"
engine = create_engine(connection_string)
df = pd.read_sql("Select * from all_data", con=engine)

@app.route("/")
def index():
    # dictionary = mongo.db.dictionary.find_one()
    # return render_template("index.html", dictionary=dictionary)
    return render_template('test.html')
@app.route("/user")
def user():
    
    return render_template('user_eng.html')

@app.route("/worldmap")
def world_map():
   
    return render_template('world_map.html')

@app.route("/api/all_data")
def get_all():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]
    res = [{k:v for k, v in row.items()} for i, row in df.iterrows()]
    return jsonify(response=res)

@app.route("/api/country")
def get_country():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]

    return jsonify(response=list(df['country'].unique()))


if __name__ == "__main__":
    app.run(debug=True)