from flask import Flask, render_template, redirect, jsonify, url_for
# from flask_pymongo import PyMongo
# import scrape_youtube
# import pymongo
from sqlalchemy import create_engine
from config import db_password, db_user, db_name, endpoint
import pandas as pd


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.

# app.config["MONGO_URI"] = "mongodb://localhost:27017/youtube"
# mongo = PyMongo(app)

connection_string = f"postgresql://{db_user}:{db_password}@{endpoint}:5432/{db_name}"
engine = create_engine(connection_string)
# df = pd.read_sql("Select * from all_data", con=engine)
# usa_df= pd.read_sql("Select * from us_data", con=engine)

@app.route("/")
def index():
    # dictionary = mongo.db.dictionary.find_one()

#    return render_template("index.html", df=df.to_json(orient="records"))
    return render_template('test.html')

@app.route("/scrape")
def scraper():
    dictionary = mongo.db.dictionary
    dictionary_data = scrape_youtube.scrape()
    dictionary.update_one({}, {"$set": dictionary_data}, upsert=True)
    return redirect("/", code=302)

@app.route("/api/all_data")
def get_all():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]
    df = pd.read_sql("Select * from all_data", con=engine)
    res = [{k:v for k, v in row.items()} for i, row in df.iterrows()]
    return jsonify(response=res)

@app.route("/api/us_data")
def get_us():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]

    res = [{k:v for k, v in row.items()} for i, row in df.iterrows()]
    return jsonify(response=res)

@app.route("/api/country")
def get_country():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]
 #   country_count=engine.execute("select count(country) from all_data where country='Japan'").scalar()
    first_10=engine.execute("select country,video_id from all_data limit 10").all()
    df=pd.DataFrame(first_10)
    print(df)
    first = [[row.country, row.video_id] for row in first_10]
    print(first)
    # return jsonify({"first":first})
    return (df.to_json(orient="records"))
    # df = pd.read_sql("Select * from all_data", con=engine)
  #  print(country_count)
 #   return jsonify({"response":country_count})
    # return jsonify(response=list(df['country'].unique()))


if __name__ == "__main__":
    app.run(debug=True)
