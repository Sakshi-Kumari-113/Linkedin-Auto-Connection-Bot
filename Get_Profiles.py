import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from configparser import ConfigParser

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

#Setting up Config file
file = 'config.ini'
config = ConfigParser()
config.read(file)

# Navigate to the URL
SECTOR = config['SECTOR']['SECTOR'] # Enter the domain for profiles.
url = f"https://www.google.com/search?q=+%22marketing%22%20AND%20%22sales%22%20AND%20%22{SECTOR}%22%20-intitle:%22profiles%22%20-inurl:%22dir/+%22+site:in.linkedin.com/in/+OR+site:in.linkedin.com/pub/"
driver.get(url)
driver.maximize_window()
time.sleep(2)

# Initiate empty list to capture final results
links = []

# Scroll and capture links
SCROLL_PAUSE_TIME = 4  # Adjust the time to wait for more results to load
MAX_SCROLLS = 10  # Adjust the number of scrolls to perform

for _ in range(MAX_SCROLLS):
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search = soup.find_all('div', class_="yuRUbf")

    for h in search:
        link = h.a.get('href')
        if link not in links:  # Avoid duplicates
            links.append(link)

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

# Save the links to a CSV file
df = pd.DataFrame(links, columns=['Link'])
df.to_csv(f"{config['CSV Handling']['NAME_CSV_to_store']}", index=False)

print(f"{len(links)} links saved to {config['CSV Handling']['NAME_CSV_to_store']}")

# Close the WebDriver
driver.quit()