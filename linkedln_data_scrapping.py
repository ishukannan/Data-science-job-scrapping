
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


# step 2: Create a Safari WebDriver instance
driver = webdriver.Safari()

# Use implicit wait for elements to load
driver.implicitly_wait(10)


# Step 3: Create the URL , Add Filters
location = "united states"
jobs = [
    '"data analyst"',
    '"data scientist"',
    '"data engineer"'
]

job_search = " OR ".join(jobs)

# Create the URL with the job search query and location
url = (
    f'https://www.linkedin.com/jobs/search?keywords={job_search}&'
    f'location={location}&'
    f'geoId=103644278&'
    f'f_JT=F&'  # Job type: Full-time
    f'f_TPR=r86400&'  # Time posted: Last 24 hours
    f'f_E=4&'       #entry level
    f'position=1&'
    f'pageNum=0'
)

# Step 4: Navigate to LinkedIn
driver.get(url)


# step 5: scroll and preload the job opening 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

i = 2
n = 500  # Define the value of n based on your needs
end_notification_xpath = "//p[contains(text(), \"You've viewed all jobs for this search\")]"
see_more_button_xpath = "//button[@aria-label='See more jobs']"

while i <= int((n + 500) / 25) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
    time.sleep(5)  # Allow time for new content to load

    try:
        # Check if the end notification is present
        end_notification = driver.find_element(By.XPATH, end_notification_xpath)
        print("Reached the end of job listings.")
        break  # Exit the loop if end notification is found
    except:
        pass

    try:
        # Try to find and click the "See more jobs" button
        see_more_button = driver.find_element(By.XPATH, see_more_button_xpath)
        driver.execute_script("arguments[0].click();", see_more_button)  # Click the button
        time.sleep(5)  # Allow time for new content to load
    except:
        print("No more 'See more jobs' button found.")
        break

i = 2
while i <= int((n+800)/25)+1: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        send = driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
        driver.execute_script("arguments[0].click();", send)   
        time.sleep(5)
        
        
                                                          
    except:
        pass
        time.sleep(10)
        
    i = i + 1


# step 6: Find Total Number of Job Listings
job_list_items = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")
total_jobs = len(job_list_items)
print(total_jobs)


#alternative scroll and click code:

i = 2
while i <= int((n + 800) / 25) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        # Check if the "You've viewed all jobs" notification is present
        notification = driver.find_element(By.XPATH, "//p[contains(text(), 'You\'ve viewed all jobs for this search')]")
        if notification:
            print("All jobs have been viewed. Stopping execution.")
            break
        
        # Click the "See more jobs" button
        send = driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
        driver.execute_script("arguments[0].click();", send)
        time.sleep(5)
        
    except Exception as e:
        # Optionally print the exception message for debugging
        print(f"Exception occurred: {e}")
        time.sleep(10)
        
    i = i + 1


#step 7: Initialize variables

locations = []
job_title = []
company = []
seniority_levels = []
employment_types = []
job_functions = []
industries = []
salaries = []

for j in range(total_jobs):
    try:
        # Scrape location
        location_elements = driver.find_elements(By.CLASS_NAME, 'job-search-card__location')
        if j < len(location_elements):
            location = location_elements[j].text
            locations.append(location.strip())
        
        # Scrape job title
        title_elements = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')
        if j < len(title_elements):
            title = title_elements[j].text
            job_title.append(title.strip())
        
        # Scrape company name
        companynames = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')
        if j < len(companynames):
            com = companynames[j].text
            company.append(com.strip())

    except IndexError:
        # Only print "no" once if an IndexError is encountered
        print("no")
        break  # Exit the loop if an IndexError is encountered


# Wait for the page to load
time.sleep(5)  # Adjust the wait time as needed

# Find the <ul> element that contains the jobs
ul_element = driver.find_element(By.CSS_SELECTOR, 'ul.jobs-search__results-list')

# Find all <li> job elements within the <ul>
job_elements = ul_element.find_elements(By.TAG_NAME, 'li')

# Lists to store job criteria
seniority_levels = []
employment_types = []
job_functions = []
industries = []
salaries = []  # List to store salary information

for index, job_element in enumerate(job_elements):
    try:
        # Click on the job element
        job_element.click()

        # Wait for the right side to update
        time.sleep(2)  # Adjust the wait time as needed

        # Find the <ul> element that contains the job description details
        ul_description = driver.find_element(By.CSS_SELECTOR, 'ul.description__job-criteria-list')
        
        # Find all <li> elements within the <ul>
        li_elements = ul_description.find_elements(By.TAG_NAME, 'li')
        
        # Create a dictionary to store the job criteria
        job_criteria = {}
        
        for li in li_elements:
            # Extract the header and text
            header_element = li.find_element(By.CSS_SELECTOR, 'h3.description__job-criteria-subheader')
            text_element = li.find_element(By.CSS_SELECTOR, 'span.description__job-criteria-text--criteria')
            
            header_text = header_element.text.strip()
            description_text = text_element.text.strip()
            
            # Store the criteria in the dictionary
            job_criteria[header_text] = description_text
        
        # Extract salary information
        try:
            salary_element = driver.find_element(By.CSS_SELECTOR, 'div.salary.compensation__salary')
            salary_text = salary_element.text.strip()
        except:
            salary_text = '0'  # Set to '0' if salary information is not available
        
        # Append criteria to the respective lists
        seniority_levels.append(job_criteria.get('Seniority level', 'Not specified'))
        employment_types.append(job_criteria.get('Employment type', 'Not specified'))
        job_functions.append(job_criteria.get('Job function', 'Not specified'))
        industries.append(job_criteria.get('Industries', 'Not specified'))
        salaries.append(salary_text)

        print(f"Job {index + 1} processed.")

        # Optional: Add a small delay before clicking the next job
        time.sleep(2)

    except Exception as e:
        print(f"Error processing job {index + 1}: {e}")


# step 8 : Create a DataFrame with more descriptive column headings from the individual Lists
        
df_company    = pd.DataFrame(company, columns=['Company Name'])
df_jobtitle   = pd.DataFrame(job_title, columns = ['Job Title']) 
df_location   = pd.DataFrame(locations, columns = ['Location'])
df_level      = pd.DataFrame(seniority_levels, columns = ['Seniority Level'])
df_emptype    = pd.DataFrame(employment_types, columns = ['Employment Type'])
df_func       = pd.DataFrame(job_functions, columns = ['Job Function'])
df_industries = pd.DataFrame(industries, columns = ['Industry'])
df_salaries = pd.DataFrame(salaries, columns = ['Salary'])
df_website_name = pd.DataFrame({'website_name': ['LinkedIn'] * len(df_company)})


# step 9 : join everything to 1 single dataframe

df_combined = pd.concat([df_company, df_jobtitle, df_location, df_level, df_salaries, df_emptype, df_func, df_industries,df_website_name], axis=1)
df_combined.to_csv('/Users/magesh/Desktop/L1.csv', index=False)


# step 10 : Establish SQL Server connection and move the dataframes to tables 

import pyodbc
import pandas as pd

# Establish connection to SQL Server
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

# Define the SQL table schema based on DataFrame columns (adjust the types accordingly)
table_name = "job_details"  # Replace with your desired table name

# Example SQL command to create a table (adjust column names and types as needed)
create_table_sql = f"""
CREATE TABLE {table_name} (
      Company_Name varchar(500),
      Job_Title varchar(500),
      Location varchar(500),
      Seniority_Level varchar(500),
      Salary varchar(500),
      Employment_Type varchar(500),
      Job_Function varchar(500),
      Industry varchar(500),
      website_name varchar(500)
);
"""

# Execute the table creation SQL command
try:
    cursor.execute(create_table_sql)
    myConnection.commit()
    print(f"Table {table_name} created successfully.")
except Exception as e:
    print(f"Error creating table: {e}")

# Insert DataFrame data into the SQL Server table
# Generating the insert SQL statement
for index, row in df_combined.iterrows():
    insert_sql = f"""
    INSERT INTO {table_name} (Company_Name, Job_Title, Location, Seniority_Level, Salary, Employment_Type, Job_Function, Industry, website_name) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); 
    """
    try:
        cursor.execute(insert_sql, tuple(row))  # Execute the insert with the row data
        myConnection.commit()
    except Exception as e:
        print(f"Error inserting row {index}: {e}")

# Optionally, fetch data to verify the insertion
sql = f"SELECT TOP 5 * FROM {table_name};"
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print(row)

# step 11: Close the connection
myConnection.close()
print("Connection closed.")

############# Alternative connection code #######################

import pyodbc
myConnection = pyodbc.connect(
    server="localhost",
    database="AdventureWorks2019",
    UID="SA",
    PWD="Flopsyishu@2017",
    driver="{ODBC Driver 18 for SQL Server}",
    TrustServerCertificate="yes"
)

print(myConnection)

cursor = myConnection.cursor()
sql = """
SELECT TOP 5 * FROM [dbo].[ticket_allocation];
"""

cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print(row)
    
myConnection.close()







