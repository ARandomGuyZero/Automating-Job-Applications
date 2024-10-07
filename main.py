"""
LinkedIn Job Application Automation

Author: Alan
Date: October 6th, 2024

This script automates applying for job listings on LinkedIn, using Selenium for web scraping and interaction.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Define your LinkedIn login credentials and phone number
ACCOUNT_EMAIL = "YOUR_LOGIN_EMAIL"
ACCOUNT_PASSWORD = "YOUR_LOGIN_PASSWORD"
PHONE = "YOUR_PHONE_NUMBER"

# Initialize the Chrome driver
# This opens the Chrome browser using Selenium
driver = webdriver.Chrome()

# Open the LinkedIn Jobs page to search for jobs with a specified location and keyword
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3586148395&f_LF=f_AL&geoId=101356765&"
           "keywords=python&location=London%2C%20England%2C%20United%20Kingdom&refresh=true")

# Wait for the page to load and reject cookies
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, 'button[action-type="DENY"]').click()

# Click the "Sign in" button to go to the login page
time.sleep(2)
driver.find_element(By.LINK_TEXT, "Sign in").click()

# Enter the login credentials (email and password)
time.sleep(2)
driver.find_element(By.ID, "username").send_keys(ACCOUNT_EMAIL)
driver.find_element(By.ID, "password").send_keys(ACCOUNT_PASSWORD)
driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

# Solve CAPTCHA manually, then press Enter to continue
input("Solve CAPTCHA and press Enter to continue...")

# Wait for the job listings page to load and get all job listings
time.sleep(5)
job_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

def apply_for_job():
    """
    Attempts to apply for a job by clicking the 'Apply' button and filling in required details such as phone number.
    If the application requires extra steps, it skips the job listing.
    """
    try:
        # Click the 'Apply' button on the job listing
        driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button").click()
        time.sleep(2)

        # Enter phone number if the field is empty
        phone_input = driver.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
        if phone_input.get_attribute("value") == "":
            phone_input.send_keys(PHONE)

        # Check if the application is simple or complex
        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            # Close the application modal if it's complex
            driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss").click()
            print("Skipped complex application.")
        else:
            # Submit the application for simple jobs
            submit_button.click()
            print("Application submitted.")

        # Close the success modal after applying
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss").click()
    except NoSuchElementException:
        # If there's no 'Apply' button, skip the listing
        print("No apply button, skipping...")

# Iterate through each job listing and attempt to apply
for listing in job_listings:
    listing.click()
    time.sleep(2)
    apply_for_job()

# Close the browser after completing the applications
driver.quit()
