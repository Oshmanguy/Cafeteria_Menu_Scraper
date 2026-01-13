#FILE HEADER -------------------------------------HEADER

#This python program scraps data from the usask culinary website
#in order to get data about todays menu. It will then send todays 
#menu via discord. 

#FILE HEADER -------------------------------------HEADER

#imports
from bs4 import BeautifulSoup
import requests

#save url to variable 
web_url = "https://culinaryservices.usask.ca/marquis-culinary-centre/week-2-january12-18-2026.php"

#get contents of web_url at reuqest time and save to varaible 
web_page = requests.get(web_url)

beautiful_page_contents = BeautifulSoup(web_page.text, "html")




print(beautiful_page_contents.prettify())


