import datetime as dt
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from pprint import pprint
import time
import config

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

    def as_dict(self):
        return {'name': self.name, 'date': str(self.date.date())}

    def __str__ (self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date.date()})"

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

    def getValidDate(self):
        while 1:
                    
            date = input("Date: ")

            date_string = date
            date_format = '%Y-%m-%d'

            try:
                date_obj = dt.datetime.strptime(date_string, date_format)
                # date = date_obj.strftime('%Y-%m-%d')
                return date_obj
                
            except ValueError:
                print("Incorrect data format, should be YYYY-MM-DD.")

    def getHolidayName(self):
        while 1:
            holiday = input("Holdiay Name: ")
            if not holiday:
                print("Holiday name can't be empty. Try again.")
            else:
                return holiday
                

        
    def  addHoliday(self):
        print("\nAdd a Holiday")
        print("================")     
        self.changes = True
    
        holiday = self.getHolidayName()
        date = self.getValidDate()
        self.addHolidayHelper(Holiday(holiday, date))
             

        ####

    def addHolidayHelper(self, holidayObj):

        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday            
        # print to the user that you added a holiday

        if isinstance(holidayObj, Holiday):
            if holidayObj not in self.innerHolidays:
                self.innerHolidays.append(holidayObj)
                print(f"{holidayObj} was added to the list.")
        else:
            print(f"{holidayObj} is not a Holiday object.")
           
        

    def findHoliday(self, HolidayName, Date):

        holiday = Holiday(HolidayName, Date)

        if holiday in self.innerHolidays:
            return holiday
        else:
            print(f"Error {HolidayName} ({Date.date()}) not found")
        

    def removeHoliday(self):
        print("\nRemove a Holiday")
        print("================") 
        self.changes = True
        name = self.getHolidayName()
        date = self.getValidDate()

        self.removeHolidayHelper(name, date)
        

    def removeHolidayHelper(self, HolidayName, Date):
      
        # Find Holiday in innerHolidays by searching the name and date combination.
        holiday = self.findHoliday(HolidayName, Date)
        
        if holiday is None:
            return
        else:
            # remove the Holiday from innerHolidays
            self.innerHolidays.remove(holiday)
            
            # inform user you deleted the holiday
            print(f"Success:\n{holiday} has been removed from the holiday list.")
      
        
    
    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        try:
            with open(filelocation, 'r') as j:
                holidays = json.loads(j.read())
        
            for holiday in holidays['holidays']:
                date = holiday['date']
                holiday_name = holiday['name']
                new_date = dt.datetime.strptime(date, '%Y-%m-%d')

                self.addHolidayHelper(Holiday(holiday_name, new_date))
        except:
            return

    def save_to_json(self):
        print("\nSaving Holiday List")
        print("================")
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

        serialized = [holiday.as_dict() for holiday in self.innerHolidays]
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
                    new_date = dt.datetime.strptime(date, '%Y-%m-%d')
                    self.addHolidayHelper(Holiday(name, new_date))


    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        holidays = list(filter(lambda x: x.date.isocalendar().week == week_number and x.date.isocalendar().year == year, self.innerHolidays))

        return holidays


    def viewHolidays(self):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        print("\nView Holidays")
        print("=================")
        current_year = dt.date.today().year
        while 1:
            year_input = input(f"Which year?[{current_year-2}-{current_year+2} Leave blank for the current year]: ")
            if not year_input:
                year_input = str(current_year)

            if year_input.isdigit() and int(year_input) in range(current_year - 2, current_year + 3):
                
                while 1:
                    week_input = input("Which week? #[1-52, Leave blank for the current week]: ")
                    if not week_input:
                        self.viewCurrentWeek()

                        break;

                    elif week_input.isdigit() and int(week_input) > 0 and int(week_input) <= 52:
                        
                        self.displayHolidaysInWeek(int(year_input), int(week_input))

                        break;
                    else:
                        print("Invalid Input. Try again.")
                else:
                    continue #Only executed if the innder loop DID NOT break

                break; #Only executed if the innder loop DID break
            else:
                print("Invalid Input. Try again.")


    def displayHolidaysInWeek(self, year, week):

        holidays = self.filter_holidays_by_week(year, week)

        print(f"\nThese are the holidays for {year} week #{week}:")

        list(map(lambda x: print(x), holidays))

    def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        weekNum = dt.date.today().isocalendar().week
        yearNum = dt.date.today().year
        d = dt.date.fromisocalendar(yearNum, weekNum, 1)
        d2 = dt.date.fromisocalendar(yearNum, weekNum, 7)
        start_date = str(d)
        end_date = str(d2)

        url = "https://weatherapi-com.p.rapidapi.com/history.json"

        querystring = {"q":"Minneapolis","dt":start_date,"lang":"en","end_dt":end_date}

        headers = {
            'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
            'x-rapidapi-key': config.api_key
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        weather = response.json()['forecast']['forecastday']
        weather_data = []
        
        for item in weather:
            date_d = item['date']
            temp_t = item['day']['avgtemp_f']
            weather_cond = item['day']['condition']['text']
            weather_data.append({'date': date_d, 'weather': f"{temp_t} F, {weather_cond}"})

        return weather_data
    
    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        current_year = dt.date.today().year
        current_week = dt.date.today().isocalendar().week

        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        current_week_holidays = self.filter_holidays_by_week(current_year, current_week)

        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
       
        while 1: 
            choice = input("Would you like to see this week's weather? [y/n]: ")
            if choice == 'y':
                weather = self.getWeather(current_week)
                print(f"\nThese are the holidays for this week:")
                for holiday in current_week_holidays:
                    wd = next((wd for wd in weather if wd["date"] == str(holiday.date.date())), None)
                    if not wd:
                        print(f"{holiday} - Weather not avaliable at this time")
                    else:
                        print(f"{holiday} - {wd['weather']}")

                break;
            elif choice == 'n':
                self.displayHolidaysInWeek(current_year, current_week)
                break;
            else:
                print('Invalid input. Try again.\n')
        


    def exit(self):
        print("\nExit")
        print("================")
        st = ""
        while 1:
            if self.changes:
                st = "\nYour changes will be lost.\n"
           
            choice = input(f"Are you sure you want to exit? {st}[y/n]: ")

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
    print("\nHoliday Menu")
    print("================")
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
        
        menu = [holidayList.addHoliday, holidayList.removeHoliday, holidayList.save_to_json, holidayList.viewHolidays, holidayList.exit]
        menu[choice-1]()



if __name__ == "__main__":
    main();








