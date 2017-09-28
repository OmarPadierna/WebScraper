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
from selenium.webdriver.support.ui import Select
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

def ISIC_Crawler2(lastPage, lastImage, pageDone, firstTime):
	try:
		tables=[]
		index=0
		#Initialize Selenium webdriver (i.e. start new Firefox instance)
		driver = webdriver.Firefox()
		driver.implicitly_wait(10)
		#Indicate driver which website to crawl
		driver.get("https://isic-archive.com/#images")

		#Initialize wait property for webdriver. Then tell it to wait until accept button appears. Click button
		driver.wait = WebDriverWait(driver, 10)
		button = driver.wait.until(EC.element_to_be_clickable((By.ID, "isic-terms-accept")))
		button.click()

		#Assume current page is NOT the last visited page 
		in_page=False

		#Get to the last visited page
		firsttimepage= True
		#Change to false if going forward in the pagination
		firstlast=True
		while (in_page is False):

			#Get current page
			
			if firsttimepage == True:
				#once page is reached wait 5 seconds
				print("Waiting 5 seconds for page to finish loading")
				time.sleep(5)
			else:
				#Interval of page jumping
				print("Waiting 3 seconds for page to finish loading") #3 seconds seeemed to work
				time.sleep(1.4)
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
					time.sleep(10)
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
					nextbutton=driver.find_element_by_id("isic-images-seekPrev")
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
				last_page=actual_page+2
			#Scraping 500 images...
#################################### Actual crawling ##############################################
		#Loop through the pages that will be scraped. 
		for x in range (actual_page,last_page):
			#Wait 5 seconds (so all images load, otherwise box element that has images will be empty)
			print("Waiting for images to load: 5 seconds")#90 was working
			time.sleep(7)
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
				time.sleep(.8)
				#driver.wait.until(EC.element_to_be_clickable((By.ID, "isic-terms-accept")))
				#image_details=driver.find_element_by_class_name("isic-image-details-name")
				repeater = True
				while(repeater is True):	
					try:
						image_details=driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"isic-image-details-name")))
						image_details_html=image_details.get_attribute("innerHTML")
						image_name=image_details_html[0:12]
						image_name_number=image_name.split("_",2)[1]
						print("got image details!")
						repeater=False
					except StaleElementReferenceException:
						print("image details are stale")
						time.sleep(.5)
						pass
					except NoSuchElementException:
						print("image details are stale")
						time.sleep(.5)
						pass
				#If the current image number is larger than the last image in page.txt then scrape it.
				if int(image_name_number) > int(lastImage) or firstTime == True:
					repeatsing=True
					while(repeatsing is True):
						try: 
							selector=driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"input-sm")))
							staleness=True
							selected_selector= Select(selector)
							print("Getting options")
							repeatsing=False
						except StaleElementReferenceException:
							print("selector is stale")
							time.sleep(.5)
							pass
						except NoSuchElementException:
							print("selector is not there, waiting...")
							time.sleep(.5)
							pass
					repeat = True
					while (repeat is True):
						try:
							print("Trying again")
							go_on= False
							while (go_on is False):
								options=selected_selector.options
								if len(options) > 1:
									print("Options good to go")
									selected_selector.select_by_index(1)
									go_on= True
									repeat=False
								else:
									print("Options not loaded waiting 500 ms")
									time.sleep(.5)
									go_on= False
						except StaleElementReferenceException:
							print("Element is stale lets wait")
							time.sleep(.5)
							selector=driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"input-sm")))
							selected_selector= Select(selector)
							pass
					print("waiting for segmentation")
					repeats=True
					while (repeats is True):
						try: 
							selector_table=driver.wait.until(EC.presence_of_element_located((By.ID,"isic-segmentation-display-container")))
							print("Got selector table")
							selector_image= selector_table.find_element_by_tag_name("img")
							selector_img_src=selector_image.get_attribute("src")
							print(selector_img_src)
							print("got selector image details!")
							result.img_url=selector_img_src
							imgname=driver.find_element_by_class_name("isic-image-details-name")
							imgname2=imgname.get_attribute("innerHTML")
							result.img=imgname2
							#Save tuple in array, go back to previous tab and wait again
							tables.append(result)
							repeats = False
						except NoSuchElementException:
							print("No such element lets wait ")
							time.sleep(.5)
							pass
						except StaleElementReferenceException:
							print("Stale element lets wait")
							time.sleep(.5)
							pass


					
				
				#If the current image number is not larger than the last image in page.txt then ignore.
				else:
					print("This is not the latest crawled image: Waiting 300 ms...")
					time.sleep(.8)

			#Click next button once all images in that page have been crawled
			if result.page != "12051 - 12086":
				nextbutton=driver.find_element_by_id("isic-images-seekNext")
				nextbutton.click()
##################################End of crawling process#################################################
		
		#Close browser
		driver.quit()
		print("500 images scraped! saving! will restart process again after storing all data")
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