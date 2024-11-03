import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

class EasyApplyLinkedin:

    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        
        service = Service(data['driver_path'])
        self.driver = webdriver.Chrome(service=service)

    def login_linkedin(self):
        self.driver.get("https://www.linkedin.com/login")
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
        time.sleep(7)

    def job_search(self):
        jobs_link = self.driver.find_element(By.LINK_TEXT, 'Jobs')
        jobs_link.click()
        time.sleep(2)

        search_keywords = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search by title, skill, or company']"))
        )
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)

        search_location = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='City, state, or zip code']"))
        )
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        time.sleep(2)
        
        try:
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Easy Apply filter.']"))
            )
            easy_apply_button.click()
            print("Easy Apply filter applied successfully.")
        except TimeoutException:
            print("Easy Apply button did not load in time.")

    def apply_to_job(self, job_element):
        job_element.click()
        try:
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button--primary')]"))
            )
            easy_apply_button.click()
            print("Clicked Easy Apply for a job.")
            
            # Loop to keep clicking "Next" as long as it appears
            while True:
                try:
                    next_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Continue to next step']"))
                    )
                    next_button.click()
                    print("Clicked Next button on the Easy Apply popup.")
                except TimeoutException:
                    print("No more Next buttons to click.")
                    break

            # After the last "Next" button, click the "Review" button
            try:
                review_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Review your application']"))
                )
                review_button.click()
                print("Clicked Review button.")
                
                # After the "Review" button, click the "Submit application" button
                submit_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit application']"))
                )
                submit_button.click()
                print("Clicked Submit application button.")
                
                # Wait for 10 seconds to allow for visual confirmation
                time.sleep(10)

            except TimeoutException:
                print("Review or Submit button did not appear.")
                
        except TimeoutException:
            print("Easy Apply button or Next button did not load in time.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def find_offers(self):
        job_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'jobs-apply-button--top-card')]")
        
        for job_element in job_elements:
            try:
                easy_apply_button = job_element.find_element(By.XPATH, ".//button[contains(@aria-label, 'Easy Apply')]")
                if easy_apply_button:
                    self.apply_to_job(job_element)
            except NoSuchElementException:
                print("Easy Apply button not found for this job, moving to the next job.")
            except Exception as e:
                print(f"An error occurred while processing job: {e}")

    def close_session(self):
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.find_offers()
        time.sleep(2)
        self.close_session()


if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()
