#import required libraries
import scrapy
from image_scraper.items import ImageScraperItem
from urllib.parse import urlparse

#define spider
class ImageSpider(scrapy.Spider):
    
    #name spider
    name = "images"
    def __init__(self, image_url=None, image_name=None, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.imageName= image_name
        self.imageUrl= image_url

    #url that will be crawled  (spider will go to this url but in this project it is not used since images are downloaded from image_url)
    start_urls= ['https://news.ycombinator.com/newest']
    #response method
    def parse(self, response):
        #This line is not used. Ignore
        self.log("Scraping: "+response.url)
        #This line is not used. ignore
        articles = response.css('body')
        #Create item object
        item1 = ImageScraperItem()
        #Write source name to image object
        item1["source"]=self.imageName
        print("Scraping Image: "+self.imageName)
        #Save image url to image object. Actual downloading is done behind the scenes by scrapy. 
        #To know more read about Scrapy pipelines and media requests
        item1["image_urls"]=[self.imageUrl]
        print("From: "+self.imageUrl)
        yield item1
        