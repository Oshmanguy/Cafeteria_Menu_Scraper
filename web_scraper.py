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

beautiful_page_contents = BeautifulSoup(web_page.text, "html.parser")

#print(beautiful_page_contents.find_all('div', id = "WeeklyMenu-Monday"))


def getSpecificDay(soup, day_of_week):

    #get a getSpecificDay of the week (certain div id)
    soup_day = soup.find("div", id = ("WeeklyMenu-" + day_of_week))
    
    #return contents for that specific day 
    return soup_day


def getMealItems(soup, meal):

    #get h3 tag that holds title of meal  (then we can get everything within h3)
    #TODO: FIX THIS STUPID THURSDAY BUG, SOMTHING IS DIFFRENT BUT I DONT KNOW WHAT 
    if meal == "Thursday":
        #this is stupid as hell
        meal_h3 = soup.find('h3', string = "&#160;" + meal)
    else:
        meal_h3 = soup.find('h3', string = meal)
    
    if not meal_h3:
        print("NO " + meal + " found")
        return []

    #get the tr that contains the meal HEADER
    current_tr = meal_h3.find_parent("tr")

    #empty list that holds meal items (text inside p tags)
    meal_items = []

    #loop through each tr tag and see if there is a p tag inside of it
    for tr in current_tr.find_next_siblings("tr"):

        #stop once all the meal items are in list (hit a h3 tag)
        if tr.find("h3"):
            break
        
        #extract all visible text from p tags and saves them to var
        for p in tr.find_all("p"):
            text = p.get_text(strip = True)

            #adds meal item to list
            if text:
                meal_items.append(text)

    #return list of lunch items
    return meal_items

#create a dict that which values contain a list containg meals for that meal time


#MAIN PROGRAM -----------------------------------------------------


#days of week list
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

#database that will hold supper and lunch lists for all days of the week
meal_database = {}

#loop through each day of the week
for day in days_of_week:
   
    #get all meal html for that day (under certain div id)
    specific_day_soup  = getSpecificDay(beautiful_page_contents, day)
    
    #save entry to dict with key being day of week and keys being list of lists (lunch and supper)
    meal_database[day] = {"lunch": getMealItems(specific_day_soup, "LUNCH"),
                          "supper": getMealItems(specific_day_soup, "SUPPER")}


    print("==================================================================================================")
    print(day)



print(meal_database)
