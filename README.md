# The Latest News On The Mission To Mars

I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

As a data scientist, web scraping is an integral skill. It's how we access and collect data from the internet, which allows us to extract insights out of the data. The ability to collect and store unstructured data is also very important because in the real world data isn’t always structured. These ideas are the reason why I decided to do this project. 

Information being scraped includes:
- The latest news title and synopsis
- The featured image on this [website](https://spaceimages-mars.com/)
- A table including facts about Mars
- Images of the Mars hemispheres


Before Pressing The Button "Scrape New Data":
<img width="1128" alt="Screenshot_20230130_121516" src="https://user-images.githubusercontent.com/85320743/215621477-5557188a-3f63-4050-aa0a-1c614743b3a7.png">

After:
<img width="1128" alt="Screenshot_20230130_121851" src="https://user-images.githubusercontent.com/85320743/215621510-6ee876d7-2e93-4b18-91c9-8ceab0c2b338.png">

## A Brief Description Of My Process

First I conducted the web scraping in a Jupyter Notebook to validate each step worked correctly and as intended. This included:

- Checking my WebDriver and ChromeDriverManager were working properly. They essentially allowed me to navigate to the site I wanted. 
- Confirming I collected the intended data from each site.
- Confirming I could access my Mongo Database and correctly store data. 

Once I completed this stage of the project I converted the Jupyter Notebook into a python script (file name "scrape_mars.py"). Most importantly I created a function that executed all the scraping code and returned all the scraped data in one Python dictionary. 

Then I created a Flask app (file name "app.py") with a route that essentially imported my python script, called the function mentioned above and stored the data in MongoDB. 

<img width="1061" alt="Screenshot_20230130_122052" src="https://user-images.githubusercontent.com/85320743/215638993-6c7e0c6b-cd51-478b-a53a-1f6af638e1d3.png">

Afterwards I created the root route that queried my Mongo database and passed the Mars data into an HTML template for displaying the data. 

Finally, I created a HTML file that took the Mars data dictionary and displayed all the data in the appropriate HTML elements. 

### Conclusion
With this project my goal was to showcase my ability to web scrape, store unstructured data in a NoSQL database and use flask to build a web application. As a data scientist, I could use these skills in a machine learning project that uses the data to uncover insights and bring value to a company. 

## Additional Information

### Websites:
https://redplanetscience.com/

https://spaceimages-mars.com/

https://galaxyfacts-mars.com/

https://marshemispheres.com/


### Tools:


1. Jupyter Notebook


2. Python


3. Selenium webdriver


4.  ChromeDriverManager


5. Beautiful Soup


6. Flask Application


7. MongoDB


8. HTML


9. CSS


10. Bootstrap
