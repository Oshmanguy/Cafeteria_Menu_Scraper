#FILE HEADER -------------------------------------HEADER

#This python program scraps data from the usask culinary website
#in order to get data about todays menu. It will then send todays 
#menu via discord. 

#FILE HEADER -------------------------------------HEADER

#imports
from bs4 import BeautifulSoup
import requests

#TODO: get day of the week and current date along with week number to construct url 
#NOTE: URL only needs to change on sunday probably at night maybe anything after 10pm




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


#TODO: fix this function so that I an get brunch and supper for Saturday and Sunday

def getMealItems(soup, meal):
   
    #only look for brunch on saturday and sunday
    if (soup != "WeeklyMenu-Saturday" or soup != "WeeklyMenu-Sunday") and meal == "BRUNCH":
        return []

    #always initalize this to none to avoid errors 
    meal_h3 = None 


    #make get all h3 tags and strip the text in them 
    for h3 in soup.find_all("h3"):
       h3_text = h3.get_text(strip = True)
       print(h3_text)#TESTING


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
            formated_day += meal + "\n\n\n"

        








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

#MAIN PROGRAM -----------------------------------------------------

#TODO: get rid of most of this and make it so that it only sends the url once depending on the day

#days of week list
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#database that will hold supper and lunch lists for all days of the week
meal_database = {}

#loop through each day of the week
for day in days_of_week:
   
    #get all meal html for that day (under certain div id)
    specific_day_soup  = getSpecificDay(beautiful_page_contents, day)
    
    #save entry to dict with key being day of week and keys being list of lists (lunch and supper)
    meal_database[day] = {"brunch": getMealItems(specific_day_soup, "BRUNCH"),
                          "lunch": getMealItems(specific_day_soup, "LUNCH"),
                          "supper": getMealItems(specific_day_soup, "SUPPER")
                         }
    print(readableMeal(meal_database, day))


