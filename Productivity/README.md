# Dashboard

**Project Name:** Dashboard

**By:** Aarav Jalan

[GitHub](http://github.com/AaravJalan)

[YouTube Video](https://www.youtube.com/watch?v=Wny8a105a84)
## Background Information

### About

Dashboard is a productivity website. With useful features such as links, notes and alarms one can remain organised and stay focused on their work. Users can create accounts and use my website to manage their lives. Additionally, customisation features such as dark mode allow them to enhance the website as per their needs.

### Why did I make this Website?

Each of CS50W's projects were challenging in their own ways and required immense brainstorming, understanding and logic.

Choosing an idea for this project was difficult as the previous 5 covered most concepts modern websites have. Managing time & notes has always been a difficult for me and others with a similar problem, so I decided to develop a tool to make this task easier for me.

During the process of programming this website (as well as the others) there were several struggles. I tried to make the website as complex as possible and use it as a chance to improve and polish my concepts of web programming.

After days of thinking, programming and innovating, I am proud to present **Dashboard** - a productivity website designed with tackling the tedious task of organisation.

### Brief Overview

**Dashboard** Contains:
- ToDo Lists with several features.
- Alarms & Stopwatches
- Links (Can be added to the Navbar)
- Progress Page
- Overview Page
- Customisation Options Including Light & Dark Modes
- Mobile Reponsiveness
All of this has been done using Javascript, Python (Django + SQL), HTML & CSS.

## Distinctiveness and Complexity
Several features make this website more complex than the other projects. 

Asynchronous Javascript has been used in many places without having to reload pages.
- Tasks Applet: Inline Editing, Delete, Undo Complete.
- Time Applet: Countdowns for alarms have been done using APIs and Javascript setInterval() functions.
- Links in Navbar: Javascript & APIs used to create bookmarks that are pinned to the Navbar.
- Popout Windows (To Create new Tasks, Links, Alarms)
- Light Mode & Darkmode using Filters.
- Bootstrap - Dropdowns, Progress Bars.

CSS has been used extensively.
- Accurate Mobile Response
- Bootstrap explored in detail - Navbar Collapse Features.
- Time Applet - Custom datetime picker used.
- Filters for Light/Dark mode.

Improved Security Features.
- Applets cannot be accessed (blocked) until user logged in.
- Users can't access other user data.

Extensive Error Checking.
- Prevents unexpected error messages.

My project is complex as it implements almost all of the various concepts that were taught in the course. This includes Django's ability to render webpages on the backend, SQLite Databases using python models, as well as Javascript (especially asynchronous) on the front-end to allow for a user interface. APIs and fetch routes have been utilised in detail. Mobile Response is thoroughly implemented, and wasn't there in the previous projects. The features found in the project weren't there in other ones, making it unique and different. 

## Files
Below are the files of my projects and a brief description about them. Default django files haven't been included.
### HTML (.html)

- layout.html - Stores the basic layout of all the other pages, including the navbar and the javascript fetch function that renders link bookmarks. Also controls dark/light mode by fetching and applying a filter.

- index.html - Index page that contains an overview of all the applets (simplified features): ToDo Lists, Stopwatch & Alarm.

- no_user.html - Alternative index page that is rendered if the user isn't signed in. Shows features of website and encourages sign in.

- todo.html - Contains todo lists. Allows user to create, edit, delete & complete tasks.

- todo-completed - Contains completed tasks. Allows user to undo-complete (mark as incomplete) & delete tasks.

- time.html - Contains alarms that are sorted by completed and then date. Allows users to create and delete alarms. Completed/Expired alarms are red in colour. Contains a stopwatch also that is added by 'include'.

- alarm.html - Contains alarm form. Javascript is used to make an interactive date-time picker (Imported from [Tempus Dominus](https://getdatepicker.com/5-4/)).

- stopwatch.html - Stopwatch HTML & Javascript code with options to start, stop & reset. Is included in time.html.

- links.html - Allows users to create, view, delete and pin links (upto 5). Pinned links appear in the navbar.

- progress.html - Shows the users progress and actions with this website. Includes % tasks completed, stopwatches used, links and alarms created.

- login.html - Users can log into their accounts.

- register.html - Create user accounts.


### JavaScript (.js)

- links.js - Contains the program to create and delete links using fetch methods.

- time.js - Contains program to create and delete alarms. Also counts down time for alarm using setInterval() function.

- todo.js - Contains program to create, edit, delete and mark tasks as completed. Also allows for tasks to be marked as uncompleted. Accessed by both todo.html & todo-completed.html.


### Python (.py)

- models.py - Contains User, ToDo, Alarm & Link Models to store information in a SQLite Database. The 'User' model has been slightly modified to have darkmode and stopwatch usage as additional properties.

- views.py - Contains all of the views - renders, HttpResponseRedirects, JSONResponses & API Routes. Handles fetch, get, post, delete and put requests.

- urls.py - Contains all the website URLs, including API routes.

- forms.py - Contains Django forms - Tasks, Alarms & Links that are used by the HTML files to input data.

## How to Run my Project
1. Open terminal & navigate to main project folder. 
2. Initialize the database.
```
python manage.py makemigrations dashboard
python manage.py migrate
```
3. Launch the Django Server http://127.0.0.1:8000/
```
python manage.py runserver
```
