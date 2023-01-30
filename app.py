#import dependencies
from flask import Flask, render_template, redirect, url_for
import scrape_mars
from flask_pymongo import PyMongo

#create an app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#create main route that renders html file
@app.route("/")
def index():
    mars_ap = mongo.db.mars_co.find_one()
    return render_template("index.html", mars_html=mars_ap)

#create route that will import scrape_mars.py script and call scrape function
@app.route("/scrape")
def scrape():
    mars_ap = mongo.db.mars_co
    mars_data = scrape_mars.scrape_all()
    mars_ap.insert_one(mars_data)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()
