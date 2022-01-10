import datetime as dt
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from pprint import pprint
import time

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

class Holiday:
    def __init__(self, name, date):
        self.name = name
        self.date = date


    def __str__ (self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date})"

    def __eq__ (self, other):
        return (self.name == other.name and self.date == other.date)

# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    def __init__(self):
        self.innerHolidays = []
        self.changes = False
        self.running = True

    # this function has been copied from stackoverflow
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    
    # def validate(self, date_text):
    #     print("do i even get here")
    #     try:
    #         dt.datetime.strptime(date_text, '%Y-%m-%d')
    #     except ValueError:
    #         print("Incorrect data format, should be YYYY-MM-DD")

    def  addHoliday(self):
        self.changes = True
        # temp input will be separrated later
        date = ""

        # while isinstance(date):
        #     date = input("Enter date: ")
        #     self.validate(date)
        #     print("invalid date")
        #     date = input("Enter date: ")

        # holiday = input("Enter holdiay: ")

        # holli = Holiday(holiday, date)
        # self.innerHolidays.append(holli)
        print("holiday has been added")

        ####

    def addHolidayHelper(self, holidayObj):

        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday            
        # print to the user that you added a holiday

        if isinstance(holidayObj, Holiday):
            if holidayObj not in self.innerHolidays:
                self.innerHolidays.append(holidayObj)
                print(f"{holidayObj.name} ({holidayObj.date}) was added to the list.")
        else:
            print(f"{holidayObj} is not a Holiday object.")
           
        

    def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        pass
    def removeHoliday(self):
        self.changes = True
        print("remove holiday called")
        pass

    def removeHolidayHelper(self, HolidayName, Date):
        print("remove holiday called")
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        pass


    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

        with open(filelocation, 'r') as j:
            holidays = json.loads(j.read())

        for holiday in holidays['holidays']:
            date = holiday['date']
            holiday_name = holiday['name']

            self.addHolidayHelper(Holiday(holiday_name, date))
        

    def save_to_json(self):
        
        while 1:
            choice = input("Are you sure you want to save your changes? [y/n]:")

            if choice == 'y':
                self.save_to_json_Helper('holidays.json')
                break;
            elif choice == 'n':
                print("Canceled:\nHoliday list file save canceled.")
                break;
            else:
                print('Invalid input. Try again.\n')


    def save_to_json_Helper(self, filelocation):

        # Write out json file to selected file.
        # get the data from holiday objectd as dictionaries

        serialized = [holiday.__dict__ for holiday in self.innerHolidays]

        f = dict()
        f['holidays'] = list(serialized)

        holidays_json = json.dumps(f)

        with open(filelocation, 'w') as j_file:
            j_file.write(holidays_json)
        self.changes = False
        print("Success:\nYour changes have been saved.")


    
    def getHTML(self, url):
        response = requests.get(url)
        return response.text

    def scrapeHolidays(self):
        self.changes = True
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years 
        # by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.

        for x in range(dt.date.today().year-2,dt.date.today().year+3):

            html = self.getHTML(f"https://www.timeanddate.com/holidays/us/{x}")
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('tbody')
        
            for row in table:

                holiday_name_tag = row.find('a')                
                try:
                    date_tag = row['data-date']
                except KeyError:
                    continue
                        
                if holiday_name_tag is None:
                    continue
                else:
                    name = holiday_name_tag.text
                    date = dt.datetime.utcfromtimestamp(int(date_tag)/1000).strftime('%Y-%m-%d')
                    
                    self.addHolidayHelper(Holiday(name, date))


    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    
    def filter_holidays_by_week(year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        pass

    def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        pass

    def getWeather(weekNum):
        print("get weather Called")
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        pass
    
    def viewCurrentWeek(self):
        print("view holidays Called")
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass


    def exit(self):

        st = ""
        while 1:
            if self.changes:
                st = "\nYour changes will be lost.\n"
           
            choice = input(f"Are you sure you want to exit? {st}[y/n]")

            if choice == 'y':
                self.running = False
                print("Goodbye!")
                return
            elif choice == 'n':
                print("Canceled exit.")
                return
            else:
                print('Invalid input. Try again.\n')

    def printList(self):
        
        for h in self.innerHolidays:
            print(h)

def printMenu():
    print("1. Add a Holiday")
    print("2. Remove a Holiday")
    print("3. Save Holiday List")
    print("4. View Holidays")
    print("5. Exit")

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object

    holidayList = HolidayList()
    # holidayList.addHolidayManually()
    # holidayList.addHolidayManually()
    
    # 2. Load JSON file via HolidayList read_json function
    print("Loading data from file")
    time.sleep(1)
    holidayList.read_json('holidays.json')

    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    print("Scraping holidays")
    time.sleep(1)
    holidayList.scrapeHolidays()


    # 4. Create while loop for user to keep adding or working with the Calender
    # holidayList.printList()
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    
    while holidayList.running:
        print("\nHoliday Management")
        print("===================")
        print(f"There are {holidayList.numHolidays()} holidays stored in the system.")
        printMenu()
    
        while 1:
            user_choice = input("Enter 1-5: ")
            if user_choice.isdigit() and int(user_choice) > 0 and int(user_choice) <= 5:
                choice = int(user_choice)
                break;
            else:
                print("Invalid Input. Try again.")
        
        menu = [holidayList.addHoliday, holidayList.removeHoliday, holidayList.save_to_json, holidayList.viewCurrentWeek, holidayList.exit]
        menu[choice-1]()



if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





