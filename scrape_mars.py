

from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import pandas as pd
import time

# Set the chromedriver path
options = webdriver.ChromeOptions() 
options.add_argument('--headless')
driver=webdriver.Chrome("C:/Data_Visualization//UCFLM20190409DATA//Homework//12-Web-Scraping-and-Document-Databases//chromedriver.exe", chrome_options=options)
executable_path = {"executable_path": "C:/Data_Visualization//UCFLM20190409DATA//Homework//12-Web-Scraping-and-Document-Databases//chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


#driver=webdriver.Chrome("C:\Data_Visualization\\UCFLM20190409DATA\\Homework\\12-Web-Scraping-and-Document-Databases\\chromedriver.exe")

def init_browser():
    executable_path = {"executable_path": "C:/Data_Visualization//UCFLM20190409DATA//Homework//12-Web-Scraping-and-Document-Databases//chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

# Latest News Article
    news_url ="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = bs(html, 'html.parser')
   
    listTextLabelElem = news_soup.find('div', class_='list_text')

    mars["news_title"] = listTextLabelElem.find('a').get_text()
    mars["news_p"] = news_soup.find('div', class_='article_teaser_body').get_text()
    
#JPL Mars Space Images - Featured Image    
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA00069-1920x1200.jpg"
    browser.visit(featured_image_url)
    html = browser.html

    time.sleep(2)

    # Find the image url to the full size
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(2)

    # Save a complete url string for this image
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    time.sleep(2)

     # Parse the resulting html with soup
    html = browser.html
    img_soup = bs(html, 'html.parser')

    # find the relative image url
    img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']

    # Use the base url to create an absolute url
    mars["featured_image"] = f'https://www.jpl.nasa.gov{img_url_rel}'

 # Retrieve Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)

    html = browser.html
    weather_soup = bs(html, 'html.parser')

    # ind a tweet with the data-name `Mars Weather`
    Mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    # Set weather
    Mars_weather_tweet = Mars_weather_tweet.find('p', 'tweet-text').get_text()

# Mars Hemisphere Data
    Mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(Mars_hemispheres_url)
    html = browser.html
    mars_hemispheres_soup = bs(html,"html.parser")
    links = mars_hemispheres_soup.find_all('div', class_='item')

    time.sleep(2)

    #Mars_hemispheres_title = mars_hemispheres_soup.find('a', class_='product-item')
   
    # Create a list of all of the hemispheres
    hemisphere_image_url = []

    for link in links:
        title = link.h3.text
        print(title)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(html, 'html.parser')
        results = soup.find('div', class_='downloads')
        img_url = results.a['href']
        hemisphere_image_url.append({'title': title, 'img_url': img_url})
        print(img_url)
        browser.back()
    
        time.sleep(2)
        
    browser.quit()

    return mars

    
   
