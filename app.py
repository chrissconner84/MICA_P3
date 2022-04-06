from flask import Flask, render_template, redirect, jsonify, url_for

from sqlalchemy import create_engine
from config import db_password, db_user, db_name, endpoint
from flask_pymongo import PyMongo
import pandas as pd
import json, os
import scrape_youtube
import plotly.express as px

app = Flask(__name__)

connection_string = f"postgresql://{db_user}:{db_password}@{endpoint}:5432/{db_name}"
engine = create_engine(connection_string)
all_df = pd.read_sql("Select * from all_data limit 10", con=engine)
# usa_df= pd.read_sql("Select * from us_data", con=engine)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_youtube"
mongo = PyMongo(app)
# test_dict={"key","value"}
@app.route("/")
def index():
        countries=engine.execute("SELECT DISTINCT COUNTRY FROM all_data")
        cat_codes=engine.execute("SELECT DISTINCT CAT_CODES FROM all_data")
        all_countries = [row.country for row in countries]
        all_cat_codes = [row.cat_codes for row in cat_codes]
        all_countries_df=pd.DataFrame(all_countries)
        all_cat_df=pd.DataFrame(all_cat_codes)
        rets=(all_countries_df.to_json(orient='records'))
        ccodes=(all_cat_df.to_json(orient='records'))
        # trending_videos=scrape_youtube.scrape();
        trending_videos = mongo.db.trending_videos.find_one();
        #print(trending_videos)
        if not trending_videos:
          #print(os.getcwd())
          with open("trending_videos.json", 'r', encoding='UTF-8') as f:
            trending_videos= json.load(f)
            print(trending_videos)        
        return render_template("index.html",countries=all_countries,all_cat_codes=all_cat_codes,rets=rets,ccodes=ccodes,trending_videos=trending_videos)
 
@app.route("/world_map")
def worldmap():
        countries=engine.execute("SELECT DISTINCT COUNTRY FROM all_data")
        all_countries = [row.country for row in countries]
        all_countries_df=pd.DataFrame(all_countries)
        rets=(all_countries_df.to_json(orient='records'))
        return render_template("world_map.html", countries=all_countries,rets=rets)
        
@app.route("/user_eng")
def user():
      
       return render_template("user_eng.html")

@app.route("/testing")
def testing():
        #Run query
        countries_likes_dislikes_view_count=engine.execute("SELECT COUNTRY, LIKES, DISLIKES, VIEW_COUNT FROM all_data limit 100")
        countries_likes_dislikes_view_count_df=pd.DataFrame(countries_likes_dislikes_view_count,columns=countries_likes_dislikes_view_count.keys())
        countries_likes_dislikes_view_count_json=countries_likes_dislikes_view_count_df.to_dict(orient="records")
        
        jsonStr = json.dumps(countries_likes_dislikes_view_count_json)
        #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

        print(countries_likes_dislikes_view_count_df)
        return  jsonStr


@app.route("/api/all_data")
def get_all():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]
    all_df = pd.read_sql("Select * from all_data limit 10", con=engine)
    res = [{k:v for k, v in row.items()} for i, row in all_df.iterrows()]
    return jsonify(response=res)

#@app.route("/api/us_data")
#def get_us():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]

#    res = [{k:v for k, v in row.items()} for i, row in df.iterrows()]
#    return jsonify(response=res)

@app.route("/api/country")
def get_country():
    # [{},{},{}]
    # {k:v,k:v} -> [[k,v],[k,v],[k,v]]
 #   country_count=engine.execute("select count(country) from all_data where country='Japan'").scalar()
     first_10=engine.execute("select country,video_id from all_data limit 10").all()
     df=pd.DataFrame(first_10)
     print(df)
    # return jsonify({"first":first})
     return (df.to_json(orient="records"))
    # df = pd.read_sql("Select * from all_data", con=engine)
  #  print(country_count)
        # return jsonify(response=list(df['country'].unique()))
@app.route("/api/countries")
def get_countries():
    countries=engine.execute("SELECT DISTINCT COUNTRY FROM all_data")
    all_countries = [row.country for row in countries]
    all_countries_df=pd.DataFrame(all_countries)
    print(all_countries_df)
    return(all_countries_df.to_json(orient='records'))
    # json=jsonify({"countries":all_countries})
    #return countries_json

@app.route("/scrape")

def scraper():
  #Get the videos by calling the scrape function
    trending_videos_data = scrape_youtube.scrape()
    #Get access to trending videos table on mongo db
    trending_videos = mongo.db.trending_videos
    #Update the table and save to data base
    trending_videos.update_one({}, {"$set": trending_videos_data}, upsert=True)
    #print(trending_videos_data["trends"][0])
    # reload the root route
    return redirect("/", code=302)

@app.route("/wm_fill")
def country_numbers():
        #Run query
        countries_geo_data=engine.execute("select * from country_geo")
        countries_geo_df=pd.DataFrame( countries_geo_data,columns= countries_geo_data.keys())
        countries_geo_json=countries_geo_df.to_dict(orient="records")
        countries_geo_json_jsonStr = json.dumps(countries_geo_json)
        # countries_numbers=engine.execute("select country, count(country),sum(view_count), sum(likes), sum(dislikes) from all_data group by country")
        # countries_numbers_df=pd.DataFrame( countries_numbers,columns= countries_numbers.keys())
        # countries_numbers_json=countries_numbers_df.to_dict(orient="records")
        
        # countries_numbers_jsonStr = json.dumps(countries_numbers_json)
        #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

        print(countries_geo_json_jsonStr)
        return  countries_geo_json_jsonStr

@app.route("/cat_code")
def cat_code():
        #Run query
         cat_code=engine.execute("SELECT * from cat_code_ag")
         cat_code_df=pd.DataFrame(cat_code,columns=cat_code.keys())
         cat_code_json=cat_code_df.to_dict(orient="records")
        
         cat_code_jsonStr = json.dumps(cat_code_json)
         #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

         print(cat_code_df)
         return  cat_code_jsonStr

@app.route("/country")
def country():
        #Run query
         country=engine.execute("SELECT * from country_ag")
         country_df=pd.DataFrame(country,columns=country.keys())
         country_json=country_df.to_dict(orient="records")
        
         country_jsonStr = json.dumps(country_json)
         #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

         print(country_df)
         return  country_jsonStr

@app.route("/top_videos")
def top_video():
        #Run query
         tvs=engine.execute("SELECT * from unique_videos_df")
         tvs_df=pd.DataFrame(tvs,columns=tvs.keys())
         tvs_json=tvs_df.to_dict(orient="records")
         tvs_jsonStr = json.dumps(tvs_json)
         #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

         return  tvs_jsonStr

@app.route("/top_channels")         
def top_channels():
        #Run query
         tcs=engine.execute("SELECT * from channel_cat")
         tcs_df=pd.DataFrame(tcs,columns=tcs.keys())
         tcs_json=tcs_df.to_dict(orient="records")
         tcs_jsonStr = json.dumps(tcs_json)
         #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

         return  tcs_jsonStr

@app.route("/mj")
def MJ_top_channels():
        #Run query
        mj_top_channels=engine.execute("select * from mj_top_channels") 
        mj_top_channels_df=pd.DataFrame(mj_top_channels,columns=mj_top_channels.keys())
        mj_top_channels_json=mj_top_channels_df.to_dict(orient="records")
        top_channels_jsonStr = json.dumps(mj_top_channels_json)
        #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]
        return  top_channels_jsonStr
@app.route("/mj2")
def MJ_top_channels_group_by_catcodes():
        #Run query
        mj_top_channels2=engine.execute("select * from grouped_cat") 
        mj_top_channels2_df=pd.DataFrame(mj_top_channels2,columns=mj_top_channels2.keys())
        mj_top_channels2_json=mj_top_channels2_df.to_dict(orient="records")
        top_channels2_jsonStr = json.dumps(mj_top_channels2_json)
        #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]
        return  top_channels2_jsonStr

if __name__ == "__main__":
    app.run(debug=True)
