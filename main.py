import sys, os, glob
from config import *
from optparse import OptionParser
from PageScraper import pageScraper
from CompanyScraper import companyScraper


def main():

    if parameters.mode.split("_")[0] == "scrape":

        # Check if given path is 'Data' folder
        if "Data" != os.path.basename(parameters.path):
            
            # Create 'Data' folder if it is not in working directory
            subfolders = [d for d in os.listdir(parameters.path) if os.path.isdir(os.path.join(parameters.path, d))]
            os.mkdir("Data") if "Data" not in subfolders else None
            dataPath = parameters.path+"/Data"
        else:
            dataPath = parameters.path

        if parameters.mode.split("_")[1] == "pages":
            print("Starting Page Scrape operation")
            pageScraper(dataPath)
            print("Finished Page Scraping Succesfully!")

        elif parameters.mode.split("_")[1] == "companies":
            print("Starting Company Scrape operation")
            companyScraper(dataPath)
            print("Finished Company Scraping Succesfully!")




if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-m", "--mode", help='''* The operation that you want to execute: 
                                                --- 'scrape_pages' => Iterates over pages in 'irantalent' website as Selenium saves visited pages.
                                                --- 'scrape_companies => Iterates over companies in 'irantalent' website as Requests sent queries by using saved pages from 'scrape_pages'
                                            ''',
                      type="str", dest="mode", default="")
    parser.add_option("-p", "--path", help='''* Folder path of the Data. (OPTIONAL)''',
                      type = "str", dest="path", default=os.getcwd())
    
    parameters, args = parser.parse_args(sys.argv[1:])

    main()