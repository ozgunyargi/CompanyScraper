import os, glob, codecs, time
from config import *
from bs4 import BeautifulSoup
import numpy as np
import requests

def companyScraper(path: str = '') -> None:

    # Create 'Companies' folder inside of 'Data' folder if it does not exist. 
    subfolders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    os.mkdir(path+"/Companies") if "Companies" not in subfolders else None
    dataPath = path + "/Companies"

    # Find in which page you left
    with open(f"{dataPath}/scrapedPages.txt", "a+") as myfile:
        myfile.seek(0)
        lines = myfile.readlines()
        LastPage = 0 if len(lines) == 0 else int(lines[-1].strip()) # Find the last unfinished Page folder

    pages = glob.glob(f"{path}/Pages/*.html") # Get a list of page htmls.
    def byNum(x):
        return int(x.split("_")[-1][:-5])
    pages = sorted(pages, key=byNum)

    pageFolders = [d for d in os.listdir(dataPath) if os.path.isdir(os.path.join(dataPath, d))] # Retrieve the sub-folder names inside of 'Companies' folder
    for indx in range(LastPage, len(pages)):
        page = pages[indx]
        pageName = os.path.basename(page)[:-5].replace("_", ": ")
        folderName = os.path.basename(page)[:-5]
        print(f"* Start Scraping {pageName}")

        # Create a 'Page' folder inside of 'Companies' folder if it does not exist
        if  folderName not in pageFolders:
            os.mkdir(dataPath+f"/{folderName}")

        scrapedCompanies = [os.path.basename(companyHtml) for companyHtml in glob.glob(f"{dataPath}/{folderName}/*.html")]

        # Open Page html to recieve company html(s).
        with codecs.open(page, 'r', 'utf-8') as myfile:
            soup = BeautifulSoup(myfile.read(), "html.parser")
        htmlDict = parseHTMLwName(soup)

        # Save company html(s) for the ones have not been scraped until now.
        for company in htmlDict:
            if company+".html" not in scrapedCompanies:
                print(f"     -- Start scraping company {company.replace('_', ' ') } ", end="")
                try:
                    r = requests.get(htmlDict[company])
                except:
                    print("\n"+"Page could not be loaded succesfully. Terminating...")
                    exit(0)
                if r.status_code == 200: # Check if company page is loaded correctly or not
                    print("=> SUCESS!")
                else:
                    print("\n"+"Page could not be loaded succesfully. Terminating...")
                    exit(0)

                sleepTime = np.abs(np.random.normal(5,1,1)[0]) # Wait for short amount of time
                print("         => Sleeping for %.2f seconds..." % sleepTime)
                time.sleep(sleepTime)

                # Save the company HTML into Page folder
                companyFile = os.path.join(f'{dataPath}/{folderName}', f"{company.replace('/', '').replace(chr(92), '').replace(chr(34), '').replace('.', '')}.html") # Remove '/', '\', '"', '.' characters from file name.
                with codecs.open(companyFile, "w", "utf−8") as myfile:
                    source = r.text
                    myfile.write(source)

        # Check if all Page companies are scraped or not. If it is the case, mark as completed.
        if len(htmlDict) == len([os.path.basename(companyHtml) for companyHtml in glob.glob(f"{dataPath}/{folderName}/*.html")]):
             with open(f"{dataPath}/scrapedPages.txt", "a+") as myfile:
                 myfile.write(f'{indx+1}\n')

# SIDE FUNCTIONS
# -----------------------------------------------------------------------------------------------------

def parseHTMLwName(html: BeautifulSoup) -> dict:
    myDict = {}
    listContainer = html.find('div', class_="row d-flex flex-wrap ng-star-inserted")
    for element in listContainer.findAll('div', class_="col-xs-12 col-sm-6 col-md-4 margin-bottom-16 ng-star-inserted"):
        href = element.div.a["href"]
        site = (webpage[:webpage.index("e", -15)] + href).replace("job-positions", "overview")
        nameContainer = element.div.find('div', class_="card-title border-bottom d-flex")
        name = nameContainer.find('div', class_="min-width-0").find('p', class_="font-20 font-weight-bold margin-bottom-4 text-ellipsis").text.strip()
        myDict[name.replace(" ", "_")] = site
    return myDict