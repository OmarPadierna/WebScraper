#From checkJson script and crawler script import all functions
from checkJson import *
from crawler import *

#Check the latest element (if any) in the Json file. 

latest=checkLatestElement ()
#Check the latest page (if any) in the Json file
latestPage=checkLatestPage ()

#crawler script creates page.txt file to control pagination. Open it. 
try:
	#Get page and latest scraped image from page.txt
	f =open("page.txt",'r')
	last=f.read()
	f.close()
	lastPage=last.split(",",2)[0]
	lastImage=int(last.split(",",2)[1])
	#Compare with data from json. 
	if lastImage!=latest:
		print("There's a discrepancy between the pagination file (page.txt) and the json file. The latest element in the json file is: "+str(latest)+" in the page: "+latestPage+" update page.txt to the page and number of the last element in json file otherwise you risk data corruption")
		match=False
	else:
		match=True
#If page.txt file doesn't exist
except FileNotFoundError :
	#If latest is -1 then json is empty and it is the first time the code is run
	if latest != -1:
		match=True
		pass
	#If not, the page.txt file has been deleted and it has to be created based on the last image scraped
	elif latest == -1:
		match=True
		pass
	else: 
		print("There's a problem, json file says that last element is:  "+str(latest)+ "but no page file has been found. Create a page.txt file in the same directory of this script and add the following line "+latestPage+","+str(latest))
		match=False

#!!!!!!IMPORTANT!!!!! currentPath has to be changed to YOUR current desktop path
currentPath="/Users/omarpadierna/Desktop/"
#assume image integrity is not correct
integrity=False
#If there are elements in the Json file then check all of them have their respective image downloaded
if match==True:
	#If json file is not empty then check for image integrity
	#if latest != -1:
		#get image integrity
		#integrity= imageIntegrity(currentPath)
	#Check if job is finished. If latest entry is 12086 and image integrity is true a message saying job is finished will appear	
	#jobFinished(latest, integrity)
	#Run job
	runJob()






