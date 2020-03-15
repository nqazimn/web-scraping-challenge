# Dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import time
import re
import pandas as pd

# Set-up dictionary of all Mars urls to be scraped
url_dict = {"NASA": "https://mars.nasa.gov/news/",
            "JPL": "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars",
            "Twitter": "https://twitter.com/marswxreport?lang=en",
            "space-facts": "https://space-facts.com/mars/",
            "astrogeology": "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"}


def scrape_nasa():
    '''
    Scrapes NASA website for latest Mars
    returns dictionary of lates news 'title' and 'text'
    '''
    response = requests.get(url=url_dict["NASA"])

    # Wait for 20 sec while the page loads
    time.sleep(20)

    soup = bs(response.text, "html.parser")

    # print(soup.prettify())

    results = soup.find_all("div", class_="slide")

    mars_latest_news = []

    for result in results:
        try:
            news_title = result.find("div", class_="content_title").text
            news_description = result.find(
                "div", class_="rollover_description_inner").text

            news_dict = {'title': news_title.strip(),
                         'description': news_description.strip()}

            mars_latest_news.append(news_dict)

        except AttributeError as e:
            print(e)

    return mars_latest_news


def scrape_jpl():
    '''
    Scrapes JPL page for latest featured image for Mars
    Returns url to the high-res image
    '''

    # Initiate the browser and visit JPL page
    browser = Browser('chrome', headless=False)
    browser.visit(url_dict['JPL'])

    # Wait for 20 sec while the page loads
    time.sleep(20)

    # scrape the page
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image = soup.find("li", class_="slide").a['data-fancybox-href']

    # create full-url to high-res image
    featured_image_url = url_dict['JPL'].split(
        '/spaceimages')[0]+featured_image

    # sanity-check
    # browser.visit(featured_image_url)

    return featured_image_url
