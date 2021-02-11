#import dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# def function that will set up ChromeDriverManager
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=True)

#def function that will scrape information
def scrape_info():
    #set url to first website
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    
    #visit website through browser and convert to bs
    browser = init_browser()
    browser.visit(url)
    html_1=browser.html
    soup=bs(html_1,'html.parser')
    
    #find title and preview paragraph for latest news story
    title = soup.find_all('div',class_="content_title")[1].text
    news_p = soup.find('div', class_="article_teaser_body").text


    #set url_2 to second website and set up with browser
    url_2='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_2)
    html_2=browser.html
    
    #find image url with soup
    soup_2=bs(html_2,"html.parser")
    image_url=soup_2.find_all('img')[1]["src"]
    featured_image='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_url


    #set url for 3rd website
    url_3="https://space-facts.com/mars/"
    
    #use read html to find tables within website
    tables=pd.read_html(url_3)
    
    #extract table needed and clean for use
    df=tables[0]
    df.columns=['Category','Mars']
    df.set_index("Category",inplace=True)
    
    #convert back to html
    final_df=df.to_html()

    
    #define blank list that will house image dictionaries
    hemisphere_image_urls=[]
    
    #define list that will be used in the click function loop
    click_lst=['Cerberus','Schiaparelli','Syrtis','Valles']
    
    #define path that will be the first part of img_url
    regular_path='https://astrogeology.usgs.gov'
    
    #set url for fourth website
    url_4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    #create loop that will click through the emelemts in click_list 
    #and return title of image and image url
    for x in range(4):
        browser.visit(url_4)
        browser.links.find_by_partial_text(click_lst[x]).click()
        html_3=browser.html
        soup_3=bs(html_3,'html.parser')
        titles=soup_3.find('h2',class_="title").text
        img_url=soup_3.find_all('img',class_="wide-image")[0]['src']
        
        #append results to list
        hemisphere_image_urls.append({"title":titles,"img_url":regular_path + img_url})
    
    #close browser
    browser.quit()

    #save data scraped to dictionary
    mars_data={
        "headline_title":title,
        "headline_par":news_p,
        "featured_img_url":featured_image,
        "df":final_df,
        "image_titles":titles,
        "hemisphere_pics":hemisphere_image_urls
    }
    
    #return data
    return mars_data


