#import dependencies
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Set up driver
    Browser = webdriver.Chrome(ChromeDriverManager().install())

    news_title, news_p = mars_news(Browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": mars_images(Browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemi(Browser),
    }

    # Stop webdriver and return data
    Browser.quit()
    return data

def mars_news(Browser):
    #Visit mars url
    url = 'https://redplanetscience.com/'
    Browser.get(url)

    #scrape page into soup object
    html=Browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # add try/except for error handling
    try:
        # Use the parent element to find the first a tag and save it as `news_title`
        slide_elem = soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    #return
    return news_title, news_p

def mars_images(Browser):
    #visit mars space image website
    JPL_url = "https://spaceimages-mars.com/"
    Browser.get(JPL_url)

    #scarpe page into soup object
    JPL_html = Browser.page_source
    JPL_soup = BeautifulSoup(JPL_html, 'html.parser')
    
    # Add try/except for error handling
    try:
        #find the image URL for the current Featured Mars Image
        img_tag = JPL_soup.find("img", class_="headerimage fade-in")

        #store jpg file name in a varible
        img_file_name = img_tag.get("src")

    except AttributeError:
        return None

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
        hemisphere_dict = {}

        #visit JPL mars space image website
        Browser.get(url)

        #create html variable
        temp_html = Browser.page_source

        #create soup object
        temp_soup = BeautifulSoup(temp_html, 'html.parser')

        #look for tag that contains the image URL to the full-resolution image
        temp_a = temp_soup.find_all("a")

        #create a temp list that resets for each website
        href_list=[]

        #create a loop through each a tag for href image links
        for a in temp_a:
            #pull each href link and append it to the href_list
            link=a.get("href")

            href_list.append(link)

        #create full url with href link
        img_link= (f"https://marshemispheres.com/{href_list[3]}")

        #add img url to hem dict
        hemisphere_dict['img_url'] = img_link

        #look for tag that contains the image URL to the full-resolution image
        temp_b = temp_soup.find("h2", class_ = "title")

        # Get Hemisphere title
        hemisphere_dict['title'] = temp_b.text

        #append this image url to hemisphere_image list
        hemi_imgs_list.append(hemisphere_dict)  

    #return list of hemisphere images
    return hemi_imgs_list

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
