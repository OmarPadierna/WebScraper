'''
Web crawler and scraper 1.0

Created by Omar Padierna on February 2017
 
'''
#Import scraping dependencies
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from image_scraper.spiders.image_spider import *
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from twisted.internet.error import *
#declare image object. 
class Img_Data:
    def __init__ (self):
        self.data = ""
        self.img = ""
        self.img_url= ""
        self.img_path= ""
        self.page=""
        self.parsed_data={}


#Define scraper for job after crawling 
def ISIC_Scraper(tables):	

		#index=0<<-used during testing.ignore
		#get size of scraped data
		#table_length=len(tables) <<<-used during testing. ignore
		#Define process with pre-defined settings
		process=CrawlerRunner(get_project_settings())
		#Make sure process is run sequentially 
		@defer.inlineCallbacks
		#Define crawl command
		def crawl():
			#iterate through tables saving each element in variable table
			for table in tables:
				print ("Extracting image:"+table.img[0:12])
				print("From url: "+table.img_url)
				#Create spider instance and extract image Name and the url of the image
				current=table.img[0:12]
				image_number=current.split("_",2)[1]
				imageName="S_"+image_number
				imageUrl=table.img_url
				Okaz= ImageSpider()
				#Indicate which spider(s) to crawl and pass image name and image URL

				yield process.crawl(Okaz,image_url=imageUrl,image_name=imageName)
			#after defining each process indicate reactor to stop
			reactor.stop()
		#start crawl process
		crawl()
		#start Twister reactor
		reactor.run()

		
		
#Define scraper for job after data integrity check. (same as above just different list)
def ISIC_Scraper2(lista):

		process=CrawlerRunner(get_project_settings())
		@defer.inlineCallbacks
		#Define crawl command
		def crawl():
			for element in lista:
				imageUrl=element[0]
				imgName=element[1]
				print ("Extracting image:"+imgName)
				print("From url: "+imageUrl)
				#Create spider instance and extract image Name and the url of the image
				Okaz= ImageSpider()
				#Indicate which spider(s) to crawl and pass image name and image URL
				yield process.crawl(Okaz,image_url=imageUrl,image_name=imgName)
			reactor.stop()
		crawl()
		reactor.run()

