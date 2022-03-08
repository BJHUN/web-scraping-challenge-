from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)


    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'mars_facts': mars_facts()
    }

    return mars_data

def mars_news(browser):    
    # Visit https://redplanetscience.com
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")

    #scrape title and paragraph 
    section = news_soup.select_one('div.list_text')    
    
    # news title
    news_title = section.find('div', class_= "content_title").get_text() 

    # news paragraph
    news_paragraph = section.find('div', class_= "article_teaser_body").get_text()

    # Close the browser after scraping
    #browser.quit()

    # Return results
    return news_title, news_paragraph

def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    image_soup = bs(html, "html.parser")

    #scrape image
    featured_image_url = image_soup.find('img',class_= "headerimage").get("src")

    image_url = f'{url}{featured_image_url}'

    return image_url

def mars_facts():
    
    mars_df = pd.read_html("https://galaxyfacts-mars.com/")[0]

    mars_df.columns = ['Description','Mars', "Earth"]

    mars_df.set_index('Description',inplace = True)

    mars_facts = mars_df.to_html()

    return mars_facts

