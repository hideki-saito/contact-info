import json
import pandas as pd

from config import *
from utility import *
from scrapers import *


def newProx_piplscraper():
    proxy, port = get_proxy()
    pipl_scraper = PiplScraper(proxy, port)
    pipl_scraper.starting()

    return pipl_scraper
    # data = pipl_scraper.scrping(email)

def get_moreInfo(df, sheetname,pipl_scraper):
    print (sheetname)
    print (list(df.columns))
    df.fillna("", inplace=True)
    emails = df[key_columns[sheetname]]
    filename = sheetname + "_moreInfo.txt"
    # emailList = ['leeann.pozos@amd.com', 'ewmeyer@marathonoil.com', 'rodney.miller@gsa.gov', 'aimee.cooper@gsa.gov']
    # search_keywords = get_keyword1(df)

    print (emails)
    count = 0
    while count < len(emails):
        email = emails[count]
        print (email)
        data = pipl_scraper.scrping(email)
        if pipl_scraper.check_accessDenied():
            pipl_scraper.driver.quit()
            pipl_scraper = newProx_piplscraper()
        else:
            add_dict(data, filename)
            count += 1


def get_likeInfo(df):
    pass


def main():
    xl = pd.ExcelFile(filename)
    sheetnames = xl.sheet_names
    df = pd.read_excel(io=filename, sheetname=target_sheet-1)

    proxy, port = get_proxy()
    pipl_scraper = PiplScraper(proxy, port)
    pipl_scraper.starting()

    if target_sheet in more_info:
        get_moreInfo(df, sheetnames[target_sheet-1], pipl_scraper)

    if target_sheet in like_info:
        get_likeInfo(df)


if __name__ == "__main__":
    target_sheet = 2
    main()