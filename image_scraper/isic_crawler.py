'''
Web crawler  1.0

Created by Omar Padierna on February 2017
 
'''
#Import dependencies
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains


#Define class object in which to save all crawled data

class Img_Data:
    def __init__ (self):
        self.data = ""
        self.img = ""
        self.img_url= ""
        self.img_path= ""
        self.page=""
        self.parsed_data={}



##This function must return the array in which it saves the info so it can be used for processing in other functions. 

def ISIC_Crawler(lastPage, lastImage, pageDone, firstTime):
	try:
		tables=[]
		index=0
		#Initialize Selenium webdriver (i.e. start new Firefox instance)
		driver = webdriver.Firefox()
		driver.implicitly_wait(120)
		#Indicate driver which website to crawl
		driver.get("https://isic-archive.com/#images")

		#Initialize wait property for webdriver. Then tell it to wait until accept button appears. Click button
		driver.wait = WebDriverWait(driver, 120)
		button = driver.wait.until(EC.element_to_be_clickable((By.ID, "isic-terms-accept")))
		button.click()

		#Assume current page is NOT the last visited page 
		in_page=False

		#Get to the last visited page
		firsttimepage= True
		#Change to false if going forward in the pagination
		firstlast=False
		while (in_page is False):

			#Get current page
			
			if firsttimepage == True:
				#once page is reached wait 5 seconds
				print("Waiting 5 seconds for page to finish loading")
				time.sleep(5)
			else:
				#Interval of page jumping
				print("Waiting 3 seconds for page to finish loading") #3 seconds seeemed to work
				time.sleep(1)
			div=driver.find_element_by_id("isic-images-hasPaging")
			page=div.find_element_by_class_name("page")
			current_page=page.get_attribute("innerHTML")
			print("This is the current page: "+current_page)
			print("This is the last visited page: "+lastPage)

			#Check if current page is last (visited) page if not click "next" button and repeat process
			if current_page == lastPage:
				print("Reached last visited page!")
				if pageDone == True :
					print("All images in this page have been extracted. Redirecting to next page")
					nextbutton=driver.find_element_by_id("isic-images-seekNext")
					nextbutton.click()
					firsttimepage=False
					print("Waiting 10 seconds for page to finish loading")
					time.sleep(5)
				in_page= True
			#If current page is not the last visited then look for next button and click it. Update current_page value to new page. 
			else :
				
				if firstlast == True:
					print("This is not the last visited page!. Redirecting to last page")
					nextbutton=driver.find_element_by_id("isic-images-seekLast")
					firstlast= False
				else:
					print("This is not the last visited page!.Redirecting to previous page")
					#Change to "isic-images-seekNext" if going forward in the pagination
					nextbutton=driver.find_element_by_id("isic-images-seekNext")
				nextbutton.click()
				firsttimepage=False
				div=driver.find_element_by_id("isic-images-hasPaging")
				page=div.find_element_by_class_name("page")
				current_page=page.get_attribute("innerHTML")
				print("New page is: "+ current_page)
			#current page is detected as string, change to integer
			currentPage_number=int(current_page.split("-",2)[1])
			#Make sure current page is not the last one 
			if currentPage_number == 12086:
				#Since pagination is in intervals, change interval to page number (i.e 1-50 is 1, 51-100 is 2, etc)
				actual_page = 242
				last_page=actual_page+1
			else:
				#Since pagination is in intervals, change interval to page number (i.e 1-50 is 1, 51-100 is 2, etc)
				actual_page_float=currentPage_number/50
				actual_page=int(actual_page_float)
				#create last page to be scraped, adding 3 makes the size chunk to 150 images because each page has 50 images
				last_page=actual_page+1
			
#################################### Actual crawling ##############################################
		#Loop through the pages that will be scraped. 
		for x in range (actual_page,last_page):
			#Wait 5 seconds (so all images load, otherwise box element that has images will be empty)
			print("Waiting for images to load: 5 seconds")#90 was working
			time.sleep(6)
			print("Waiting is finished!")
			#Get box with images
			box2=driver.find_element_by_id("isic-images-imageWall")
			#limit =0
			#Extract images then iterate on each image
			buttons = box2.find_elements_by_tag_name("img")
			for button in buttons:
				try:
					driver.wait.until(EC.presence_of_element_located((By.TAG_NAME,"img")))
					print("Found image!")
				finally:
					pass
				#Scroll up so image is visible
				driver.execute_script("return arguments[0].scrollIntoView();", button)
				#Generate Img_Data instance (otherwise elements will be overwritten)
				result=Img_Data()

				#Get page
				div=driver.find_element_by_id("isic-images-hasPaging")
				staleness=True
				while (staleness is True):
					staleness=EC.staleness_of(div)
					print("Checking page div is not stale hold on...")

				page=div.find_element_by_class_name("page")
				result.page=page.get_attribute("innerHTML")
				print("Got paging!")

				#Click on image
				button.click()

				#Wait 2 seconds and then look for table with image data
				print("Waiting 500 ms in order to avoid getting kicked out...")
				time.sleep(.7)
				#driver.wait.until(EC.element_to_be_clickable((By.ID, "isic-terms-accept")))
				#image_details=driver.find_element_by_class_name("isic-image-details-name")
				image_details=driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"isic-image-details-name")))
				image_details_html=image_details.get_attribute("innerHTML")
				image_name=image_details_html[0:12]
				image_name_number=image_name.split("_",2)[1]
				print("got image details!")
				#If the current image number is larger than the last image in page.txt then scrape it.
				if int(image_name_number) > int(lastImage) or firstTime == True:
					##Begin table extraction 
					print("Getting details of image: " + image_name)
					print("Looking for image table")
					#table=driver.find_element_by_class_name("isic-image-details-table")
					table=driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isic-image-details-table")))
					staleness=True
					while (staleness is True):
						staleness=EC.staleness_of(table)
						print("Checking image is not stale hold on...")
					#Extract data and save it in a tuple
					table_html=table.get_attribute("innerHTML")
					result.data=table_html
					print("Got image table, looking for button")
					#Click button to open image in new tab then switch focus on that tab
					button=driver.wait.until(EC.presence_of_element_located((By.ID,"isic-image-details-openwindow")))
					staleness=True
					while (staleness is True):
						staleness=EC.staleness_of(button)
						print("Checking button is not stale hold on...")
					print("Button should not be stale anymore")
					#button=driver.find_element_by_class_name("openwindow")
					button.click()
					print("Redirecting to hi-res image: Waiting 300 ms...")
					time.sleep(.4)
					driver.switch_to_window(driver.window_handles[-1])
					url_correct=False
					while(url_correct is False):
						imageUrl=driver.current_url
						#Get image url
						if imageUrl=="about:blank":
							print("URl was not received! trying again!")
						else:
							url_correct=True
					#about:blank
					result.img_url=imageUrl

					#Get image details and save them in the same tuple 
					image=driver.find_element_by_tag_name("title")
					image_html=image.get_attribute("innerHTML")
					result.img=image_html

					#Save tuple in array, go back to previous tab and wait again
					tables.append(result)    
					driver.close()
					driver.switch_to_window(driver.window_handles[0])
				
				#If the current image number is not larger than the last image in page.txt then ignore.
				else:
					print("This is not the latest crawled image: Waiting 300 ms...")
					time.sleep(.7)

			#Click next button once all images in that page have been crawled
			if result.page != "12051 - 12086":
				nextbutton=driver.find_element_by_id("isic-images-seekNext")
				nextbutton.click()
##################################End of crawling process#################################################
		
		#Close browser
		driver.quit()
		print("300 images scraped! saving! will restart process again after storing all data")
		#Return data
		return tables

#Catch exceptions in case job gets cancelled for some reason. 
	except StaleElementReferenceException:
		driver.quit()
		print("Oops something went wrong! try again! Error: Stale element")
		return tables

	except NoSuchElementException:
		driver.quit()
		print("Oops something went wrong! try again! Error: No such Element")
		return tables

	except TimeoutException:
		driver.quit()
		print("Oops something went wrong! try again! Error: Timeout")
		return tables
	except NoSuchWindowException:
		driver.quit()
		print("Oops something went wrong! try again! Error: No such Window")
		return tables
	except WebDriverException:
		print("Oops something went wrong! try again! Error: WebDriverException")
		return tables