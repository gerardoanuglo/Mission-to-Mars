#import dependencies
from flask import Flask, render_template, redirect, url_for
from scrape_mars import scrape_all
from flask_pymongo import PyMongo

#create an app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#create main route that renders html file
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


#create route that will import scrape_mars.py script and call scrape function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run()
