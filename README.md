# Project Description:
A project focused on scraping job listings data from various job portals, performing exploratory data analysis (EDA) using Python and Pandas, preforming discriptive analysis and visualizing the results using Tableau. The analysis covers job roles across different career levels (entry, associate, senior, manager), providing insights into the job market trends based on the collected data.

# My Goal:
  1. Insightful statistical analysis of job market trends, offering a comprehensive overview of the current job landscape.
  2. Perform EDA to identify trends and patterns in the job market.
  3. Dashboard creation and storytelling.

# Acquisition:
  1. Transforming unstructured data to structured dataset that can be used for further analysis.
  2. Connecting to ODBC driver and moving data from dataframes to SQL database.
  3. Creating interactive dashboard to visualize and explore job market insights across various dimensions.
 

# Prerequisites:
 
      from selenium import webdriver
      from selenium.webdriver.chrome.service import Service
      from selenium.webdriver.chrome.options import Options

      from selenium import webdriver
      import time
      import pandas as pd
      import os

      from selenium.webdriver.support.select import Select
      from selenium.webdriver.support.ui import WebDriverWait
      from selenium.webdriver.common.by import By
      from selenium.webdriver.support import expected_conditions as EC
      from selenium.webdriver.common.keys import Keys

# Process and Methodology:

# Data Collection:
      Tools: Python, BeautifulSoup, Selenium, Pandas, Requests, JSON, Jupyter Notebook.
      Websites: LinkedIn, Indeed, ZipRecruiter, and other job portals.

 1. Challenges:
    
     •	 Paginated Rendering: Websites that display job listings across multiple pages.
    
     •	 Infinite Scroll: Websites where job listings continuously update as you scroll down.
    
     •	 Load More Button: Websites requiring interaction (e.g., clicking a button) to load more job listings.
     
 3. Approach:
    
     •	 Web Scraping:
    
    Use Selenium for handling dynamic content rendering, such as infinite scrolls and load more buttons.
    
    Use BeautifulSoup and Requests for scraping static content.
    
     •	 Data Extraction: Extract relevant information like job title, company, location, posting date, job level, and job description.

# Exploratory Data Analysis (EDA) using Pandas:
     •	Data Inspection: Review the number of rows and columns.
     •	Data Types: Analyze the types of values (e.g., text, numeric, categorical).
     •	Missing Values: Identify systematic or random missing data and address them appropriately (e.g., imputation, deletion).
     •	Outliers: Detect and handle outliers that could skew the analysis.
   
# Data Cleaning:
     •	Normalization: Standardize job titles, locations, and company names.
     •	Duplicate Removal: Identify and remove duplicate listings.
     •	Data Transformation: Convert job levels into categorical variables, extract relevant features from job descriptions, and clean textual data.

# Data Storage:
  relational database (SQL Server) to store structured data, enabling easy querying and integration with Tableau.
     
      import pyodbc
    myConnection = pyodbc.connect
    (
       server="localhost",
       database="AdventureWorks2019",
       UID="SA",
       PWD="Flopsyishu@2017",
       driver="{ODBC Driver 18 for SQL Server}",
       TrustServerCertificate="yes"
     )

    print(myConnection)

     cursor = myConnection.cursor()
     sql = """ SELECT TOP 5 * FROM [dbo].[ticket_allocation];"""

     cursor.execute(sql)
     rows = cursor.fetchall()
       for row in rows:
           print(row)
    
    myConnection.close()

# Tableau public link:
https://public.tableau.com/app/profile/ishwarya.gopi.kannan8438/viz/DataScienceJobMarketAnalysisforSep2024/Dashboard1?publish=yes

<img width="1277" alt="Screenshot 2024-09-22 at 1 47 52 PM" src="https://github.com/user-attachments/assets/42215011-a707-4c77-a3f3-72fb85c21657">



