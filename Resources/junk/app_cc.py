from flask import Flask, render_template, redirect, jsonify, url_for

from sqlalchemy import create_engine
from config import db_password, db_user, db_name, endpoint
import pandas as pd


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
        rets=(all_countries_df.to_json(orient='records'))
        ccodes=(all_cat_df.to_json(orient='records'))
        return render_template("index.html",countries=all_countries,all_cat_codes=all_cat_codes,rets=rets,ccodes=ccodes)
 
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
        countries=engine.execute("SELECT DISTINCT COUNTRY FROM all_data")
        all_countries = [row.country for row in countries]
        all_countries_df=pd.DataFrame(all_countries)
        rets={"country": all_countries for country in all_countries}
        return rets


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

if __name__ == "__main__":
    app.run(debug=True)
