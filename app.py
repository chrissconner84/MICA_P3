from flask import Flask, render_template, redirect, jsonify, url_for, request
import config
import flask
from sqlalchemy import create_engine
from config import db_password, db_user, db_name, endpoint #gkey
#from flask_pymongo import PyMongo
import pandas as pd
import json, os
#import scrape_youtube
import plotly.express as px
import plotly
import joblib
import requests
import tensorflow as tf
import keras
from keras.models import load_model
import numpy as np
import urllib.request
import os
from os import environ


nn_model = load_model('model_nn.h5')
print ('NN Model loaded')


app = Flask(__name__)

connection_string = f"postgresql://{db_user}:{db_password}@{endpoint}:5432/{db_name}"
engine = create_engine(connection_string)
all_df = pd.read_sql("Select * from all_data limit 10", con=engine)
# usa_df= pd.read_sql("Select * from us_data", con=engine)
# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_youtube"
# mongo = PyMongo(app)
# test_dict={"key","value"}

@app.route("/")
def index():
        # countries=engine.execute("SELECT DISTINCT COUNTRY FROM all_data")
        # cat_codes=engine.execute("SELECT DISTINCT CAT_CODES FROM all_data")
        # all_countries = [row.country for row in countries]
        # all_cat_codes = [row.cat_codes for row in cat_codes]
        # all_countries_df=pd.DataFrame(all_countries)
        # all_cat_df=pd.DataFrame(all_cat_codes)
        # rets=(all_countries_df.to_json(orient='records'))
        # ccodes=(all_cat_df.to_json(orient='records'))
        # trending_videos=scrape_youtube.scrape();
        #trending_videos = mongo.db.trending_videos.find_one();
        #print(trending_videos)
        #if not trending_videos:
          #print(os.getcwd())
        #base_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&maxResults=20&key="+gkey
        # run a request using our params dictionary
        #response = requests.get(base_url)
        # print the response url, avoid doing for public github repos in order to avoid exposing key
        #print(response.url)
        # convert response to json
        #trending_videos = response.json()

        #with open("trending_videos.json", 'r', encoding='UTF-8') as f:
        #         trending_videos= json.load(f)
            #print(trending_videos)
        
               
        #return render_template("index.html",countries=all_countries,all_cat_codes=all_cat_codes,rets=rets,ccodes=ccodes,trending_videos=trending_videos)
        return render_template("index.html")
@app.route("/mike_page2")
def mikepage2():
      return render_template("mike_page2.html")
#    #START OF GRAPH 1
#    unique_data_grouped_country = pd.read_sql('SELECT country, AVG(view_count) AS avg_view_count, AVG(likes_ratio) AS avg_likes_ratio, AVG(comments_ratio) AS avg_comments_ratio, AVG(engagement_score) AS avg_engagment_score FROM unique_data GROUP BY country;', con = engine)
#    #country_ag = pd.read_sql("SELECT * FROM country_ag", con = engine)
#    #country_ag_df = country_ag['view_count'].median()
#    fig1 = px.bar(unique_data_grouped_country,
#           x = 'country',
#           y = 'avg_view_count',
#           color = 'country',
#           labels={'country':'Country', 'avg_view_count':'Avg Views Amount of Views on Final Trending Date'},
#           title="Avg Views By Country",
#           text_auto = True)
#    fig1.update_layout(title_x = 0.5)     

#    #START OF GRAPH 2
#    #country_ag2 = pd.read_sql("SELECT * FROM country_ag", con = engine)
#    #country_ag2 = unique_data.groupby('country')['likes_ratio'].median().reset_index()
#    fig2 = px.bar(unique_data_grouped_country,
#            x = 'country', 
#            y = 'avg_likes_ratio',
#            color = 'country',
#            labels={'country':'Country', 'avg_likes_ratio':'Percentage of Likes per View (%)'},
#            title="Avg Likes By Country",
#            text_auto = True)
#         #    height = 700)
#    fig2.update_layout(title_x = 0.5) 
# #    fig2 = px.bar(country_ag2,
# #        x = country_ag2['country'],
# #        y = country_ag2['likes_ratio'],
# #        color = 'country',
# #        labels={'country':'Country',
# #                      'likes_ratio':'Likes Ratio (%)'}
# #        )
#    #START OF GRAPH 3      
#    fig3 = px.bar(unique_data_grouped_country, 
#        x = 'country', 
#        y = 'avg_comments_ratio',
#        color = 'country',
#        labels={'country':'Country', 'avg_comments_ratio':'Percentage of Comments per View (%)'},
#        title = 'Avg Comments by View',
#        text_auto = True)
#    fig3.update_layout(title_x = 0.5)
#      graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
#      graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
#      graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

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

@app.route("/nn_model",methods=['GET', 'POST'])
def nnmodel():
    if request.method == 'POST':
        print(request)
        # Need to add ssome checking of arguments
        category_e = request.form['category_e']
        publish_to_trend = request.form['publish_to_trend']
        publish_day_num = request.form['publish_day_num']
        pt_views = request.form['pt_views']
        pt_likes = request.form['pt_likes']
        pt_dislikes = request.form['pt_dislikes']
        pt_comments = request.form['pt_comments']
        try:
            data=[[int(category_e), int(publish_to_trend), int(publish_day_num), int(pt_views), int(pt_likes),int(pt_dislikes), int(pt_comments)]]
        except ValueError:
            return render_template ('nn_model.html', pred=str("N/A [Incorrect Parameters, Please resubmit the form]"))
#        data=[[int(category_e), int(publish_to_trend), 0,0 ,0,0,0,0,0]]
        scaler = joblib.load('./scaler_nn.pkl')
#        load the columns usinf pickle format
        columns = joblib.load ('./model_columns_nn.pkl')
#  This line will fill any missing column with a 0.  Care should be taken that
# won't affect your output
        x=pd.DataFrame(data)
        x.columns = [columns]
        print(x)
        test_input_scaled = scaler.transform(x)
        test_target_hat=nn_model.predict(test_input_scaled)
        test_target_hat[test_target_hat > 0.5] = 1
        test_target_hat[test_target_hat <= 0.5] = 0
        if test_target_hat== 1:
            prediction ='It will trend for 4 or more days'
        else:
            prediction ='It will trend for less than 4 days'           
        return render_template("nn_model.html", pred=prediction)
        # return render_template('nn_model.html', pred=str(test_target_hat))
    return render_template('nn_model.html')

@app.route("/mike_model")
def mikemodel():
      
       return render_template("mike_model.html")

@app.route("/abby_model")
def abbymodel():
      
       return render_template("abby_model.html")       

@app.route("/testing")
def testing():
        #Run query
        countries_likes_dislikes_view_count=engine.execute("SELECT COUNTRY, LIKES, DISLIKES, VIEW_COUNT FROM all_data limit 100")
        countries_likes_dislikes_view_count_df=pd.DataFrame(countries_likes_dislikes_view_count,columns=countries_likes_dislikes_view_count.keys())
        countries_likes_dislikes_view_count_json=countries_likes_dislikes_view_count_df.to_dict(orient="records")
        
        jsonStr = json.dumps(countries_likes_dislikes_view_count_json)
        #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]

        #print(countries_likes_dislikes_view_count_df)
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

        #print(countries_geo_json_jsonStr)
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

@app.route("/dash")
def dash_app():
        #Run query
        channels_grouped = pd.read_sql("select channeltitle, cat_codes, count(trending_date) from all_data group by channeltitle, cat_codes order by count(channeltitle) DESC", con = engine)
        fig = px.bar(channels_grouped,
             x = channels_grouped['channeltitle'][0:100],
             y = channels_grouped['count'][0:100],
             color = channels_grouped['cat_codes'][0:100],
             labels = {'x': 'Channel Title',
                      'y': 'Total Trending Days'},
             title = 'Top YouTube Channels by Total Trending Days',
             text_auto = True)
             
        fig.write_html('./templates/channels_pretty.html')
        # channels_grouped_df=pd.DataFrame(channels_grouped,columns=mj_top_channels2.keys())
        # channels_grouped_json=channels_grouped_df.to_dict(orient="records")
        # channels_grouped_jsonStr = json.dumps(channels_grouped_json)
        #res = [{k:v for k, v in row.items()} for i, row in countries_likes_dislikes_view_count_df.iterrows()]
        return render_template('channels_pretty.html')


@app.route("/notdash")
def notdash():
   #Top Chart on notdash.html   
   channels_grouped = pd.read_sql("select channeltitle, cat_codes, count(trending_date) from all_data group by channeltitle, cat_codes order by count(channeltitle) DESC", con = engine)
   channels_grouped_df=pd.DataFrame(channels_grouped)
   fig = px.bar(channels_grouped,
             x = channels_grouped['channeltitle'][0:50],
             y = channels_grouped['count'][0:50],
             color = channels_grouped['cat_codes'][0:50],
             labels = {'x': 'Channel Title',
                      'y': 'Total Trending Days',
                      'color':'Category'},
             title = 'Top YouTube Channels by Total Trending Days',
             text_auto = True,
             height = 700
                        )
   fig.update_layout(xaxis_categoryorder = 'total descending')
   fig.update_layout(title_x = 0.5)
   #Bottom Chart on notdash.html
   categories_grouped = pd.read_sql("select cat_codes, count(trending_date) from all_data group by cat_codes order by count(channeltitle) DESC", con = engine)
   fig.update_layout(
    yaxis = dict(
    tickfont = dict(size=20)))
   
   fig1 = px.bar(categories_grouped,
             x = 'cat_codes',
             y = 'count',
             #color = all_data[]
             labels = {'cat_codes': 'Category Title',
                      'count': 'Total Trending Days'},
             title = 'Top YouTube Categories by Total Trending Days',
             text_auto = True)
   fig1.update_layout(title_x = 0.5)           
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON, graphJSON1=graphJSON1)
#      return render_template('notdash.html', graphJSON=graphJSON)   

@app.route("/user_eng2")
def user_eng2():
      
   #START OF GRAPH 1
   unique_data_grouped_country = pd.read_sql('SELECT country, AVG(view_count) AS avg_view_count, AVG(likes_ratio) AS avg_likes_ratio, AVG(comments_ratio) AS avg_comments_ratio, AVG(engagement_score) AS avg_engagment_score FROM unique_data GROUP BY country;', con = engine)
   #country_ag = pd.read_sql("SELECT * FROM country_ag", con = engine)
   #country_ag_df = country_ag['view_count'].median()
   fig1 = px.bar(unique_data_grouped_country,
          x = 'country',
          y = 'avg_view_count',
          color = 'country',
          labels={'country':'Country', 'avg_view_count':'Avg Views Amount of Views on Final Trending Date'},
          title="Avg Views By Country",
          text_auto = True)
   fig1.update_layout(title_x = 0.5)     

   #START OF GRAPH 2
   #country_ag2 = pd.read_sql("SELECT * FROM country_ag", con = engine)
   #country_ag2 = unique_data.groupby('country')['likes_ratio'].median().reset_index()
   fig2 = px.bar(unique_data_grouped_country,
           x = 'country', 
           y = 'avg_likes_ratio',
           color = 'country',
           labels={'country':'Country', 'avg_likes_ratio':'Percentage of Likes per View (%)'},
           title="Avg Likes By Country",
           text_auto = True)
        #    height = 700)
   fig2.update_layout(title_x = 0.5) 
#    fig2 = px.bar(country_ag2,
#        x = country_ag2['country'],
#        y = country_ag2['likes_ratio'],
#        color = 'country',
#        labels={'country':'Country',
#                      'likes_ratio':'Likes Ratio (%)'}
#        )
   #START OF GRAPH 3      
   fig3 = px.bar(unique_data_grouped_country, 
       x = 'country', 
       y = 'avg_comments_ratio',
       color = 'country',
       labels={'country':'Country', 'avg_comments_ratio':'Percentage of Comments per View (%)'},
       title = 'Avg Comments by View',
       text_auto = True)
   fig3.update_layout(title_x = 0.5)
#    country_ag3 = pd.read_sql("SELECT * FROM country_ag", con = engine)
#    fig3 = px.bar(country_ag3,
#        x = country_ag3['country'],
#        y = country_ag3['comment_count'],
#        color = 'country',
#        labels={'country':'Country',
#                      'comment_count':'Comments Ratio(%)'})

   # START of GRAPH 4 
   fig4 = px.bar(unique_data_grouped_country, 
       x = 'country', 
       y = 'avg_engagment_score', 
       color = 'country',
       labels={'country':'Country', 'avg_engagment_score':'Engagement Score: 50% comments / 49% likes / 1% views'},
       title = 'Engagement Score',
       text_auto = True)
   fig4.update_layout(title_x = 0.5)     
#    country_ag4 = pd.read_sql("SELECT * FROM country_ag", con = engine)
#    fig4 = px.bar(country_ag4,
#        x = 'country',
#        y = 'engagement_score',
#        color = 'country',
#        labels ={'country':'Country',
#                      'engagement_score':'Engagement Score (%)'}) 

   graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
   graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
   graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
   graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('user_eng2.html', graphJSON1=graphJSON1,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4)
#      return render_template('notdash.html', graphJSON=graphJSON)   



if __name__ == "__main__":
    app.run(debug=True)
