
#!/usr/bin/env python
# coding: utf-8

# ## NASA Mars News
# * Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import IPython
import time


# In[2]:


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# In[3]:

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(5)

    # In[4]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[5]:


    news_title = soup.find(class_='content_title')
    news_p = soup.find(class_='article_teaser_body')


    # In[6]:


    # print(news_title.text)
    # print(news_p.text)


    # ## JPL Mars Space Images - Featured Image
    # 
    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # 
    # * Make sure to find the image url to the full size .jpg image.
    # 
    # * Make sure to save a complete url string for this image.

    # In[7]:


    url_mars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_mars)


    # In[8]:


    html_mars = browser.html
    soup1 = BeautifulSoup(html_mars, 'html.parser')


    # In[9]:


    url_front = 'https://www.jpl.nasa.gov'

    featured_image = soup1.find(class_='button fancybox')
    featured_image_url = url_front + featured_image.get('data-fancybox-href')

    # print(featured_image_url)


    # ## Mars Weather
    # 
    # * Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

    # In[10]:


    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)


    # In[11]:


    html_twitter = browser.html
    soup2 = BeautifulSoup(html_twitter, 'html.parser')


    # In[12]:


    last_tweet = soup2.find(class_='js-tweet-text-container')

    mars_weather = (last_tweet.text).strip()

    # print(mars_weather)


    # ## Mars Facts
    # 
    # * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string.

    # In[13]:


    facts_table = pd.read_html('https://space-facts.com/mars', index_col=0)


    # In[14]:


    facts_df = facts_table[0]
    facts_html = facts_df.to_html(header=False)
    facts_html = facts_html.replace('\n', '')
    # facts_html


    # ## Mars Hemispheres
    # 
    # * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # In[16]:


    url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemis)


    # In[17]:


    html_hemis = browser.html
    soup4 = BeautifulSoup(html_hemis, 'html.parser')


    # In[18]:


    hemi_links = soup4.find_all(class_='itemLink')

    gov_url = 'https://astrogeology.usgs.gov'
    link_list = []
    img_url_list = []
    img_title_list = []

    hemi_img_urls = []

    for link in hemi_links:
        if (gov_url + link.get('href')) not in link_list:
            link_url = gov_url + link.get('href')
            link_list.append(link_url)
            
            browser.visit(link_url)
            link_html = browser.html
            soup_loop = BeautifulSoup(link_html, 'html.parser')
            img_title = soup_loop.find('h2', class_='title')
            img_url = ((soup_loop.find('ul')).find('li')).find('a')
            hemi_img_urls.append(
            {'title': ((img_title.text).strip('Enhanced')).strip(),
            'img_url': img_url.get('href')
            })
            
    # hemi_img_urls


    # ## Step 2 - MongoDB and Flask Application
    # * Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
    # * Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

    # In[19]:


    scraped_dict = {
        'latest_mars_news': {
            'news_title': news_title.text,
            'news_p': news_p.text
        },
        'featured_mars_image': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': facts_html,
        'mars_hemispheres': hemi_img_urls
    }


    # In[20]:
    browser.quit()

    return(scraped_dict)


