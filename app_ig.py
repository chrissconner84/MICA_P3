from flask import Flask, render_template, redirect, jsonify, url_for

from sqlalchemy import create_engine
from config import db_password, db_user, db_name, endpoint
import pandas as pd
import json
import scrape_youtube
from flask import g

app = Flask(__name__)

connection_string = f"postgresql://{db_user}:{db_password}@{endpoint}:5432/{db_name}"
engine = create_engine(connection_string)
all_df = pd.read_sql("Select * from all_data limit 10", con=engine)

# usa_df= pd.read_sql("Select * from us_data", con=engine)
test_dict={"key","value"}

@app.route("/")
def index():
        countries=engine.execute("SELECT DISTINCT COUNTRY FROM all_data")
        cat_codes=engine.execute("SELECT DISTINCT CAT_CODES FROM all_data")
        all_countries = [row.country for row in countries]
        all_cat_codes = [row.cat_codes for row in cat_codes]
        all_countries_df=pd.DataFrame(all_countries)
        all_cat_df=pd.DataFrame(all_cat_codes)
        trending_videos={
  "trends": [
    {
      "summary": "All Sports Golf Battle at The Masters by Dude Perfect 13 hours ago 11 minutes, 18 seconds 2,444,072 views", 
      "title": "\n\nAll Sports Golf Battle at The Masters\n", 
      "video_link": "http://youtube.com/watch?v=heIKaaamvdc"
    }, 
    {
      "summary": "Harry Styles - As It Was (Official Video) by Harry Styles 2 days ago 2 minutes, 46 seconds 25,955,970 views", 
      "title": "\n\nHarry Styles - As It Was (Official Video)\n", 
      "video_link": "http://youtube.com/watch?v=H5v3kku4y6Q"
    }, 
    {
      "summary": "Anuel AA, Yailin la M\u00e1s Viral - Si Tu Me Busca (Video Oficial) by Anuel AA 2 days ago 4 minutes, 32 seconds 9,252,304 views", 
      "title": "\n\nAnuel AA, Yailin la M\u00e1s Viral - Si Tu Me Busca (Video Oficial)\n", 
      "video_link": "http://youtube.com/watch?v=Pc2Hl2w_7qM"
    }, 
    {
      "summary": "Our Ancient Street Cat Passed Away by Safiya Nygaard 9 hours ago 20 minutes 777,236 views", 
      "title": "\n\nOur Ancient Street Cat Passed Away\n", 
      "video_link": "http://youtube.com/watch?v=Zad6v8ZHzdg"
    }, 
    {
      "summary": "Tommy Davidson had run-in with Will Smith by FOX 5 New York 1 day ago 4 minutes, 22 seconds 1,072,097 views", 
      "title": "\n\nTommy Davidson had run-in with Will Smith\n", 
      "video_link": "http://youtube.com/watch?v=undSilfB3AQ"
    }, 
    {
      "summary": "$150,000 Funniest Survival Games... by TommyInnit 1 day ago 20 minutes 1,586,147 views", 
      "title": "\n\n$150,000 Funniest Survival Games...\n", 
      "video_link": "http://youtube.com/watch?v=s9FqnrJnmDQ"
    }, 
    {
      "summary": "NBA YoungBoy - 4KT BABY by YoungBoy Never Broke Again 1 day ago 2 minutes, 11 seconds 2,238,951 views", 
      "title": "\n\nNBA YoungBoy - 4KT BABY\n", 
      "video_link": "http://youtube.com/watch?v=1KbxOjnmvjI"
    }
   ]};
        rets=(all_countries_df.to_json(orient='records'))
        ccodes=(all_cat_df.to_json(orient='records'))
        return render_template("index.html",countries=all_countries,all_cat_codes=all_cat_codes,rets=rets,ccodes=ccodes, trending_videos=trending_videos)
 
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
        # countries=engine.execute("SELECT count(COUNTRY) FROM all_data")
        # all_countries = [row.country for row in countries]
        # all_countries_df=pd.DataFrame(all_countries)
        # rets={"country": all_countries for country in all_countries}
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
    trending_videos = scrape_youtube.scrape()
    #dictionary.update_one({}, {"$set": dictionary_data}, upsert=True)
    print(trending_videos["trends"][0])
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
