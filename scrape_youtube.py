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
    results = soup.find_all('a', class_='yt-simple-endpoint style-scope ytd-video-renderer')
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
    browser.quit()
    return(trends_dictionary)
