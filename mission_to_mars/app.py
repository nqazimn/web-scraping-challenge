from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Set-up connection to database
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")


@app.route("/")
def index():
    listings = mongo.db.mission_to_mars_app.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.mission_to_mars_app
    mars_data = scrape_mars.scrape()
    listings.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
