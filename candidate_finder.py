import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class CandidateFinder:
    def __init__(self, driver):
        self.driver = driver

    def search_candidates(self, keywords):
        print(f"Searching for candidates with keywords: {keywords}")
        search_query = " ".join(keywords)

        self.driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)

        try:
            search_box = self.driver.find_element(By.CSS_SELECTOR, ".search-global-typeahead__input")
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)

            # Click on "People" filter
            people_button = self.driver.find_element(By.XPATH, "//button[text()='People']")
            people_button.click()
            time.sleep(3)

            candidates = []
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            # Scroll and scrape logic
            while len(candidates) < 50: # Limit to 50 candidates for now
                search_results = self.driver.find_elements(By.CSS_SELECTOR, ".reusable-search__result-container")

                for result in search_results:
                    try:
                        name = result.find_element(By.CSS_SELECTOR, ".entity-result__title-text a").text.strip()
                        headline = result.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle").text.strip()
                        url = result.find_element(By.CSS_SELECTOR, ".entity-result__title-text a").get_attribute("href")

                        if name and url:
                            candidates.append({
                                "name": name,
                                "headline": headline,
                                "url": url
                            })
                    except Exception:
                        continue # Skip if element is not found

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            df = pd.DataFrame(candidates)
            df.to_csv("candidates.csv", index=False)
            print(f"Found and saved {len(candidates)} candidates to candidates.csv")

        except Exception as e:
            print(f"An error occurred during candidate search: {e}")