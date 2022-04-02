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
all_data = engine.execute("SELECT * FROM all_data")
all_data_df = pd.DataFrame(all_data, columns=all_data._metadata.keys)


all_data_df['likes_ratio'] = all_data_df['likes'] / all_data_df['view_count']
all_data_df['dislikes_ratio'] = all_data_df['dislikes'] / all_data_df['view_count']
all_data_df['comments_ratio'] = all_data_df['comment_count'] / all_data_df['view_count']
all_data_df['engagement_score'] = (all_data_df['likes'] + all_data_df['dislikes'] + all_data_df['comment_count'])/ all_data_df['view_count']
all_data_df = all_data_df.drop_duplicates(subset = 'video_id', keep = 'last')
cat_codes_likes_agg = round(all_data_df.groupby('country').mean(),2)

# cat_codes_likes_agg = all_data_df.groupby("cat_codes").count()



"""
Routes used to send data to d3.json; make sure to send as json format

Also you can use pd.to_json() instead of JSONify but it's not as easy to use with plotly
"""


@app.route("/")
def index():
    # dictionary = mongo.db.dictionary.find_one()
    # return render_template("index.html", dictionary=dictionary)
    return render_template('test_mj.html')


@app.route("/scrape")
def scraper():
    dictionary = mongo.db.dictionary
    dictionary_data = scrape_youtube.scrape()
    dictionary.update_one({}, {"$set": dictionary_data}, upsert=True)
    return redirect("/", code=302)


@app.route("/api/test")
def plotly_test():
    res = [{k:v for k, v in row.items()} for i, row in value_counts_df.iterrows()]
    return jsonify(response=res)

# Returns [{}, {},]
@app.route("/api/cat_codes_likes_agg")
def cat_codes_agg_route():
    res = [{k:v for k, v in row.items()} for i, row in cat_codes_likes_agg.iterrows()]
    return jsonify(response=res)

# Returns ["Canada", .....]
@app.route("/api/country")
def get_country():
    return jsonify(response=list(all_data_df['country'].unique()))


if __name__ == "__main__":
    app.run(debug=True)
