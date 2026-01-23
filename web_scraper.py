#FILE HEADER -------------------------------------HEADER

#This python program scraps data from the usask culinary website
#in order to get data about todays menu. It will then send todays 
#menu via discord. 

#FILE HEADER -------------------------------------HEADER

#imports
from bs4 import BeautifulSoup
import requests
import os
import json
from dotenv import load_dotenv
from datetime import date, datetime, timedelta 


#load enviornment variables so cron can see webhook url 
load_dotenv()

def getSpecificDay(soup, day_of_week):

    #get a getSpecificDay of the week (certain div id)
    soup_day = soup.find("div", id = ("WeeklyMenu-" + day_of_week))
    
    #return contents for that specific day 
    return soup_day


def getMealItems(soup, meal):
   

    #always initalize this to none to avoid errors 
    meal_h3 = None 


    #make get all h3 tags and strip the text in them 
    for h3 in soup.find_all("h3"):
       h3_text = h3.get_text(strip = True)

       #see if the stripped text equals a meal (BRUNCH, LUNCH or SUPPER)
       if h3_text == meal:
           meal_h3 = h3 
           break

    #if LUNCH or SUPPER does not exist then we return empty list and print that the meal was not found
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

def readableMeal(meal_dict, day_of_week):

    #define string
    formated_day = "==========" + day_of_week + "=========\n\n"


    #check if saturday or Sunday (BRUNCH on these days)
    if day_of_week == "Saturday" or day_of_week == "Sunday":


        formated_day += "----------BRUNCH----------\n\n"

        #create internal dict to loop through 
        internal_dict_brunch = meal_dict[day_of_week]["brunch"]

        #loop through items in dict and add them to string 
        for meal in internal_dict_brunch:
            formated_day += meal + "\n\n"

        formated_day += "\n"

        

    #FIRST DO LUNCH MEALS===========================

    formated_day += "----------LUNCH----------\n\n"

    #create internal dict to loop through 
    internal_dict_lunch = meal_dict[day_of_week]["lunch"]
    
    #loop through items in dict and add them to string 
    for meal in internal_dict_lunch:
        formated_day +=  meal + "\n\n"

    formated_day += "\n"
        
    #SUPPER===========================================

    #just add on to original formatted string
    formated_day += "----------SUPPER----------\n\n"

    #create internal dict to loop thorugh (the list, is a value in the dict)
    internal_dict_supper = meal_dict[day_of_week]["supper"]


    #loop through iteems for supper of that day and add to string
    for meal in internal_dict_supper:
        formated_day += meal + "\n\n"

    #returns formated string with everything for that day
    return formated_day


def send_to_discord(message: str):

    #you will have to use your own webhoot here, I have mine saved as an enviornment variable
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    #raise error if no webhook_url of if the url does not work
    if not webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL not set")

    #JSON payload 
    payload = {
        "content": message
    }

    r = requests.post(webhook_url, json=payload)
    r.raise_for_status()

#helper function for send_to_discord 
def send_long_message(text):
    MAX = 1900 #max is 2000
    chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]

    #send over chunks
    for chunk in chunks:
        send_to_discord(chunk)


#MAIN PROGRAM -----------------------------------------------------

#get month name
today = date.today()
#Internation Organization for Standardization (holds dates, times, etc)
iso = today.isocalendar()

#get todays day of week name
day_of_week_name = today.strftime("%A")


#save month name to var and make it lowercase
full_month_name = today.strftime("%B").lower()

#get Monday and Sunday date for url
monday = today - timedelta(days=today.weekday())
sunday = monday + timedelta(days=6)

monday_date = monday.day
sunday_date = sunday.day

#get todays year
year = iso.year                                                                                                                                 
#get week num
week_num = iso.week
week_num -= 1 #have to go back a week since website is behind 


#create URL using todays week and dates
web_url = f"https://culinaryservices.usask.ca/marquis-culinary-centre/week-{week_num}-{full_month_name}{monday_date}-{sunday_date}-{year}.php"


print(web_url)#TESTING


#get contents of web_url at reuqest time and save to varaible
web_page = requests.get(web_url, timeout=10)

#raise error if the url can not be reached 
if web_page.status_code != 200:
    raise RuntimeError("Failed to fetch menu page")

beautiful_page_contents = BeautifulSoup(web_page.text, "html.parser")


#database that will hold supper and lunch lists for all days of the week
meal_database = {}

   
#get all meal html for that day (under certain div id)
specific_day_soup  = getSpecificDay(beautiful_page_contents, day_of_week_name)
    
#save entry to dict with key being day of week and keys being list of lists (lunch and supper)
meal_database[day_of_week_name] = {"brunch": getMealItems(specific_day_soup, "BRUNCH"),
                      "lunch": getMealItems(specific_day_soup, "LUNCH"),
                      "supper": getMealItems(specific_day_soup, "SUPPER")
                     }


#send out payload o7
send_long_message(readableMeal(meal_database, day_of_week_name))

