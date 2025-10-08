import os
from scraper import LinkedInScraper
from automaton import LinkedInAutomaton
from tracker import tracker_menu
from dotenv import load_dotenv

def main():
    load_dotenv()
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    if not email or not password:
        print("Please set your LINKEDIN_EMAIL and LINKEDIN_PASSWORD in a .env file.")
        return

    scraper = LinkedInScraper(email, password)
    scraper.login()

    automaton = LinkedInAutomaton(scraper.driver)

    while True:
        print("\n--- LinkedIn Job Application Bot ---")
        print("1. Scrape for jobs")
        print("2. Apply to scraped jobs")
        print("3. Track applications")
        print("4. Exit")
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
            break
        else:
            print("Invalid choice. Please try again.")

    scraper.close()
    print("\nExiting LinkedIn Job Application Bot.")

if __name__ == "__main__":
    main()