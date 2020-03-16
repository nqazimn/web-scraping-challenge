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

    browser.quit()
    # sanity-check
    # browser.visit(featured_image_url)

    return featured_image_url


def scrape_twitter():
    '''
    Scrapes twitter and returns latest weather report
    '''
    response = requests.get(url=url_dict["Twitter"])

    # Wait for 20 sec while the page loads
    time.sleep(20)

    soup = bs(response.text, "html.parser")

    # using re: Regular Expression matching (source:https://docs.python.org/3/library/re.html)
    # since the weather reports always start with 'Insight sol' on the Twitter page

    weather_reports = soup(text=re.compile(r'InSight sol'))

    try:
        # only select the latest weather report
        mars_weather = str(weather_reports[0])

        # Manipulate the string to return desired format
        mars_weather = mars_weather[8:].capitalize().replace("\n", "; ")

    except:
        mars_weather = "N/A"
        print("Weather Report not available.")

    return mars_weather


def scrape_space_facts():
    '''
    Scrapes space-facts.com for facts about Mars and 
    returns a table in HTML format
    '''
    tables = pd.read_html(url_dict["space-facts"])

    # sleep for 10 sec while the page loads
    time.sleep(10)

    mars_table = tables[0]

    try:
        mars_table = mars_table.rename(columns={0: 'Parameter', 1: "Value"})
        mars_table = mars_table.set_index('Parameter')
    except:
        print('Columns already renamed')

    mars_table_html = mars_table.to_html()

    return mars_table_html


def scrape_astrogeology():
    '''
    Scrape astrogeology.com to extract high-res images 
    of Mars's hemispheres. Using splinter in conjunction with BeautifulSoup
    '''
    browser = Browser('chrome', headless=False)
    browser.visit(url_dict["astrogeology"])

    time.sleep(10)

    html = browser.html
    soup = bs(html, 'html.parser')

    items = soup.find_all("div", class_="item")

    mars_hemisphere_image_urls = []

    for item in items:
        full_url = url_dict['astrogeology'].split('/search')[0]+item.a['href']

        browser.visit(full_url)

        html = browser.html
        soup = bs(html, 'html.parser')

        image_url = soup.find("div", class_="downloads")

        mars_hemisphere_image_urls.append({"title": item.h3.text.split(' Enhanced')[0],
                                           "img_url": image_url.li.a['href']})

    browser.quit()

    return mars_hemisphere_image_urls


def scrape():

    news = scrape_nasa()
    print('LOG: News scraped.')

    url_to_featured_image = scrape_jpl()
    print('LOG: Featured image scraped.')

    weather = scrape_twitter()
    print('LOG: Weather scraped.')

    data_table = scrape_space_facts()
    print('LOG: Data table scraped.')

    url_to_hemisphere_images = scrape_astrogeology()
    print('LOG: Hemisphere images scraped')

    dict_of_scraped_stuff = {'news': news[0],
                             'url_to_featured_image': url_to_featured_image,
                             'weather': weather,
                             'data_table': data_table,
                             'url_to_hemisphere_images': url_to_hemisphere_images}

    return dict_of_scraped_stuff
