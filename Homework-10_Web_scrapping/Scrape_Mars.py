#%% [markdown]
# # Import dependencies

#%%
import time
import re
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver

def scrape():
    browser = init_browser()
    mars_data_scrape = {}

#%% [markdown]
# # Nasa Web Site Scrapping-Executable path
# NEWS

#%%
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


#%%
news_title = soup.find('div', class_='content_title').get_text()
print(news_title)
news_p = soup.find('div', class_='article_teaser_body').get_text()
print(news_p)

mars_data_scrape["data1"] = news_title
mars_data_scrape["data2"] = news_p

#%% [markdown]
# IMAGES

#%%
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(2)
browser.click_link_by_partial_text('more info')
time.sleep(2)
browser.click_link_by_partial_text('.jpg')


#%%
html = browser.html
soup = bs(html, 'html.parser')

featured_image_url = soup.find('img').get('src')
print(featured_img_url)

mars_data_scrape["image"] = featured_img_url

#%% [markdown]
# # Twitter Scrapping
# WEATHER

#%%
url = 'https://twitter.com/marswxreport?lang=en'
html = requests.get(url)
soup = bs(html.text, 'lxml')


#%%
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
mars_weather

mars_data_scrape["weather"] = mars_weather

#%% [markdown]
# FACTS

#%%
url = 'https://space-facts.com/mars/'
table_df = pd.read_html(url)[0]
table_df = table_df.rename(columns={0:'Mars Planet Profile', 1:''})
table_df = table_df.set_index('Mars Planet Profile', drop=True)
table_df

mars_data_scrape["table"] = table_df.to_html()

#%%
table = table_df.to_html(classes = 'table table-striped')
print(table)

#%% [markdown]
# # Mars Hemispheres

#%%
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)


#%%
from bs4 import BeautifulSoup as bs
html_hemispheres = browser.html
soup = bs(html_hemispheres, 'html.parser')
items = soup.find_all('div', class_='item')
hemisphere_image_urls = []
hemispheres_main_url = 'https://astrogeology.usgs.gov'
# Loop through the items previously stored
for i in items: 
    title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
hemisphere_image_urls

mars_data_scrape["hemispheres"] = hemisphere_image_urls
#return mars_data_scrape

#%%



