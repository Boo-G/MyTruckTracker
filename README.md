# Team-28 CMPT 370


## Required Software

Before running MyTruckTracker, make sure to have python3 downloaded (built using python 3.9.13). The rest of the required extensions will be downloaded when you run the exeutable in the coming steps. 

The executable will automatically download: Django, Django_hosts, django-storage-url, pillow, pywebview, and psycopg2-binary.

## First Start (for non demonstration)

Prior to running the service, an administrator account should be created to take full advantage of the features available. To do this you will have to navigate to the folder "team-28-cmp-370" in the console, and run the command "python3 manage.py createsuperuser". This will initiate the initial creation of an administrator for the service. Following the requested inputs will complete the administrator creation. 

## Starting the service

To run the project, first you will need to download the project. You will then need to navigate to the folder "team-28-cmp-370" and run the file named "MyTruckTracker". 
_**Note:** If you are on a Linux, or macOS based system you will need to navigate to the file location and run the command "bash ./MyTruckTracker"_ 

This executable will run and open the website on your default internet browser.

## Getting Started
Upon starting the service in the clients case the databases will be empty, however for testing purposes the databases will have information provided for ease of demonstration.

You will be able to create a user or login, the default admin login is: 
username: admin 
password: 123

Once logged in you will have access to certain pages depending on if you are a manager (administrator) or a regular employee. These pages can be accessed by using the navigation bar located at the top of the screen. 

**Shared Views:**

Home screen- 
The home screen allows for users to check out and sign in vehicles

Profile - 
This screen shows all information pertaining to the current logged in user. This includes the vehicles, tickets, personal vehicle requests, and accidents that are assigned to them. 

Search Bar - 
You are able to use the search bar to search for information relating to users or vehicles. This includes license plates, make, model, year, and from users first name, last name, username or email. This will then create hyper links that allows you to view more information based on the results. 

Filtered search -
The filtered search drop down has three options: Vehicles, Users, and expenses 
    Vehicles - This will show all the vehicles in the database and allow for the displayed values to be sorted by: VIN, Brand or Employee.
    Users - This will show all the users in the database and allow for the displayed values to be sorted by: First name, employee ID, and if they are a manager
    Expenses - This will display all of the expenses that are in the database. This also displays the personal vehicle requests that are open


add- 
There are two options for adding: ticket, expenses
    Tickets - Allows for the user to add in information relating to vehicle infraction tickets associated with the vehicle
    Expenses - Allows for the user to submit expenses related to costs assocaiated with the vehicle, including oil changes, tire replacements and other work completed on the vehicle.
    Personal Vehicle Trip - Allows for the user to submit a form for the user to request reimbursement for a trip made with their personal vehicles.
    Accident - Allows for the user to complete and submit a form with information about an accident

**Admin View:**

add- 
There are two options for adding that can only be accessed by an admin: vehicles, users
    vehicles - Displays a form to be completed to add a vehicle to the database. From this you can also add a new license plate aswell.
    users - Displays a form to be completed to add a user to the database. This also adds the user as an account that can be logged in from. To see information on reuirements for password and username, hover over the words "password" and "username" respectively.

Admin Portal- 
There are two options within the admin portal: admin approvals, and view databases
    admin approvals - Displays approvals that admins (managers) need to approve, such as expenses and personal vehicle requests. Also within this screen a total count of vehicles, expenses and users is displayed. 
    view databases - displays all of the database entries, with buttons allowing for the each entry to be edited or deleted.

Filtered Search-
    Accidents - Displays the current accidents on record


 
