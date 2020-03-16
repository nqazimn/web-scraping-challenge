from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars_app"
# mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")


@app.route("/")
def index():
    # return "Welcome"
    listings = mongo.db.mission_to_mars_app.find_one()
    # print(listings)
    # team_list = ["test1", "test2", "test3"]
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    # print("Testing...")
    # return "Welcome to 'Mission to Mars' page!"
    listings = mongo.db.mission_to_mars_app
    mars_data = scrape_mars.scrape()
    listings.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
