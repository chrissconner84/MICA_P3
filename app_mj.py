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



"""
Create dataframes here; only runs when Flask starts or resets
"""

raw_value_counts = engine.execute("""
                        Select country, count(*) 
                        from all_data
                        group by country""", con=engine)
value_counts_df = pd.DataFrame(raw_value_counts, columns = raw_value_counts._metadata.keys)

# You can use test_all_df like main_df in jpytr; feel free to rename
test_all = engine.execute("SELECT * FROM all_data")
test_all_df = pd.DataFrame(test_all, columns=test_all._metadata.keys)

test_avg_view = test_all_df.groupby("country").mean()

"""
Routes used to send data to d3.json; make sure to send as json format

Also you can use pd.to_json() instead of JSONify but it's not as easy to use with plotly
"""

@app.route("/")
def index():
    # dictionary = mongo.db.dictionary.find_one()
    # return render_template("index.html", dictionary=dictionary)
    return render_template('test.html')

@app.route("/scrape")
def scraper():
    dictionary = mongo.db.dictionary
    dictionary_data = scrape_youtube.scrape()
    dictionary.update_one({}, {"$set": dictionary_data}, upsert=True)
    return redirect("/", code=302)

@app.route("/api/test")
def get_all():
    res = [{k:v for k, v in row.items()} for i, row in value_counts_df.iterrows()]
    return jsonify(response=res)

# Returns [{}, {},]
@app.route("/api/test_avg_view")
def test_avg_view_route():
    res = [{k:v for k, v in row.items()} for i, row in test_avg_view.iterrows()]
    return jsonify(response=res)

# Returns ["Canada", .....]
@app.route("/api/country")
def get_country():
    return jsonify(response=list(test_all_df['country'].unique()))


if __name__ == "__main__":
    app.run(debug=True)
