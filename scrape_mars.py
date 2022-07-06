#import dependencies
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    Browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_p = mars_news(Browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": mars_images(Browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemi(Browser),
        "image_titles": hemi_titles(Browser)
    }

    # Stop webdriver and return data
    Browser.quit()
    return data


def mars_news(Browser):
    #Visit mars url
    url = 'https://redplanetscience.com/'
    Browser.visit(url)

    #scrape page into soup object
    html=Browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #the tag that contains all news titles and paragraphs
    sections = soup.find_all('div', class_="content_title")
    containers = soup.find_all('div', class_="article_teaser_body")

    #list of titles and paragraphs
    title_list=[]
    p_list=[]

    # Loop through returned sections for titles
    for section in sections:

        #retrieve the news title
        title = section.text

        #append list with each title
        title_list.append(title)

    # Loop through returned containers for paragraphs
    for container in containers:

        #retrieve the news paragraph
        text = container.text

        #append list with each paragraph
        p_list.append(text)

    #the most recent title with its corresponding teaser paragraph.
    news_title = title_list[0]
    news_p = p_list[0]

    #return
    return news_title, news_p

def mars_images(Browser):
    #visit mars space image website
    JPL_url = "https://spaceimages-mars.com/"
    Browser.visit(JPL_url)

    #scarpe page into soup object
    JPL_html = Browser.html
    JPL_soup = BeautifulSoup(JPL_html, 'html.parser')
    
    #find the image URL for the current Featured Mars Image
    img_tag = JPL_soup.find("img", class_="headerimage fade-in")

    #store jpg file name in a varible
    img_file_name = img_tag.get("src")

    #create full url for img
    featured_image_url = (f"{JPL_url}{img_file_name}")

    #return
    return featured_image_url

def mars_facts():
    #use Pandas to scrape the table containing facts about the planet including diameter, mass, etc.
    facts_url = "https://galaxyfacts-mars.com/"

    tables = pd.read_html(facts_url)
    df = (tables[0])

    #clean table before converting to html
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True)

    #Use Pandas to convert the data to a HTML table string.
    mars_html = df.to_html(classes="table table-striped")
    
    #return
    return mars_html

def mars_hemi(Browser):
    #each individual url for a specific hemisphere of mars
    cerberus_url="https://marshemispheres.com/cerberus.html"
    schiaparelli_url="https://marshemispheres.com/schiaparelli.html"
    syrtis_url="https://marshemispheres.com/syrtis.html"
    valles_url="https://marshemispheres.com/valles.html"

    #create a list of urls to loop through
    list_urls= [cerberus_url, schiaparelli_url, syrtis_url, valles_url]

    hemi_imgs_list=[]

    #create a loop that goes through each url extracting the images
    for url in list_urls:
        #visit JPL mars space image website
        Browser.visit(url)

        #create html variable
        temp_html = Browser.html

        #create soup object
        temp_soup = BeautifulSoup(temp_html, 'html.parser')

        #look for tag that contains the image URL to the full-resolution image
        temp_a = temp_soup.find_all("a")

        #create a temp list for href links, that also resets for each website
        href_list=[]

        #create a loop through each "a" tag for href image links
        for a in temp_a:
            #pull each href link and append it to the href_list
            link=a.get("href")

            href_list.append(link)

        #create full url with href link
        #item number 5 in list is the desired link
        img_link= (f"https://marshemispheres.com/schiaparelli.html/{href_list[3]}")

        #append this image url to hemisphere_image list
        hemi_imgs_list.append(img_link) 
    
    #return list of hemisphere images
    return hemi_imgs_list

def hemi_titles(Browser):
    #each individual url for a specific hemisphere of mars
    cerberus_url="https://marshemispheres.com/cerberus.html"
    schiaparelli_url="https://marshemispheres.com/schiaparelli.html"
    syrtis_url="https://marshemispheres.com/syrtis.html"
    valles_url="https://marshemispheres.com/valles.html"

    #create a list of urls to loop through
    list_urls= [cerberus_url, schiaparelli_url, syrtis_url, valles_url]
    hemispheres=[]

    #create a loop that goes through each url extracting the image title
    for url in list_urls:
        #visit JPL mars space image website
        Browser.visit(url)

        #create html variable
        temp_html = Browser.html

        #create soup object
        temp_soup = BeautifulSoup(temp_html, 'html.parser')

        #look for tag that contains the image title text to the sample image and the tag for the img url
        temp_b = temp_soup.find("h2", class_ = "title")
        temp_c = temp_soup.find("a", text="Sample").get("href")

        #create a dictionary to add to the list
        temp_dict = {
        "title": temp_b,
        "img_url": temp_c
        }

        #append to hemispheres list
        hemispheres.append(temp_dict)

    return hemispheres



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
