import json
import random
import selenium
import pandas as pd

from config import *
from utility import *
from scrapers import *


def newProx_piplscraper(blockstatus):
    global current_proxy, ticker, ticker_number

    proxy, port = get_proxy(current_proxy, blockstatus)

    current_proxy = proxy
    ticker = 0
    ticker_number = random.randint(ticker_min, ticker_max)
    logger.info("========================================")
    logger.info("proxy->%s ticker_number->%d\n" %(current_proxy, ticker_number))
    pipl_scraper = PiplScraper(proxy, port)
    try:
        pipl_scraper.starting()
        return pipl_scraper
    except:
        pipl_scraper.driver.quit()
        return newProx_piplscraper(False)

    # data = pipl_scraper.scrping(email)

def get_Info(df, sheetname, pipl_scraper):


    logger.info("\n\nSHEETNAME -> %s\n\n\n" % sheetname)
    global ticker, starting_index
    df.fillna("", inplace=True)
    emails = df[key_columns[sheetname]]
    sheet_moreInfo = sheetname + "_moreInfo"
    sheet_moreContact = sheetname + "_moreContact"

    columns  = list(df.columns) + output_newColumns
    # sheet_init(sheet_moreInfo, columns)
    # sheet_init(sheet_moreContact, columns)

    # count = unscanned_starting(filename, emails)
    index = starting_index
    while index < len(emails):
        email = emails[index]
        original_series = df.iloc[index]

        logger.info("Index-> %d   Ticker->%d    Email->%s" %(index, ticker, email))

        try:
            data_moreInfo, data_moreContact = pipl_scraper.scrping(email)
        except:
            pipl_scraper.driver.quit()
            pipl_scraper = newProx_piplscraper(False)
            continue

        if pipl_scraper.check_accessDenied():
            pipl_scraper.driver.quit()
            pipl_scraper = newProx_piplscraper(True)

        elif ticker > ticker_number:
            pipl_scraper.driver.quit()
            pipl_scraper = newProx_piplscraper(False)

        else:
            # logger.info(data_moreInfo)
            # logger.info(data_moreContact)

            series_moreInfo = pd.concat([original_series, pd.Series(data_moreInfo)])
            df_moreInfo = pd.DataFrame([series_moreInfo], columns=list(series_moreInfo.keys()))[columns]
            # del series_moreInfo['email']
            series_moreContact = pd.concat([original_series, pd.Series(data_moreContact)])
            df_moreContact = pd.DataFrame([series_moreContact], columns=list(series_moreContact.keys()))[columns]
            # del series_morecontact['email']

            # logger.info(df_moreInfo)
            # logger.info(df_moreContact)

            add_dfToexcel(df_moreInfo, sheet_moreInfo, columns)
            add_dfToexcel(df_moreContact, sheet_moreContact, columns)

            index += 1
            write_status(sheetname, index)

            ticker += 1

    starting_index = 0
    pipl_scraper.driver.quit()


def main():
    xl = pd.ExcelFile(source_file)
    sheetnames = xl.sheet_names

    if not starting_sheet:
        start_sheetIndex = 0
    else:
        start_sheetIndex = sheetnames.index(starting_sheet)

    pipl_scraper = newProx_piplscraper(False)
    for i in range(start_sheetIndex, len(sheetnames)):
        df = pd.read_excel(io=source_file, sheetname=i)
        get_Info(df, sheetnames[i], pipl_scraper)


if __name__ == "__main__":

    current_proxy = ''
    ticker = 0
    ticker_number = 0
    starting_sheet, starting_index = get_status()


    if not os.path.exists(output):
        writer = pd.ExcelWriter(output)
        df = pd.DataFrame()
        df.to_excel(writer)
        writer.save()

    main()