import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

class LinkedInScraper:
    def __init__(self, email, password):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.email = email
        self.password = password

    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)

    def scrape_jobs(self, keywords, location):
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
        self.driver.get(search_url)
        time.sleep(4)

        jobs = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            job_listings = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list li")
            for job in job_listings:
                try:
                    title = job.find_element(By.CSS_SELECTOR, ".base-search-card__title").text
                    company = job.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle").text
                    location = job.find_element(By.CSS_SELECTOR, ".job-search-card__location").text
                    job_url = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "url": job_url
                    })
                except Exception as e:
                    print(f"Error extracting job details: {e}")

            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        df = pd.DataFrame(jobs)
        df.to_csv("linkedin_jobs.csv", index=False)
        print(f"Scraped {len(jobs)} jobs and saved to linkedin_jobs.csv")

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    scraper = LinkedInScraper(email, password)
    scraper.login()
    # scraper.scrape_jobs("Software Engineer", "United States")
    scraper.close()
    print("Scraping complete.")