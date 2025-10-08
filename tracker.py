import pandas as pd
import os

APPLIED_JOBS_FILE = "applied_jobs.csv"

def view_applications():
    if not os.path.exists(APPLIED_JOBS_FILE):
        print("No applications tracked yet.")
        return

    df = pd.read_csv(APPLIED_JOBS_FILE)
    print("\n--- Tracked Applications ---")
    print(df.to_string())

def update_application_status():
    if not os.path.exists(APPLIED_JOBS_FILE):
        print("No applications to update.")
        return

    view_applications()
    df = pd.read_csv(APPLIED_JOBS_FILE)

    try:
        job_index = int(input("Enter the index of the job to update: "))
        if job_index not in df.index:
            print("Invalid index.")
            return

        new_status = input("Enter the new status (e.g., Interviewing, Offered, Rejected): ")
        df.loc[job_index, 'status'] = new_status
        df.to_csv(APPLIED_JOBS_FILE, index=False)
        print("Application status updated successfully.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def tracker_menu():
    while True:
        print("\n--- Application Tracker ---")
        print("1. View all applications")
        print("2. Update application status")
        print("3. Back to main menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_applications()
        elif choice == '2':
            update_application_status()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")