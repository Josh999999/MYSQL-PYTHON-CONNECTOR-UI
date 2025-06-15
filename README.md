# MYSQL-PYTHON-CONNECTOR-UI
The MYSQL-Python-connector-User Interface is a user interface tool that allows users who have a 
MYSQL database to interact with it through a visual database, allowing the user to view, tables, databases, 
and the contents within them. It also allows users to update the structure of their database by:   
- **CREATING tables**
- **DROPING tables**
- **CREATING databases**
- **DROPPING databases**

<br>
    
It also allows users to generate their queries in a more user-friendly way than the SQL language, instead of having to know SQL users can retrieve the 
filtered information they need from a table using list boxes and drop-down boxes.
This itself is not very special as the MYSQL workbench allows users to manipulate the structure of their database manually and many other DBMS’s 
have ways to queries a database through a UI. The special thing about the MYSQL-Python-connector-User Interface it that it returns the query that it 
runs (using the MYSQL-Python connector) back to the user. This is useful as it helps people who have no interest in learning SQL or can’t use it; 
still generate queries that are specific to their database. From here they can use these returned queries for two purposes:
- **1.** - To help them learn SQL easier by giving them an in depth look at how the query directly affects that database.
- **2.** - To put them into their own application that uses their personal MYSQL database (e.g., a web app) 


---


## Running the site
To run the application in it's current state you will need to follow the current steps


### Step 1. Download requirements
Download the current python version of the libraries used in this project using the requirements.txt file
```
pip install -r requirements.txt
```
<br>


### Step 2. Install MySQL
Install MySQL to give the application a database to connect to
<br>
Download at: https://dev.mysql.com/downloads/installer/

<br>


### Step 3. Create the MySQL Database
Create a Database called "world" that the application will use as its anchor database
```
CREATE DATABASE world;
```
<br>


### Step 4. Run the web application using python
Run the application using the python
```
python Main_sys.py
```
<br>


### Step 5. Run the web application using python
Log into the connector with the details you set when creating the MySQL server
```
Username: root
Password: root
```
<br>


---


## Brief look at the project:

Here we will have a brief look at the user interface going through what it can do with brief descriptions to get a good idea of what it is and what it can help achieve.
  

### Log-in screen:
![image](https://user-images.githubusercontent.com/87393875/195882288-26f6094e-e957-4f8b-9029-ef69702c2ba8.png)

<br>

<br>


### Create user screen:
![image](https://user-images.githubusercontent.com/87393875/195882330-6861ea85-5a86-4485-bde5-a43190d4f351.png)


The create user screen will allow you to create a user with the MYSQL-Python-connector-User Interface. 
Note that the user you create must be an existing one with the MYSQL server client, if it is not the connector won’t 
be able to establish a connector with the MYSQL server (this means all the details need to be 100% accurate)

The login-in screen is simply a way to validate all users to make sure that they have the permissions to be accessing 
the database. 

Note that the MYSQL-Python-connector-User Interface uses the RSA encryption algorithm (Euler.py) to encrypt all users 
usernames and passwords for the principle of safety.

<br>

<br>


### The main page:
![image](https://user-images.githubusercontent.com/87393875/195882514-61bb635d-75fc-473f-9eb6-ef271e027ae4.png)

This is the main page of the connector, from here you can perform all the main operations that the system can perform 
(listed in the project description section)

As you can see on the right you can select a database from your connection (this will create a new connector in the 
session connected to that database), from there you can view the tables inside on that database 
(these are displayed in the tables section), and finally from there you may select a table 
of your choosing and its content (attributes, records, etc) will be displayed on the right hand side of 
the “Current Table block”

<br>

<br>


### A quick example:
![image](https://user-images.githubusercontent.com/87393875/195882608-837e3ff0-a665-4fa8-afbd-1801a9145d76.png)

This image here showcases one of the biggest features of the connector its ability to allows the user to query 
the database in a user-friendly way. 
As you can see here after clicking the “SELECT” button on the right this menu appears under the “Manipulate table” block, 
this is filled with all the attributes of the table in a tick box list where the user can select which ones they want 
to display. 

It also has a “WHERE” section, in this section a 
user can filter records by deciding which pieces of information in an attribute in the table they would like to display 
(In this example all of the attributes but “CountryCode” have been chosen to be displayed, and the table has been filtered 
to only display records WHERE the ID attribute is equal to 2)

Finally the circled spot at the bottom named “SQL Statement Output” will display the output 
from the query (the data it returns), and it will return the query that was used to generate this data.



