#Import dependencies
import json
from pathlib import Path
from isic_scraper import *

'''
This function checks the latest element in the json file and returns its index.
'''

class Img_Data:
    def __init__ (self):
        self.data = ""
        self.img = ""
        self.img_url= ""
        self.img_path= ""
        self.page=""
        self.parsed_data={}

def checkLatestElement ():

    with open('dataset.json') as f:
        lines=json.load(f)
        integers=list(lines.keys())

        for index,key in enumerate(integers):
        	integer=int(key)
        	integers[index]=integer
        sortedkeys=sorted(integers)
        sortedkeys_s=sortedkeys[-1]
        print("This is the latest key: "+str(sortedkeys_s))
        return sortedkeys_s
'''
This function checks the latest page in the json file and returns its range.
'''
def checkLatestPage ():

    with open('dataset.json') as f:
        lines=json.load(f)
        integers=list(lines.keys())
        Latestpage=""
        for index,key in enumerate(integers):
        	integer=int(key)
        	integers[index]=integer
        sortedkeys=sorted(integers)
        sortedkeys_s=sortedkeys[-1]
        if sortedkeys_s == -1:
            pass
        else:
            Latestpage=lines[str(sortedkeys_s)]["page"]
            print("This is the latest page: "+Latestpage)
        return Latestpage
'''
This function checks the latest page in the json file and returns its range.
'''
def imageIntegrity (currentPath):

    with open('dataset.json') as f:
        lines=json.load(f)
        keys=list(lines.keys())
        lista=[]
    print("Verifying that all entries have its respective jpg file")
    integrity=False
    for key,value in lines.items():
    	if key == "-1":
    		#Empty element was created because json file has to have something when using json.load.
    		print("Ignoring empty element")
    		integrity=False
    	else:
    		dictionary=lines[key]
    		path=currentPath+dictionary["img_path"]
    		image=Path(path)
    		downloaded=image.is_file()
    		if downloaded == False:
    			integrity = False
    			print("The jpg file for image: "+ dictionary["img"][0:12]+ " has not been downloaded")
    			print("Attempting download")
    			imageUrl=dictionary["img_url"]
    			imgName=dictionary["img"][0:12]
    			lista.append((imageUrl,imgName))

    missing=len(lista)
    if missing!=0:
    	print("Downloading images")
    	ISIC_Scraper2(lista)
    	integrity= True
    print("All entries should have their respective jpg file")
    return integrity

def imageIntegrity2 (currentPath,last):
    

    missing_images=[]
    index=0
    for x in range (0,last):
        #ISIC_0011990
        #ISIC_0000000
        zeroes10=int(x/10)
        zeroes100=int(x/100)
        zeroes1000=int(x/1000)
        zeroes10000=int(x/10000)

        #Means single digit
        if zeroes10 == 0:
            name_path="ima/S_000000"+str(x)+".jpg"
        #Check for double digit
        elif zeroes100== 0:
            name_path="ima/S_00000"+str(x)+".jpg"
        #Check for triple digit
        elif zeroes1000==0:
            name_path="ima/S_0000"+str(x)+".jpg"
        #Check for 4 digits
        elif zeroes10000==0:
            name_path="ima/S_000"+str(x)+".jpg"
        else:
            name_path="ima/S_00"+str(x)+".jpg"

        path=currentPath+name_path
        image=Path(path)
        downloaded=image.is_file()

        if downloaded == False:
            print("Checking into the image folder directly it seems that image: "+name_path+" is missing")
            missing_images.append(name_path)
            
    print(missing_images)
    print(len(missing_images))
    print(index)
##Goal, compare image file name with index in json and with img name in json. If all 3 are equal then things are good. 
def imageIntegrity3 (currentPath, table):
    with open('dataset.json') as f:
        lines=json.load(f)

    integers=list(lines.keys())

    for index,key in enumerate(integers):
        integer=int(key)
        integers[index]=integer
    sortedkeys=sorted(integers)
    last_element=sortedkeys[-1]

    sortedkeys_s=last_element-len(table)+1
    print("Begins at: "+str(sortedkeys_s))
        
    index=0
    lista=[]
    integrit=True
    #Receive table and count elements
    for element in table:
        #Get table name 
        imgName_table=element.img[5:12]
        #Get table name for file (includes .jpg)
        imgName_forfile=element.img[0:12]
        #Change name for integer
        namenum_table=int(imgName_table)
        #Generate path for image (based on table data)
        path=currentPath+element.img_path
        image=Path(path)
        #Check if image is in table
        downloaded=image.is_file()
        #Get index of element and transform to string
        f=[i for i, a in enumerate(table) if a == element]
        #Change stringkey from "[index]" to "index" 
        x=str(f)
        split1=x.split("[",1)[1]
        indexelement_string=split1.split("]",1)[0]
        indexelement=int(indexelement_string)
        stringkey=str(indexelement+sortedkeys_s)
        #Using index as key open Json data
        dictionary=lines[stringkey]
        #Get name from json data
        imgName_json=dictionary["img"][5:12]
        #Change name into number
        namenum_json=int(imgName_json)
        #Check if table name matches json index and matches file name.
        if namenum_table != namenum_json:
            index +=1
            print("There's a mislabeling in jSon file :"+str(namenum_json)+" for table name "+str(namenum_table) + "in index :" +stringkey)
            integrit=False
        #Check if image (from table path) exists, if not, get table url and table name
        elif downloaded == False:
            print("Checking into the image folder directly it seems that image: "+element.img_path+" is missing")
            print("Saving...")
            lista.append((element.img_url,imgName_forfile))
            integrit=False
    
    if integrit == True:
        print("There seems to be integrity between crawled data,json and existing files")
    missing=len(lista)
    if missing!=0:
        print("Downloading images")
        ISIC_Scraper2(lista)
        print("There should be integrity now, check again in next iteration")

'''
    with open('dataset.json') as f:
        lines=json.load(f)
        keys=list(lines.keys())
        lista=[]
    print("Verifying that all entries have its respective jpg file")
    integrity=False
    for key,value in lines.items():
        if key == "-1":
            #Empty element was created because json file has to have something when using json.load.
            print("Ignoring empty element")
            integrity=False
        else:
            dictionary=lines[key]
            path=currentPath+dictionary["img_path"]
            image=Path(path)
            downloaded=image.is_file()
            if downloaded == False:
                integrity = False
                print("The jpg file for image: "+ dictionary["img"][0:12]+ " has not been downloaded")
                print("Attempting download")
                imageUrl=dictionary["img_url"]
                imgName=dictionary["img"][0:12]
                lista.append((imageUrl,imgName))

    missing=len(lista)
    if missing!=0:
        print("Downloading images")
        ISIC_Scraper2(lista)
        integrity= True
    print("All entries should have their respective jpg file")
    return integrity
'''
def jobFinished (sortedkeys_s, integrity):

	if sortedkeys_s == 12086 and integrity == True:
		print("All entries have been scraped and cleaned! :)")
		return True
	elif sortedkeys_s == -1:
		print("Json file is empty no entries have been downloaded, 12086 entries to go")
		return False
	else:
		print("Job is not done, latest image scraped is: "+str(sortedkeys_s)+ ", "+str(12086-sortedkeys_s)+ " entries missing")
		print("If latest image is 12086 maybe not all the images have been downloaded")
		return False


#checkLatestElement()
#These are test commands used to try the file- Not relevant
#currentPath="/Users/omarpadierna/Desktop/"
#imagenumber="0003299"
#imagenumber2=int(imagenumber)
#imageIntegrity2(currentPath, imagenumber2)
#imageIntegrity(currentPath)
#latest=checkLatestElement()
#jobFinished(latest)