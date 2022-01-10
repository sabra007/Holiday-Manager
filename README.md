# Holiday Manager
This is an applicaation that tracks holidays.

When the program starts it loads initial holiday data from the given json file.
Then it scrapes additional holidays from https://www.timeanddate.com/holidays/us/ the present year, 2 years of past holidays, and 2 years of future holidays.


After that it will show menu options for interactions.



Sample run

```
Holiday Management
===================
There are 2562 holidays stored in the system.

Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
Enter 1-5: 1

Add a Holiday
================
Holdiay Name: holiday 4
Date: 2022-1-10
holiday 4 (2022-01-10) was added to the list.

Holiday Management
===================
There are 2563 holidays stored in the system.

Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
Enter 1-5: 2

Remove a Holiday
================
Holdiay Name: Christmas Day  
Date: 2024-12-25
Success:
Christmas Day (2024-12-25) has been removed from the holiday list.

Holiday Management
===================
There are 2562 holidays stored in the system.

Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
Enter 1-5: 3

Saving Holiday List
================
Are you sure you want to save your changes? [y/n]:y
Success:
Your changes have been saved.

Holiday Management
===================
There are 2562 holidays stored in the system.

Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
Enter 1-5: 4

View Holidays
=================
Which year?[2020-2024 Leave blank for the current year]:
Which week? #[1-52, Leave blank for the current week]: 
Would you like to see this week's weather? [y/n]: y
get weather Called

These are the holidays for this week:
Stephen Foster Memorial Day (2022-01-13) - Weather not avaliable at this time
Orthodox New Year (2022-01-14) - Weather not avaliable at this time
World Religion Day (2022-01-16) - Weather not avaliable at this time
h1 (2022-01-10) - -3.7 F, Sunny
h2 (2022-01-11) - 21.5 F, Overcast
h3 (2022-01-12) - 22.4 F, Mist
holiday 4 (2022-01-10) - -3.7 F, Sunny

Holiday Management
===================
There are 2562 holidays stored in the system.

Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
Enter 1-5: 4

View Holidays
=================
Which year?[2020-2024 Leave blank for the current year]: 2021
Which week? #[1-52, Leave blank for the current week]: 25

These are the holidays for 2021 week #25:
International Day of Yoga (2021-06-21)
International Day of the Celebration of the Solstice (2021-06-21)
West Virginia Day observed (2021-06-21)
Public Service Day (2021-06-23)
International Widows' Day (2021-06-23)
Day of the Seafarer (2021-06-25)
International Day Against Drug Abuse and Illicit Trafficking (2021-06-26)
International Day in Support of Victims of Torture (2021-06-26)
Micro-, Small and Medium-sized Enterprises Day (2021-06-27)

Holiday Management
===================
There are 2562 holidays stored in the system.

Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
Enter 1-5: 5

Exit
================
Are you sure you want to exit? [y/n]: y
Goodbye!
```



## Flowchart
___
![Flowchart](./flowchart.png)


Holiday data from: https://www.timeanddate.com/holidays/us/
Weather data from: https://rapidapi.com/weatherapi/api/weatherapi-com/
