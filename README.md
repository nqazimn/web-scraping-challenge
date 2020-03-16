# web-scraping-challenge
This is a mock project built to practice web-scraping using Python Beautiful Soup in connection with MongoDB.

<p align="center">
  <img src="/mission_to_mars/screenshots/screen_capture3.PNG">
</p>

## Background

The main goal is to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

## Prerequisites
You should have the following python packages installed in your Python environment to run the included jupyter notebooks:-
```
flask, flask_pymongo (installed by-default in a Python installation)
pandas
time
requests
BeautifulSoup
re
```

## File Layout

1. The project tasks are divided into multiple sub-tasks, each with its own function call. The functions are defined in ```scrape_mars.py```. The following details some of the basics of the code:-
* Scrape **latest news** about Mars from NASA website - ```scrape_nasa()```
* Scrape the **latest featured image** from JPL website - ```scrape_jpl()```
* Scrape the **latest weather report** from twitter - ```scrape_twitter()```
* Scrape **facts and figures** from space-facts.com - ```scrape_space_facts()```
* Scrape **high-resolution images** from astrogeology.com - ```scrape_astrogeology()```

2. The code for the above functions was individually tested in a Jupyter notebook, ```mission_to_mars_scraper.ipynb```.

3. The flask app used to serve the scraped results and the call the main ```scraper()``` function is included in ```app.py```.

4. The screenshots of the app presented as a HTML page are included in _/mission_to_mars/screenshots/_.
