import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from setup import EMAIL, PASSWORD, CLASS_SCHEDULES, POLL_RATE, WAIT_JOIN

# Function to get the current class based on the schedule
def get_current_class():
    current_day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')

    for class_name, (class_url, days_of_week, time_range) in CLASS_SCHEDULES.items():
        start_time, end_time = time_range
        if current_day in days_of_week and start_time <= current_time <= end_time:
            return class_name, class_url, end_time  # Return end time as well

    return None, None, None  # If no class is found

# Function to run the iClicker automation
def run_iclicker(class_name, class_url, end_time):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, 'chromedriver.exe')
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    # Log in to iClicker
    driver.get('https://student.iclicker.com/#/login')

    # Enter email
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "input-email"))).send_keys(EMAIL)
    driver.find_element(By.ID, "input-email").submit()

    # Enter password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-password"))).send_keys(PASSWORD)
    driver.find_element(By.ID, "input-password").submit()

    # Click sign-in button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-in-button"))).click()

    # Click on the class name
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[text()="{class_name}"]'))).click()

    # Attempt to find and click the Join button
    button_found = False
    while not button_found:
        
        current_time = datetime.now().strftime('%H:%M')  # Get current time here
        if current_time > end_time:  # Check if the current time exceeds the class's end time
            print("Class time is over, exiting polling loop...")
            break

        try:
            WebDriverWait(driver, WAIT_JOIN).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnJoin"]'))).click()
            button_found = True
            print("Clicked Join button.")
        except Exception as e:
            print("Join button not found, retrying...")
            time.sleep(5)

    # Polling loop
    previous_poll_detected = False  # Initialize this variable to track poll state

    while True:
        print("While loop working")
        print(f"Current URL: {driver.current_url}")
        
        current_time = datetime.now().strftime('%H:%M')
        if current_time > end_time:  # Check if the current time exceeds the class's end time
            print("Class time is over, exiting polling loop...")
            break

        # Check if the current URL is for a poll
        if '/poll' in driver.current_url:
            if not previous_poll_detected:  # If we haven't handled a poll yet
                clicked = False
                print("Poll URL detected, entering retry loop for Multiple Choice A")

                # Indefinite retry loop until clicked
                while not clicked:
                    try:
                        # Wait for the option to be clickable
                        multiple_choice_a = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, 'multiple-choice-a'))
                        )
                        multiple_choice_a.click()  # Attempt to click using Selenium
                        clicked = True  # Mark as clicked if successful
                        print("Clicked on Multiple Choice A.")
                    except Exception as e:
                        print(f"Click failed: {e}, retrying...")
                        time.sleep(1)  # Wait before retrying

                previous_poll_detected = True  # Mark that we've handled this poll
            else:
                print("Already handled the current poll, waiting for a new one...")
        else:
            previous_poll_detected = False  # Reset if not on a poll page

        time.sleep(POLL_RATE)  # Wait before the next check

    try:
        driver.quit()  # Close the browser after finishing
    except Exception as e:
        print(f"Error closing the driver: {e}")

# Main loop to check for classes and run iClicker
while True:
    try:
        class_name, class_url, end_time = get_current_class()  # Get end time too
        
        if class_name:
            print(f"Class '{class_name}' is scheduled. Starting iClicker...")
            run_iclicker(class_name, class_url, end_time)  # Pass end time to the function
        else:
            print("No class scheduled at this time. Checking again in 10 minutes...")
            time.sleep(600)  # Check every 10 minutes
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(600)  # Wait before retrying

