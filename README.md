# YOUR PROJECT TITLE    "Family Health Tracker"
#### Video Demo:  <URL https://youtu.be/fkSvATlmiXU> 


#### Description:

For my final project, I decided to make a web application and, having young children, I thought a good idea would be a family health tracker that would allow monitoring of temperatures taken, medication given and symptoms added to the app.

&nbsp;

Part of my reason for choosing this was when the children are ill, especially at night, you can check when any medication was last given or what a previous temperature was on the app, especially if this was done by my wife, and she is now sleeping I wouldn't have to wake her up to find out, or if the children's grandparents were babysitting for us, they wouldn't need to contact us to find out this information they could just check the app.

&nbsp;

The app allows a person to create a user account and password to create a secure login for the app. Once logged in, you can create a patient by inputting name, age (date of birth), height and weight and this person will then appear as a patient within the app. On the patient side of the app, you can also update all patient information: date of birth, height, weight but not the name. There is also the option to delete the patient and all patient data from the app.

&nbsp;

When a patient has been created, you can then start updating them with temperatures taken, medication given and track symptoms.

&nbsp;

There are two ways to input information into the patient. The first way is to use the patient dashboard, where you can see a quick breakdown of the three main areas for the patient in table format. These are the last 5 temperatures taken, the last 5 medications given, and the last 5 symptoms recorded on the dashboard. There is also a line graph linked to the temperature table and this will start to populate when temperatures are added.

&nbsp;

On this dashboard page for the patient, you can update all three of the main tables directly from this screen by filling out the required information in the accordion-style dropdown at the bottom of each table.

&nbsp;

The second way of inputting this information is to go directly to the temperature, medication or symptom page. On these pages there is a dropdown selection for the patient. If the user has created more than one patient, then all patients will be listed in the dropdown box in order for the user to make a selection. Then you just need to complete all the remaining relevant information in the required boxes, e.g. temperature, medication given, medication amount, symptoms and the date and time, click the update button and this will update the patient information.

&nbsp;

For the medication options, I have created a small list that can be chosen from the dropdown menu, but the input field also allows free text to be written in as well.

&nbsp;

While the dashboard shows a small graph linked to the temperature, it only shows the 5 temperatures in the temperature table, there is also a temperature graph page which, after selecting the patient from the dropdown selection, will show a larger graph showing the last 10 temperatures taken for the patient.

&nbsp;

The app also has a page of useful links, as I live in the UK these links point to the different NHS (National Health Service) providers in the four countries that make up the UK (Wales, England, Scotland and Northern Ireland) as well as the NHS none emergency 111 online service.

&nbsp;

The app also allows a user to download all the patient data for a person. This is downloaded as a CSV file and contains all the data held in the database for the patient. This could then be given to a doctor or health provider and may be useful. The option to download the patient data can also be done from the individual patient dashboards.

## Installation

I have built and run this project on Visual Studio Code.

Install VSCode if needed.

In VSCode command pallet (Ctrl+Shift+p)
git: clone (install git for windows if needed)
clone my github project repository:
https://github.com/Martin9090/CS50Final-Project.git

Open a powershell terminal and run the following commands one at a time, these commands will install Python, allow the apllication to execute, create a virtual enviroment for the application to run in, install dependencies and requirements and run the application:

winget install --id Python.Python.3.11 -e --source winget

python.exe -m pip install --upgrade pip

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

py -3 -m venv .venv

. .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

python -m pip install -r requirements.txt

python -m flask run --host=127.0.0.1 --port=5000

The terminal should show:
Running on http://127.0.0.1:5000 (or something similar) click on the link in the terminal to open the browser page.

## Tech Stack

- Python 3.11
- Flask
- SQLite
- Bootstrap
- Werkzeug

## Files in my project and app.py

#### <ins>project.db</ins>

The project makes extensive use of a sqlite3 database to store all the relevant data that makes the app work.

The database is separated into 5 different tables:

#### <ins>users</ins> - this stores all the user information:

id

username

hash (hashed user password)

#### <ins>patient</ins> - this stores all the patient information:

id

name

age (date of birth)

height

weight

user_id (id of the user that added the patient to the database).

#### <ins>temp</ins> - this stores all the temperature information:

patient_id

user_id

current_time (actual date/time the entry was added to the system)

seleceted_time (the user inputted date/time of when the temperature was taken)

temp

##### <ins>symptom</ins> - this stores all the symptom information:

patient_id

user_id

current_time (actual date/time the entry was added to the system)

seleceted_time (the user inputted date/time of when the temperature was taken)

symptom (free writing text field)

#### <ins>medication</ins> - this stores all the symptom information:

patient_id

user_id

current_time (actual date/time the entry was added to the system)

seleceted_time (the user inputted date/time of when the temperature was taken)

medication (free writing text field)

dosage (free writing text field)

#### <ins>Layout.html</ins>

The layout creates the top navigation bar and bottom of every page of my project.

&nbsp;

Before logging in to the app, it only allows the register and login buttons to show on the top right and the app logo in the top left. The logo itself is also a link back to this homepage.

&nbsp;

After the user has logged in, the navigation bar changes with multiple dropdown menus and more links and replaces the register and login links with account and logout.

&nbsp;

When I first created the app the navigation bar just kept growing as I added more links. It was when a friend of mine saw it and asked why I hadn't created a dropdown menu for the ones that could be grouped together. It was from that I looked at the boostrap framework that the app is using anyway to create dropdown menus in the navigation bar.

&nbsp;

I created a logo for my app using AI online through the website design.com.

#### <ins>homepage/index.html</ins>

The homepage gives a description of the app along with the features it has and how it works along.

#### <ins>register.html / login.hrml</ins>

The register screen has 3 boxes for inputting a username, password and re-typing the password. If any of the boxes are left empty before submitting the information, it will show an error advising what is missing username, password etc. or if the username is already in use.

&nbsp;

The password the user has inputted is hashed using werkzeug utilities and stored in the database using an SQL query along with the other details.

&nbsp;

Once the user has registered, it redirects to the login screen ready for the user to login.

&nbsp;

Login has a username and password box, if either field is left empty, an error is shown. After a successful login, the user is moved to the patient's page.

#### <ins>patients.html</ins>

For a new user, this page is empty with a button for adding a new patient, but for a user with patients already in the system, this page displays a list of all the patients in a table with a link to their patient dashboard. Below the table is also a link to delete patient data.

An SQL query is made for the patient information when the page loads, populating the table.

#### <ins>add_patinet.html</ins>

This page has 4 fields to complete patient name, date of birth, height and weight. Any field not completed will produce an error. This information is then used to check if this user has already input a patient with the same name and produce an error if one is found otherwise, it stores the user in the database along with the user_id of the user that has added the patient (see projects.db entry above).

After entering a new user, the app sends you back to the patient's screen where the new patient should now be showing.

#### <ins>update.html / updateone.html</ins>

Update has a single dropdown field. In this dropdown is a list of all the patients that the user has added to the app. The dropdown list uses a SQL query when the page loads, creating the list of patients for selection.

When the user makes a selection and clicks the select button, the system renders the update_one page.

The update_one page shows the patient's name along with 3 fields: date of birth, height and weight. These fields are pre-populated with the current details of the patient. These can be changed and the patient data updated using the update button at the bottom of the form.

&nbsp;

Again, if any of these fields are deleted or left blank, an error will be shown to the user.

&nbsp;

Completing the information, a SQL query then updates the database with the new information and the user is then sent back to the patient's page.

#### <ins>download.html</ins>

I wanted to add a way to download all patient information that had been added to the database, as with update this screen only has a single dropdown field for the patient to be selected and a button to create the download file.

&nbsp;

When a user is selected 4 SQL queries or made to get the information from each of the 4 tables patient, temp, medication, symptom for the selected patient, it stores these in variables to be picked up by the CSV write function. Originally, I tried to use a single query to pull all the information out of the tables in one query, but I would always end up with thousands of additional lines being produced in the CSV file unnecessarily.

&nbsp;

&nbsp;I have had a lot trouble getting this to work as I wanted it looking through a lot of documentation and stack overflow forums, but in the end, I used ChatGPT to get the function working as I wanted, allowing me to write each variable file into the CSV file with the column headings as the headings on the file and then writing the next file in creating another line of headings from that file and so on.

Once the CSV file has been completed, it uses send_file to pass the CSV to the browser for download and then deletes the file from the app so constant download requests won't create unnecessary files that take up space.

#### <ins>delete.html</ins>

I felt there should be an option on the app to remove all the data for a patient and delete the patient.

This page has a single input field where the username has to be typed in order to delete the patient and all data. I wanted to make a type-in field rather than a dropdown to stop any accidental deletion of data. When you mouse over the field, a tooltip appears(bootstrap) that the field is case-sensitive so the user has to type the patient's name in exactly as it is in the app in order to allow deletion.

&nbsp;

When the delete data button is pressed, the patient data is deleted from all tables and then the patient is deleted from the app.

#### <ins>temperature.html</ins>

As with other pages, this has a patient select dropdown field to choose the patient, a field to input temperature and a date/time selection box. If any of these fields are left blank, an error message will be shown. When complete and the update button pressed the data will be added to the temp table in the database (see projects.db entry above).

When the page first loads, it also includes a table of the last 10 temperatures taken according to the selected_time column in the database. This shows the patient's name, the user that made the entry, the time taken (user selected) and the temperature.

#### <ins>medication.html</ins>

This page is very similar to the temperature page with a dropdown for patient selection. The field for inputting the medication is both a selection field to which I have already inputted several commonly used medications, I created this with the use of a list, but the field itself is also free entry text. A field for the amount given with a dropdown selection box next to it to choose between ml, mg and tablet as the most common weight/measures of medication along with date and time.

If any of these fields are left blank, the user will receive an error. When complete and the update button pressed the data will be added to the medication table in the database, I have concatenated the amount given and the unit of measure into a single entry before it is entered into the database (see projects.db entry above).

The same as temperature when the page first loads, it also includes a table of the last 10 medications given according to the selected_time column in the database, this shows patient name, the user that made the entry, the time taken (user selected), medication and amount given.

#### <ins>symptoms.html</ins>

Like both temperature and medication, this has a dropdown for patient selection a field to enter the symptom and date/time.

If any of these fields are left blank, the user will receive an error, when complete and the update button pressed, the data will be added to the symptom table in the database. I have concatenated the amount given and the unit of measure into a single entry before it is entered into the database (see projects.db entry above).

&nbsp;

The same as temperature and medication when the page first loads, it also includes a table of the last 10 symptoms recorded according to the selected_time column in the database this shows the patient's name, the user that made the entry, the time taken (user selected) and symptoms.

#### <ins>graph.html / graphone.html</ins>

As a way of showing a possibly easier to see representation of a patient's temperature over time, I wanted to show the data in a line graph format. The graph page has a single dropdown field for patient selection. When the submit button is pressed, the graphone page is rendered.

The graph uses chart.js to produce the graph using a SQL query to pull the data from the temperature database. I store the data in 2 dictionary variables for date and temperature so I can use them in the creation of the graph.

I did have some trouble getting this working as many online resources didn't have exactly what I needed, and again I turned to ChatGPT to solve this issue for me.

The graph shows the last 10 temperatures taken for the patient according to the selected_time column in the database, these are then shown left to right in ascending order of date.

#### <ins>links.html</ins>

This page has a number of web links for the different NHS websites within the UK.

#### <ins>dashboard.html</ins>

From the patient's page, each patient has a dashboard link that sends them through to the dashboard page. When it does that, it also passes through the patient id at the same time.

The dashboard page is split into a 2x2 grid, this makes extensive use of the CSS grid layout and responsive web design in order to adjust the grids upon screen reduction.

The grids contain a table of the last 5 temperatures, medication and symptoms for the patient and the 4th grid contains a graph displaying the 5 temperatures in the temperature grid.

The temperature, medication and symptom grids each have an accordion-style dropdown (bootstrap) where new information can be added. As we are already on the patient's dashboard, the patient's name does not need to be selected, the patient id is held on the page in a display:none input tag for use, but in each grid the remaining fields are the for inputting the data. If there are any empty fields before submitting the user will be shown an error.

Under the patient's name, at the top of the page is a button to download the patient data, this works the same as the download data page, but again you do not need to select the patient's name as it is already on the page and will produce the download.

#### <ins>helpers.py</ins>

This contains callable functions these are:

apology - shows the error screen and message

login_required - ensure user is logged in to the see the information otherwise sends them back to the login screen.

calculate_age - this takes the date of birth and uses the current date and returns the age of the patient in years.

datetime_change - this takes the date time from the database and change into a different format for displaying on screen.

time - this returns the current date time and can be called with the shorter function of time.

### <ins>While making this project I used the following resources:</ins>

CS50X course material

W3Schools

Geek for geeks

Stack overflow

Bootstrap

AI used for logo design website design.com

AI used for assistance with coding ChatGPT.
