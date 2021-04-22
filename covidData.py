import requests
import json
import mysql.connector
from mysql.connector import Error

#we are using python 3.7 and mysql.connector 6.1.11

#the code below will automatically log the user in to their database when the program is ran

db = mysql.connector.connect(
    host=" ",
    user=" ",
    passwd=" "
)
mycursor=db.cursor()

#this will be the menu looped for the user to interact with in  a while loop
def print_menu():
    print ("MAIN MENU")
    print ("****************")       
    print ("a. Find General Covid Data by State and Date")
    print ("b. Save Positive Covid Case Increases & # of Covid Deaths Increased by State and Date")
    print ("o. Output all Data Saved")
    print ("q. Exit Program")
    print ("****************\n")

#we set x to 1 as it will be the basis of our while loop    
x = 1  

#while loop will be needed for the main menu code below
while x == 1:          ## While loop which will keep going until x = 2
    print('\n')
    print_menu()    ## Displays menu
    userInput = input('What would you like to do?\n')
    if userInput == 'a':
        #if the user selects a) they'll be asked for the State's abbreviation as well as the date in (yyyymmdd) format
        user_state = input("Enter the state for which the COVID data should be retrieved (e.g. TX):\n")
        user_date = input("Enter the date for which the COVID data should be retrieved (e.g. 20201219): \n")
        response = requests.get("https://api.covidtracking.com/v1/states/"+user_state+"/"+user_date+".json") #we'll inject the user's data in our api url to fecth user specified data
        json_out = response.json()
        #the following code will save the specified data for us to later use to print out statements 
        json_date = json_out['date'] #this line will save data from the json output with the 'date' header
        json_state = json_out['state'] #this line will save data from the json output with the 'state' header
        json_positive = json_out['positive'] #this line will save data from the json output with the 'positive' header
        json_death = json_out['death'] #this line will save data from the json output with the 'death' header
        #code below will print out the data in a way that will be easy for the user to interpret 
        print('\n')
        print ("*****")
        print ("STATE") #header for data
        print ("*****") 
        print (json_state) #prints actual data
        print('\n')
        print ("****") 
        print ("DATE")#header for data
        print ("****") 
        print (json_date) #prints actual data
        print('\n')
        print ("**************") 
        print ("POSITIVE CASES")#header for data
        print ("**************") 
        print (json_positive)#prints actual data
        print('\n')
        print ("****************")         
        print ("CONFIRMED DEATHS")#header for data
        print ("****************") 
        print (json_death)#prints actual data
        print('\n')
        print('Data Retrieved!\n')
    elif userInput == 'b':
        #if the user selects b) they'll be asked for the State's abbreviation as well as the date in (yyyymmdd) format
        user_state = input("Enter the state for which the COVID data should be retrieved (e.g. TX):\n")
        user_date = input("Enter the date for which the COVID data should be retrieved (e.g. 20201219): \n")
        response = requests.get("https://api.covidtracking.com/v1/states/"+user_state+"/"+user_date+".json") #we'll inject the user's data in our url to fecth specified data
        jsql_out = response.json()
        # the following code will save the specified data for us to later use to input into our database
        jsql_date = jsql_out['date'] #this line will save data from the json output with the 'date' header
        jsql_state = jsql_out['state'] #this line will save data from the json output with the 'state' header
        jsql_positive = jsql_out['positiveIncrease'] #this line will save data from the json output with the 'positiveIncrease' header
        jsql_death = jsql_out['deathIncrease'] #this line will save data from the json output with the 'deathIncrease' header
        mycursor.execute("insert into covid.exam1 (u_date,state,positiveIncrease,deathIncrease) VALUES (%s,%s,%s,%s)",(jsql_date,jsql_state,jsql_positive,jsql_death)) #this code injects the data we retrieved into an insert statment for our database
        db.commit() #commits data to our database
        print('You Saved General Covid Data\n')
    elif userInput == 'o':
        #if the user selects o) then we will display all our data saved, by default they will be sorted by a generated unique_id number in ascending order
        print('All Contacts Presented\n') #code added 02/18/21 5:15pm
        mycursor.execute("select u_date,state,positiveIncrease,deathIncrease FROM covid.exam1;") 
        #the following code will show all our data saved in the covid.exam1 database along with a header for the user to understand what the numbers mean
        for p in mycursor: #loop will print all data in table exam1
         print ('\n')
         print("  ----     |-----|---------|----------") 
         print("  Date     |State|New Cases|New Deaths") #header for data
         print("  ----     |-----|---------|----------") 
         print ('\n')
         print(p)   #prints actual data
    elif userInput == 'q':
        #this command will quit our program by breaking our while loop and making x = 2, also will print a statement to communicate the termination of the program
        print('Exit Complete, GoodBye!\n')
        x = 2
        exit    
