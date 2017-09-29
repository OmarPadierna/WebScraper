# WebScraper


This is a web scraper that I wrote for a friend. The task was to download the images in a database and scrape some information related to that image. This information is planned to be stored in a json file. 

This code uses Selenium (to click on buttons around the website) and scrapy (to scrape the info and download the images)

Since the way I configured selenium was too fast for the DOM, sometimes the program would throw an error. Although there is error handling in the code, it is pretty bad since it doesn't say much. Most issues were related to selenium trying to find an element that the DOM hadn't loaded yet.

Because of this the process of downloading the images and scraping the data was interrupted. Since the database is too large and it was meant for a classification problem it was important to ensure data integrity. It is because of this that every time the task was executed the first function to run was one that ensured data inegrity (i.e. that the entries in the json file corresponded to the number of downloaded images).

Selenium would then navigate to the latest downloaded image and resume the task from there. 

This code has not been refactored and it was meant to be run by me (my friend only wanted the json file and the image). Since I understood what the code did exactly and modified it on the fly as I encountered errors, there is a high chance that it will not work out of the box. 

The general logic of the code and how each python file is related (and their order of execution) can be found in the image file. 
