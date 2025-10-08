import time
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Outreach:
    def __init__(self, driver):
        self.driver = driver

    def send_connection_requests(self, candidates_file):
        if not os.path.exists(candidates_file):
            print(f"Error: {candidates_file} not found. Please search for candidates first.")
            return

        candidates = pd.read_csv(candidates_file)
        print(f"Starting to send connection requests to {len(candidates)} candidates.")

        for index, row in candidates.iterrows():
            self.driver.get(row['url'])
            time.sleep(4)

            try:
                # Find and click the 'Connect' button
                connect_button = self.driver.find_element(By.XPATH, "//button[span[text()='Connect']]")
                connect_button.click()
                time.sleep(2)

                # Send the request with a generic message
                # Find the "Add a note" button to customize the message
                add_note_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Add a note']")
                add_note_button.click()
                time.sleep(1)

                # Add a generic message
                message_box = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='message']")
                message = f"Hi {row['name'].split()[0]}, I came across your profile and would like to connect."
                message_box.send_keys(message)
                time.sleep(1)

                # Find and click the 'Send' button
                send_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send now']")
                send_button.click()

                print(f"Connection request sent to {row['name']}.")
                time.sleep(2) # Wait a bit before the next one

            except NoSuchElementException:
                print(f"Could not find a 'Connect' button for {row['name']}. They might already be a connection.")
            except Exception as e:
                print(f"An error occurred while connecting with {row['name']}: {e}")

        print("\nFinished sending connection requests.")