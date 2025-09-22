from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import mysql.connector
from prettytable import PrettyTable
from Database_Handling import DataBase
from configparser import ConfigParser




#Setting up Config file
file = 'config.ini'
config = ConfigParser()
config.read(file)
LINKEDIN_USERNAME = config['LinkedIn Credentials']['LINKEDIN_USERNAME']
LINKEDIN_PASSWORD = config['LinkedIn Credentials']['LINKEDIN_PASSWORD']


def login_to_linkedin(driver, username, password):
    """Logs into LinkedIn with the provided credentials."""
    driver.get('https://www.linkedin.com/login')

    # Wait for the username field to be present
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys(username)

    # Enter the password
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for the homepage to load
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'global-nav-search'))
    )
    print("Logged in successfully")


def Send_Request(driver, link):
    """Clicking on connect button and then send request without note button,
    If connect button not available then clicking more button, then connect and then send request without note button for each link."""


    driver.get(link)
    driver.maximize_window()
    time.sleep(2)
    name=""
    try:
        name_element = driver.find_element(By.XPATH, '//h1[contains(@class, "text-heading-xlarge")]')
        name = name_element.text

    except:
        pass

    try:
        more_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'More actions')]")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(more_button)).click()
        print("Clicked the More button")

        connect_now_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'to connect')]")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(connect_now_button)).click()
        print("Clicked the Connect now button")

        time.sleep(2)
        # waiting 2 seconds and then clicking send with a note button
        send_without_note_button = driver.find_element(By.XPATH,
                                                       "//button[contains(@aria-label, 'Send without a note')]")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(send_without_note_button)).click()
        print("Clicked Send without note button")
        connection_request="Sent"
        return connection_request,name

    except:
        # When More button is not present
        try:

            # Wait for the Connect button to be present
            connect_now_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'to connect')]")

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(connect_now_button)).click()
            print("Clicked the Connect now button")

            time.sleep(2)
            # waiting 2 seconds and then clicking send with a note button
            send_without_note_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send without a note')]")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(send_without_note_button)).click()
            print("Clicked Send without note button")
            connection_request = "Sent"
            return connection_request,name


        except :
            print(f"Failed to connect")
            connection_request="Not Sent"
            return connection_request,name




def wait_for_browser_close(driver):
    """Keeps the script running until the browser window is closed."""
    while True:
        try:
            # Check if the driver is still active
            driver.current_url
            time.sleep(1)
        except:
            print("Browser closed, ending program.")
            break

def Iterate_CSV(driver,db_obj):
    try:

        with open(f"{config['CSV Handling']['NAME_CSV_to_use']}", mode='r', newline='') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)

            # Skip the header row
            next(csv_reader)

            # Iterate over the rows in the CSV
            for row in csv_reader:
                # Using the links  in the first column
                connection_request,name= Send_Request(driver, row[0])
                link = str(row[0])

                # Define the insert query
                insert_query = "INSERT INTO profile (Name,LinkedIN_ID,Connection_Request) VALUES (%s,%s,%s)"

                # Execute the insert query with the link as a parameter
                db_obj.mycursor.execute(insert_query, (name,link,connection_request))
                db_obj.Show_Content()
                db_obj.db.commit()
    except:
        pass




    finally:
        # Ensure the driver is quit if it's still running
        try:
            driver.quit()
        except:
            pass


def main():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    db_obj = DataBase()
    db_obj.Describe(describe=True)
    login_to_linkedin(driver, LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    Iterate_CSV(driver,db_obj)
    db_obj.Show_Content()
    wait_for_browser_close(driver)



if __name__ == "__main__":
    main()


