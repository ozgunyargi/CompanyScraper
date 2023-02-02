import os, time, codecs
import numpy as np
from config import *

# WEBDRIVER OPERATIONS
from selenium import webdriver

#FIREFOX
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# WAIT OPERATIONS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pageScraper(path: str = '') -> None:

    # Create 'Page' folder inside of 'Data' folder if it does not exist. 
    subfolders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    os.mkdir(path+"/Pages") if "Pages" not in subfolders else None
    dataPath = path + "/Pages"

    # Find in which page you left
    with open(f"{dataPath}/scrapedPages.txt", "a+") as myfile:
        myfile.seek(0)
        lines = myfile.readlines()
        buttonClicked = 0 if len(lines) == 0 else int(lines[-1].strip())

    # Initiate the driver (GeckoDriver)
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
    options.set_preference("general.useragent.override", f"userAgent={user_agent}")
    options.headless = True

    driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=options)

    print("----")
    print(f"    * Opening: {webpage} ", end = "")
    # Open the page
    driver.get(webpage)
    xPath = '/html/body/app-root/div/div/div[2]/div/it-company-list/div/div[2]/div[2]/div'
    waitToLoad(xPath, driver) # Check if company containers are loaded succesfully
    print("=> SUCESS!")

    button_xPath = '//*[@id="companies-brands-list"]/div/div[1]/button[2]'
    for _ in range(buttonClicked): # Ignore the already saved files and directly move to unsaved page.
        print(f"     -- Page {_+1} is already saved. Skipping...")
        clickButton(button_xPath, driver) # Click the button to go next page
        sleepTime = np.abs(np.random.normal(5,1,1)[0])
        print("         => Sleeping for %.2f seconds..." % sleepTime)
        time.sleep(sleepTime)

    try:

        while True: # Iterate over pages and save the html files into 'Pages' folder
            pageNum = buttonClicked + 1
            print(f"     -- Start scraping page {pageNum} ", end="")

            pageFile = os.path.join(dataPath, f"Page_{buttonClicked+1}.html")
            with codecs.open(pageFile, "w", "utf−8") as myfile:
                source = driver.page_source
                myfile.write(source)

            buttonClicked += 1
            with open(f"{dataPath}/scrapedPages.txt", "a+") as myfile:
                myfile.write(f"{buttonClicked}\n")

            print("=> SUCESS!")

            clickButton(button_xPath, driver)
            waitToLoad(xPath, driver)
            sleepTime = np.abs(np.random.normal(5,1,1)[0])
            print("         => Sleeping for %.2f seconds..." % sleepTime)
            time.sleep(sleepTime)
    except:
        #close browser session
        print(f"Page {pageNum} could not be loaded succesfully. Terminating...")
        driver.quit()


# SIDE FUNCTIONS
# -----------------------------------------------------------------------------------------------------

def waitToLoad (xpath: str, driver_: webdriver.firefox.webdriver.WebDriver) -> None:
    try:
        WebDriverWait(driver_, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except:
        print("Page could not be loaded succesfully. Terminating...")
        driver_.quit()

def clickButton(xpath: str, driver_: webdriver.firefox.webdriver.WebDriver) -> None:
    try:
        WebDriverWait(driver_, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except:
        print("Button could not be found. Terminating...")
        driver_.quit()

# -------------------------------------------------------------------------------------------------------

    

    