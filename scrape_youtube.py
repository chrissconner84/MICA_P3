#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import time
# sys.path.append('../../')
# Import API key
# from api_keys import g_key

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    country_code="US"

    #request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,chart=mostPopular&regionCode={country_code}&maxResults=50&key={g_key}"
    #
    request_url="https://www.youtube.com/feed/trending"

    browser.visit(request_url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a', class_='ytd-video-renderer')
    relative_video=[]
    relative_title=[]
    len(results)
    i=0
    j=0
    trends_dictionary={}
    trends = []
    titles=[]
    summaries=[]
    video_links=[]
    for article in results:
        title=article.get("title")
        summary=article.get('aria-label')
        video_link="http://youtube.com"+article.get("href")
        if ((title is not None) and (summary is not None) and (article.get("href")  is not None)):

            titles.append(article.get("title"))
            summaries.append(article.get('aria-label'))
            video_links.append("http://youtube.com"+article.get("href"))
            trends.append({"title":article.text,"summary":article.get('aria-label'),"video_link":"http://youtube.com"+article.get("href")})
            # print(f"{i} ytd: article: {article} len: {len(article)}")
            # print(f"article.href:{article.get('href')}")
            # print(f"article.aria-label:{article.get('aria-label')}")
            # print(f"href={article.find('a',id_='video-title')}")
    trends_dictionary.update({"trends":trends})
    return(trends_dictionary)

# url = 'https://spaceimages-mars.com'
# browser.visit(url)
# time.sleep(1)


# html = browser.html
# soup = BeautifulSoup(html, 'html.parser')


# #find the featured image 
# results = soup.find('img', class_='headerimage')["src"]

# featured_image_title = soup.find('h1', class_='media_feature_title').text
# featured_image_url=url+'/' + results



# url = 'https://galaxyfacts-mars.com'
# browser.visit(url)


# html = browser.html
# soup = BeautifulSoup(html, 'html.parser')



# results = soup.find('table', class_='table-striped')
# print(str(results)[0])
# # string="""
# # html_string = string + results + string

# # from IPython.display import display_html
# # display_html(html_string, raw=True)
# Mars_facts_df = pd.read_html(str(results))[0]
# Mars_facts_df.rename(columns={0:"Mars Facts", 1: "Values"}, inplace=True)
# Mars_facts_html=Mars_facts_df.to_html()
# Mars_fact_html_file='Mars_facts.html'
# with open(Mars_fact_html_file, 'a') as f:
#     f.write(Mars_facts_html)
    
# url = 'https://marshemispheres.com/'
# browser.visit(url)
# time.sleep(1)


# html = browser.html
# soup = BeautifulSoup(html, 'html.parser')



# results = soup.find_all('div', class_='item')
# relative_img=[]
# for article in results:
#     # Use Beautiful Soup's find() method to navigate and retrieve attributes
#     relative_img.append(url+article.find('a')['href'])

# hemisphere_image_urls = []
# img_url=[]
# title=[]

# for link in relative_img:
#     browser.visit(link)
#     time.sleep(1)


#     html = browser.html
#     soup = BeautifulSoup(html, 'html.parser')

#     string= (soup.find_all('li')[0])
#     local=soup.find('h2', class_='title').text.rsplit(' ', 1)[0]
#     local_url=link.rsplit('/',1)[0] + '/'+string.find("a")['href']
#     title.append(local)
#     img_url.append(local_url)
#     hemisphere_image_urls.append({"title":local, "img_url":local_url})

# browser.quit()
# dictionary={}

# dictionary.update({"news":news})
# dictionary.update({"featured_image_title":featured_image_title})
# dictionary.update({"featured_image_url":featured_image_url})
# dictionary.update({"table_html_file":Mars_fact_html_file})
# dictionary.update({"table_html":Mars_facts_html.strip()})

# dictionary.update({"hemisphere_image_urls":hemisphere_image_urls})
# return(dictionary)