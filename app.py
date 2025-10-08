import os
from scraper import LinkedInScraper
from automaton import LinkedInAutomaton
from tracker import tracker_menu
from candidate_finder import CandidateFinder
from outreach import Outreach
from dotenv import load_dotenv

def main():
    load_dotenv()
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    if not email or not password:
        print("Please set your LINKEDIN_EMAIL and LINKEDIN_PASSWORD in a .env file.")
        return

    # It's more efficient to initialize the driver once.
    # Let's use the scraper's driver for all operations.
    scraper = LinkedInScraper(email, password)
    scraper.login()

    driver = scraper.driver # Re-use the authenticated driver
    automaton = LinkedInAutomaton(driver)
    candidate_finder = CandidateFinder(driver)
    outreach = Outreach(driver)

    while True:
        print("\n--- LinkedIn Automation Tool ---")
        print("1. Scrape for jobs")
        print("2. Apply to scraped jobs")
        print("3. Track applications")
        print("4. Search for candidates")
        print("5. Send connection requests to candidates")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            keywords = input("Enter job keywords (e.g., Software Engineer): ")
            location = input("Enter location (e.g., United States): ")
            scraper.scrape_jobs(keywords, location)
            print("\nJob scraping complete.")
        elif choice == '2':
            automaton.apply_to_jobs("linkedin_jobs.csv")
        elif choice == '3':
            tracker_menu()
        elif choice == '4':
            candidate_keywords = ["microcontroller", "MCU", "autosar"]
            candidate_finder.search_candidates(candidate_keywords)
        elif choice == '5':
            outreach.send_connection_requests("candidates.csv")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

    scraper.close()
    print("\nExiting LinkedIn Automation Tool.")

if __name__ == "__main__":
    main()