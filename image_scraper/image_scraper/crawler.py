'''
Web crawler and scraper 1.0

Created by Omar Padierna on February 2017

Crawl responsibly. 

'''
#for this to work you need to download geckodriver and add it to ~/usr/bin/local

#Import required libraries. Selenium for crawling, Scrapy for scraping
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

#Define class object in which to save all scraped data
class Img_Data:
    def __init__ (self):
        self.data = ""
        self.img = ""
        self.index = ""

#Initialize webdriver (start new Firefox instance)
driver = webdriver.Firefox()
#Indicate driver which website to crawl
driver.get("https://isic-archive.com/#images")

#Initialize wait property for webdriver. Then tell it to wait until accept button appears and click
driver.wait = WebDriverWait(driver, 5)
button = driver.wait.until(EC.element_to_be_clickable((By.ID, "isic-terms-accept")))
time.sleep(10)
button.click()

#Wait 5 seconds (so all images load in the DOM, otherwise box element will be empty)
time.sleep(5)
box2=driver.find_element_by_id("isic-images-imageWall")

#Extract images then iterate on each image
buttons = box2.find_elements_by_tag_name("img")
tables=[]

index=0
for button in buttons:
    #Generate Img_Data instance (otherwise elements will be overwritten)
    result=Img_Data()

    #Click on image
    print("Scraping image " + str(index))
    result.index="Scraping image " + str(index)
    button.click()

    #Wait 2 seconds and then look for table with image data
    time.sleep(2)
    table=driver.find_element_by_class_name("isic-image-details-table")

    #Extract data and save it in a tuple
    table_html=table.get_attribute("innerHTML")+"////"
    result.data=table_html

    #Click button to open image in new tab then switch focus on that tab
    button=driver.find_element_by_class_name("openwindow")
    button.click()
    time.sleep(1)
    driver.switch_to_window(driver.window_handles[-1])
    print("should be in other tab")
    url=driver.current_url
    print(url)
    #Get image details and save them in the same tuple 
    image=driver.find_element_by_tag_name("title")
    image_html=image.get_attribute("innerHTML")
    result.img=image_html
    #Save tuple in array, go back to previous tab and wait another two seconds
    tables.append(result)
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    time.sleep(2)
    index+=1
    if index > 1:
        break
    
for table in tables:
    print ("These were the indexes:"+table.index)
    print ("These were the images:"+table.img)
    print ("These were the tables:<table>"+table.data+"</table>")
time.sleep(15)
driver.quit()