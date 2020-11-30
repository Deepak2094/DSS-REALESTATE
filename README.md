# DSS-REALESTATE
This repository contains codes for building the Decision support System for Real Estate 

# Languages Used - Python 3.x and HTML

# The Folder contains the following Folders
  1) API Calls - This folder contains the python code to extract House Listing, Restuarant and Bars data in Arlington, VA
  2) Inputs - Consists of 4 Input data files filtered based on the distance 
  3) Modules - The folder consists of 4 python files to get the DSS Application up and running
    a)Filter_Listings.py - Filters the Input dataset based on the filters assigned by the user
    b)Model.py - Creates a ranked set of Listings based on the users preference
    c)format_Listings.py - formats the Listings data to make it presentable in the Front end (HTML Webpage)
    d)Flaskapp.py  - Flask Framework which connects all the HTML webpage
    d)static - Contains a static image to be displayed in the UI
    e) Templates - consists of 3 HTML Webapges 
    
# How to Run the DSS Application ?
  Step 1 : Import all the Folders into any IDE - Spyder,Pycharm etc., (please maintain same folder structure and install any dependent packages as needed)
  Step 2 : Run the Flaskapp.py script using.
  Step 3 : Go to the Local Sever location displayed in the output by clicking on it
          (OR)
          Or type in the following address on any browser (http://127.0.0.1:5000/)
  Step 4 : Now, you will see the DSS Homepage

# Alternate Option - if there is no IDE

  Step 1 : Import all the Folders into any Location in your computer (please maintain same folder structure)
  Step 2: Open Terminal on Mac (or) Command Prompt on Windows OS
  Step 3: Type the following python3 /Users/deepak/Documents/DAEN/SYST 542/Project/Deliverables/Modules/Flaskapp.py (The location will change based on where its      stored in your computer)
  Step 4 : Go to the Local Sever location displayed in the output by clicking on it
          (OR)
          Or type in the following address on any browser (http://127.0.0.1:5000/)
  Step 5 : Now, you will see the DSS Homepage
