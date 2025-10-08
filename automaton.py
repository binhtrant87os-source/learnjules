import os
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

try:
    import config
except ImportError:
    config = None

class LinkedInAutomaton:
    def __init__(self, driver):
        self.driver = driver

    def apply_to_jobs(self, jobs_file):
        if not config:
            print("Error: config.py not found. Please copy config.py.example to config.py and fill it out.")
            return

        if not os.path.exists(jobs_file):
            print(f"Error: {jobs_file} not found.")
            return

        jobs = pd.read_csv(jobs_file)
        applied_jobs = []

        for index, row in jobs.iterrows():
            self.driver.get(row['url'])
            time.sleep(3)
            try:
                easy_apply_button = self.driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button")
                easy_apply_button.click()
                time.sleep(2)

                # Loop through application pages
                while True:
                    try:
                        # Upload resume if requested
                        resume_upload = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                        resume_upload.send_keys(config.USER_PROFILE["resume_path"])
                        time.sleep(1)
                    except NoSuchElementException:
                        pass # No resume upload on this page

                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Continue'], button[aria-label*='Next']")
                        next_button.click()
                        time.sleep(2)
                    except NoSuchElementException:
                        break # No more "Next" buttons

                # Final submission
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Submit application']")
                    submit_button.click()
                    print(f"Successfully applied to: {row['title']} at {row['company']}")
                    applied_jobs.append(row.to_dict())
                except NoSuchElementException:
                    print(f"Could not find submit button for {row['title']}. Closing application.")
                    # Close the dialog
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss']").click()
                    except:
                        pass

            except NoSuchElementException:
                print(f"No 'Easy Apply' button for {row['title']}. Skipping.")
            except Exception as e:
                print(f"An error occurred while applying to {row['title']}: {e}")

        # Save applied jobs for tracking
        if applied_jobs:
            df = pd.DataFrame(applied_jobs)
            df['applied_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
            df['status'] = 'Applied'
            df.to_csv("applied_jobs.csv", index=False)
            print(f"\nSaved {len(applied_jobs)} applied jobs to applied_jobs.csv")