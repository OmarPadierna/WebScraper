import json
#Declate image object
class Img_Data:
    def __init__ (self):
        self.data = ""
        self.img = ""
        self.img_url= ""
        self.img_path= ""
        self.page=""
        self.parsed_data={}

'''
writeFile receives the array that contains raw scraped information, cleans each element
and saves it in a json file
'''


def writeFile (table):
    #Open json file
    with open('dataset.json') as f:
        #Load data returns a dictionary
        lines=json.load(f)
        #get the dictionary keys and cast as list
        integers=list(lines.keys())
        #Iterate through list and change each key from string to number
        for index,key in enumerate(integers):
            integer=int(key)
            integers[index]=integer
        #Sort the keys and get the latest element
        sortedkeys=sorted(integers)[-1]
    #Add 1 to the latest element and save it for index
    index=sortedkeys+1
    #Iterate crawled data
    for element in table:
        #Extract data and image name
        data=element.data
        img=element.img
        #Get rid of html tags and convert table text into dictionary 
        cleanTags(element, data)
        #Generate path of images. (i.e  inform in which folder the images will be saved)
        generatePath(element,img)
        #Erase data with html tags. Not needed anymore since new data has been saved in parsed_data field
        #element.data=""
        #Convert element (i.e image object) to a dictionary (this is required because to parse json files dictionaries are needed)
        iterable=element.__dict__
        #create small dictionary that wraps index with element dictionary
        dic={index:iterable}
        #update data
        lines.update(dic)
        index+=1
    #Write updated data into json file
    with open('dataset.json','w') as f:
        json.dump(lines,f)
'''
generatePath takes the image name and builds the path in which the image is stored
'''

def generatePath (element,img):
    imgname=img[0:16]
    path="ima/"+imgname
    element.img_path=path

'''
    Code is a bit repetitive, cleanTags function goes line by line and splits each string to 
    get rid of html tags then saves value in its respective key in a dictionary. 
'''

def cleanTags (element, data):
   #Get rid of <tbody> and </tbody> tags
   strip_tbody=data.split("<tbody>",1)[1]
   rows=strip_tbody.split("</tbody>",1)[0]
   #Get rid of all elements with tag <tr>
   strip_tr=rows.split("<tr>",rows.count("<tr>"))
   #Reset rows and turn it into an array
   rows=[]
   dic={}
   internal_dic={}
   #for each row in the array that has elements without <tr>....
   for row in range(1,len(strip_tr)):
    #Save into rows each row but taking away </tr> tag
        rows.append(strip_tr[row].split("</tr>",1)[0])
   for row in range(0, len(rows)):
 
    #Check if row is a header; if so, take tags away then save it as a key.
        if rows[row].count("isic-image-details-table-section-header") !=0:
            sp1=rows[row].split('<td colspan="2" class="isic-image-details-table-section-header">',1)[1]
            key=sp1.split("</td>",1)[0]
            internal_dic={}
        else:
            if rows[row].count("<code>") != 0:
                sp1=rows[row].split("<td>",rows[row].count("<td>"))
                key2=sp1[1].split("</td>",1)[0]
                value_code=sp1[2].split("</td>",1)[0]
                value_code_strip=value_code.split("<code>",1)[1]
                value=value_code_strip.split("</code>",1)[0]
                internal_dic[key2]=value
                dic[key]=internal_dic
            else: 
                sp1=rows[row].split("<td>",rows[row].count("<td>"))
                key2=sp1[1].split("</td>",1)[0]
                value=sp1[2].split("</td>",1)[0]
                internal_dic[key2]=value
                dic[key]=internal_dic
        
    
   #print(dic)
   element.parsed_data=dic






#element=Img_Data()
#element.data='<tbody><tr><td colspan=\"2\" class=\"isic-image-details-table-section-header\">Info</td></tr><tr><td>Unique ID</td><td><code>5436e3afbae478396759f119</code></td></tr><tr><td>Dataset</td><td>ISIC_UDA-1_1</td></tr><tr><td>Created</td><td>October 9, 2014 at 14:36:15</td></tr><tr><td>License</td><td><a target=\"_blank\" href=\"https://creativecommons.org/publicdomain/zero/1.0/\">CC-0</a></td></tr><tr><td colspan=\"2\" class=\"isic-image-details-table-section-header\">Clinical Metadata</td></tr><tr><td>age_approx</td><td>70</td></tr><tr><td>benign_malignant</td><td>benign</td></tr><tr><td>diagnosis</td><td>nevus</td></tr><tr><td>diagnosis_confirm_type</td><td></td></tr><tr><td>melanocytic</td><td>true</td></tr><tr><td>sex</td><td>male</td></tr><tr><td colspan=\"2\" class=\"isic-image-details-table-section-header\">Acquisition Metadata</td></tr><tr><td>Dimensions (pixels)</td><td>1504 \u00d7 1129</td></tr><tr><td colspan=\"2\" class=\"isic-image-details-table-section-header\">Unstructured Metadata</td></tr><tr><td>diagnosis</td><td>Nevus</td></tr><tr><td>id1</td><td>38</td></tr><tr><td>localization</td><td>Back</td></tr><tr><td>site</td><td>bar</td></tr></tbody>'
#cleanTags(element, element.data)
#print(element.parsed_data)
