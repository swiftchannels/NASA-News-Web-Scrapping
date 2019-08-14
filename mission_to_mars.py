
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import os
import requests 
import pymongo
import pandas as pd
from splinter import Browser


# In[2]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[3]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# # NASA MARS NEWS

# In[4]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[5]:


# pass the url into chrome broswer
html = browser.html
soup = bs(html, 'html.parser')
# grap the latest news
results = soup.select_one('li.slide')


# In[6]:


# slice out the Title and Title Paragraph and store on variable title and title_para respectively
title = results.find('div', class_="content_title").text
title_para = results.find('div', class_="article_teaser_body").text


# In[7]:


print("....the latest NASA news.....")
print("Title: " + title)
print("Title Paragraph: "+ title_para)


# # JPL Mars Space Images - Featured Image
# 

# In[8]:


# openning the url on chrome
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[9]:


full_image = browser.find_by_id('full_image')
full_image.click()


# In[10]:


browser.is_element_present_by_text('more info', wait_time=1)
more_info = browser.find_link_by_partial_text('more info')
more_info.click()


# In[11]:


html = browser.html
image_soup = bs(html, 'html.parser')


# In[12]:


featured_image = image_soup.select_one('figure.lede a img').get("src")
featured_image


# In[13]:


featured_image_url = f'https://www.jpl.nasa.gov{featured_image}'
featured_image_url


# ## Mars Weather Tweet

# In[14]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[15]:


html = browser.html
soup_weather = bs(html, 'html.parser')


# In[16]:


# scrape the first mars weather tweet
mars_tweet = soup_weather.select_one('div.js-tweet-text-container')


# In[17]:


mars_weather = mars_tweet.find('p').text 
mars_weather


# In[18]:


url = "http://space-facts.com/mars/"


# In[19]:


mars_df = pd.read_html(url)
mars_data = mars_df[0]
mars_data


# In[20]:


mars_fact = mars_data[["Mars - Earth Comparison", "Mars"]]


# In[21]:


Mars_fact = mars_fact.rename(columns={"Mars - Earth Comparison":"Fact_parameters"})


# In[22]:


Mars_fact.set_index('Fact_parameters', inplace = True)


# In[23]:


Mars_fact


# In[24]:


Mars_html = Mars_fact.to_html()


# In[25]:


Mars_html


# In[26]:


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# In[27]:


html = browser.html
mars_hemi = bs(html, 'html.parser')


# In[28]:


Results = mars_hemi.find_all('div', class_="item")


# In[29]:


hemisphere_image_urls = []

# First, get a list of all of the hemispheres
links = browser.find_by_css("a.product-item h3")

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()
    


# In[30]:


hemisphere_image_urls

