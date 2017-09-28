'''
Web crawler and scraper 1.0

Created by Omar Padierna on February 2017
 
'''
#Import crawler script
from isic_crawler import *
from isic_crawler2 import *
#Import scraper script
from isic_scraper import *
#Import script that writes in json
#from writeJson import *
from checkJson import imageIntegrity2

class Img_Data:
    def __init__ (self):
        self.data = ""
        self.img = ""
        self.img_url= ""
        self.img_path= ""
        self.page=""
        self.parsed_data={}


def runJob():
    #Attempt to open file "page.txt" 
    currentPath="/Users/omarpadierna/Desktop/"
    try:
        f =open("page.txt",'r')
        #Get data in page.txt
        last=f.read()
        f.close()
        lastPage=last.split(",",2)[0]
        lastImage=last.split(",",2)[1]
        print("The last page you scraped was: "+lastPage+" and the last image you scraped was: "+lastImage)

        lastnumber=lastPage.split("-",2)[1]

        verification=int(lastnumber)-int(lastImage)
        #Set firstTime flag to false cause if try worked then this is not the first time this code has been run
        firstTime = False
        #check if the latest page has been finished. image number is always 1 less than page range i.e last image in 1 -50 is 0000049
        if verification == 1:
            pageDone= True
        #If verification is not 1 then page has not been done. set flag. 
        else :
            pageDone= False

    ######################################### Sending instruction to crawler and scraper
        #Run crawler job, receive data in tables
        #Change to ISIC_Crawler if want to run the original code.
        tables = ISIC_Crawler2(lastPage, lastImage, pageDone, firstTime)
        if len(tables)!=0:
            #Open txt page and write last scraped object
            f = open("page.txt", "w")
            page=tables[-1].page
            print("The last scraped page was: "+page)
            current=tables[-1].img[0:12]
            print("The last downloaded image was: "+current)
            image_number=current.split("_",2)[1]
            f.write(page+","+image_number)
            f.close()
            #update Json file with new data
            #writeFile(tables)
            #imageIntegrity3 (currentPath, tables)
            #Run scraping job (this is where images get downloaded)
            ISIC_Scraper(tables)
            last_image=int(image_number)
            currentPath="/Users/omarpadierna/Desktop/"
            imageIntegrity2(currentPath, last_image)
        else:
            print("Crawler didn't return any data! ")
            


    #If file "page.txt" doesn't exist it means it is the first time the scraper is being executed.
    except FileNotFoundError :
        #indicate that this is the first time the script is run. set initial elements (i.e. first page and first image)
        print("This is the first time ISIC is crawled")
        lastPage="1 - 50"
        lastImage="0000000"
        pageDone = False
        firstTime = True
    ########################################
        #Run Selenium crawler to go through each image, extract table data and save it in array "tables". 
        #Change to ISIC_Crawler if want to run the original code.
        tables = ISIC_Crawler2(lastPage, lastImage, pageDone, firstTime)

        #Read latest data scraped, create page.txt and save data there.
        page=tables[-1].page
        print("The last scraped page was: "+page)
        current=tables[-1].img[0:12]
        print("The last downloaded image was: "+current)
        image_number=current.split("_",2)[1]
        f = open("page.txt", "w")
        f.write(page+","+image_number)
        f.close()
        #update Json file with latest data
        #writeFile(tables)
        #imageIntegrity3 (currentPath, tables)
        #Download images
        ISIC_Scraper(tables)
        last_image=int(image_number)
        currentPath="/Users/omarpadierna/Desktop/"
        imageIntegrity2(currentPath, last_image)
      ####### Downloading images in chunks of 5 ############  

runJob()