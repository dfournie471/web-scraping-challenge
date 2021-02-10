from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=True)

def scrape_info():
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser = init_browser()
    browser.visit(url)
    html_1=browser.html
    soup=bs(html_1,'html.parser')
    title = soup.find_all('div',class_="content_title")[1].text
    news_p = soup.find('div', class_="article_teaser_body").text


    
    url_2='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_2)
    html_2=browser.html
    soup_2=bs(html_2,"html.parser")
    image_url=soup_2.find_all('img')[1]["src"]
    featured_image='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_url


    url_3="https://space-facts.com/mars/"
    tables=pd.read_html(url_3)
    df=tables[0]
    df.columns=['Category','Mars']
    df.set_index("Category",inplace=True)
    final_df=df.to_html()


    hemisphere_image_urls=[]
    click_lst=['Cerberus','Schiaparelli','Syrtis','Valles']
    regular_path='https://astrogeology.usgs.gov'
    url_4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    for x in range(4):
        browser.visit(url_4)
        browser.links.find_by_partial_text(click_lst[x]).click()
        html_3=browser.html
        soup_3=bs(html_3,'html.parser')
        titles=soup_3.find('h2',class_="title").text
        img_url=soup_3.find_all('img',class_="wide-image")[0]['src']
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


