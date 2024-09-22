#step 1 : Import Packages

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

# step 2: Set up the driver
driver = webdriver.Safari()

# Use implicit wait for elements to load
driver.implicitly_wait(10)

# Step 3: Create the URL customize it by add filters and specific locations
location = "United States"
jobs = [
    '"data analyst"',
    '"data scientist"',
    '"data engineer"'
]

job_search = "+OR+".join(jobs)

url = (
    f'https://www.indeed.com/jobs?q={job_search}&'
    f'l={location}&'
    f'fromage=1'
)


# Step 4: Navigate to Indeed
driver.get(url)


# step 5: Initialize variables
job_titles = []
company_names = []
locations = []
salary_names = []
current_page = 1

# Scroll to the bottom of the page
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

while True:
    print(f"Processing page {current_page}...")

    # Find the <ul> element that contains the job listings
    ul_element = driver.find_element(By.CSS_SELECTOR, 'ul.css-zu9cdh')

    # Find all <li> job elements within the <ul>
    job_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    for index, job_element in enumerate(job_elements):
        try:
            # Click on the job element
            job_element.click()

            # Wait for the job details to load
            time.sleep(5)  # Adjust the wait time as needed

            # step 6 : Find the element and scrap the data 
            try:
                title_element = driver.find_element(By.CSS_SELECTOR, 'h2.jobsearch-JobInfoHeader-title.css-1t78hkx e1tiznh50 span')
                job_title = title_element.text.strip()
            except:
                job_title = 'No title found'

            
            try:
                company_element = driver.find_element(By.CSS_SELECTOR, 'a.css-1ioi40n.e19afand0')
                company_name = company_element.text.strip()
            except:
                company_name = 'No company found'

            
            try:
                location_element = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="inlineHeader-companyLocation"] div')
                location = location_element.text.strip()
            except:
                location = 'No location found'
                
            try:
                salary_element = driver.find_element(By.CSS_SELECTOR, 'span.css-19j1a75.eu4oa1w0')
                salary_name = salary_element.text.strip()
            except:
                salary_name = 'No salary found'



            # Append job title to the list
            job_titles.append(job_title)
            locations.append(location)
            company_names.append(company_name)
            salary_names.append(salary_name)

            print(f"Job {index + 1} title processed: {job_title}")

            # Optional: Add a small delay before clicking the next job
            time.sleep(2)

        except Exception as e:
            print(f"Error processing job {index + 1}: {e}")

    # Check for the next page button
    try:
        next_page_element = driver.find_element(By.CSS_SELECTOR, 'ul.css-1g90gv6 a[data-testid^="pagination-page-"]')
        next_page_element.click()

        # Wait for the new page to load
        time.sleep(5)  # Adjust the wait time as needed

        current_page += 1

    except:
        print("No more pages to process.")
        break


# step 7 : Create a DataFrame with more descriptive column headings from the individual Lists

df_company    = pd.DataFrame(company_names, columns=['Company Name'])
df_jobtitle   = pd.DataFrame(job_titles, columns = ['Job Title']) 
df_location   = pd.DataFrame(locations, columns = ['Location'])
df_level      = pd.DataFrame({'Seniority Level': ['Entry Level'] * len(df_company)})
df_emptype    = pd.DataFrame({'Employment Type': ['Full Time'] * len(df_company)})
df_func       = pd.DataFrame({'Job Function': ['Computer science'] * len(df_company)})
df_industries = pd.DataFrame({'Industry': [''] * len(df_company)})
df_salaries = pd.DataFrame(salary_names, columns = ['Salary'])
df_website_name = pd.DataFrame({'website_name': ['Indeed'] * len(df_company)})
 
# step 8 : join everything to 1 single dataframe

df_combined = pd.concat([df_company, df_jobtitle, df_location, df_level, df_salaries, df_emptype, df_func, df_industries,df_website_name], axis=1)
df_combined.to_csv('/Users/magesh/Desktop/L1.csv', index=False)


# step 9: Establish connection to SQL Server

import pyodbc
import pandas as pd

myConnection = pyodbc.connect(
    server="localhost",
    database="AdventureWorks2019",
    UID="SA",
    PWD="Flopsyishu@2017",
    driver="{ODBC Driver 18 for SQL Server}",
    TrustServerCertificate="yes"
)

print("Connection successful:", myConnection)

cursor = myConnection.cursor()

# Define the existing SQL table name (adjust this as needed)
table_name = "job_details"  # Replace with the name of your existing table

# Insert DataFrame data into the existing SQL Server table
# Generating the insert SQL statement
for index, row in df_combined.iterrows():
    insert_sql = f"""
    INSERT INTO {table_name} (Company_Name, Job_Title, Location, Seniority_Level, Salary, Employment_Type, Job_Function, Industry, website_name) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); 
    """
    try:
        # Execute the insert with the row data
        cursor.execute(insert_sql, tuple(row))
        myConnection.commit()
    except Exception as e:
        print(f"Error inserting row {index}: {e}")

# Optionally, fetch data to verify the insertion
sql = f"SELECT TOP 5 * FROM {table_name};"
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print(row)

# step 10 : Close the connection
myConnection.close()
print("Connection closed.")

#Data-science-job-scrapping
