# http://radaris.com
# https://holaconnect.com/
# https://pipl.com
from time import sleep
import json
import random
import sys

from selenium import webdriver
from selenium.webdriver.common.proxy import *
import requests
from bs4 import BeautifulSoup

from config import *


class PiplScraper():
    def __init__(self, proxy, port):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy)
        profile.set_preference("network.proxy.http_port", int(port))
        profile.set_preference("network.proxy.ssl", proxy)
        profile.set_preference("network.proxy.ssl_port", int(port))
        profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile=profile,
                                        executable_path=os.path.join(rootpath, 'driver', 'geckodriver'))

        self.driver.maximize_window()
        self.driver.set_page_load_timeout(30)


    def starting(self):
        self.driver.get(pipl['init_url'])
        sleep(pipl['delay'])
        self.login()


    def check_accessDenied(self):
        try:
            if "Access Denied" in self.driver.find_element_by_id('content').text:
                return True
            else:
                return False
        except:
            return False


    def login(self):
        self.driver.find_element_by_id("login_button").click()
        sleep(pipl['delay'])

        self.driver.find_element_by_id("id_email").send_keys(pipl['email'])
        self.driver.find_element_by_id("id_password").send_keys(pipl['password'])
        self.driver.find_element_by_id("submit-id-login").click()
        sleep(pipl['delay'])


    def search(self, email):
        self.driver.find_element_by_id("findall").clear()
        self.driver.find_element_by_id("findall").send_keys(email)
        self.driver.find_elements_by_class_name("btn-search")[1].click()
        # sleep(pipl['delay'])
        sleep(random.randint(delay_min, delay_max))


    def get_data(self):
        data = {}
        try:
            data['image'] = self.driver.find_element_by_id('profile_image').find_element_by_tag_name('img').get_attribute("src")
        except:
            pass

        try:
            data['age'] = self.driver.find_element_by_class_name('age').text
        except:
            pass

        try:
            data['fullname'] =  self.driver.find_element_by_class_name("header").text
            properties = self.driver.find_elements_by_class_name("row-line")
            for i in properties:
                title = i.find_element_by_class_name("field_label").text.lower().strip(":").strip("s")
                value = i.find_element_by_class_name('values').text
                data[title] = value
        except:
            pass

        return data

    def get_relativeResult(self):
        try:
            self.driver.find_element_by_xpath("//div[@class='profile_result_content search_link'][1]/div/a").click()
            sleep(random.randint(delay_min, delay_max))
            return self.get_data()
        except:
            return {}

    def formatting_data(self, raw_data):
        data = raw_data
        for new_column in output_newColumns:
            if not new_column in data.keys():
                data[new_column] = ""

        return data

    def scrping(self, email):
        self.search(email)
        data1 = self.get_data()
        # data1['email'] = email
        data1.pop('', None)

        data2 = self.get_relativeResult()

        # data2['email'] = email
        data2.pop('', None)

        return self.formatting_data(data1), self.formatting_data(data2)


def get_proxy(current_proxy, block_status):
    from random import shuffle

    blockedProxies_path = os.path.join(rootpath, 'status', "blocked_proxies.txt")
    try:
        with open(blockedProxies_path) as f:
            blocked_proxies = [item.strip("\n") for item in f.readlines()]

    except:
        with open(blockedProxies_path, 'w') as f:
            f.write("")
            blocked_proxies = []

    print(current_proxy)
    print (blocked_proxies)
    url = "https://free-proxy-list.net/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content)
    proxie_tags = soup.find('table', attrs={'id':'proxylisttable'}).find_all('tr')[1:-1]
    shuffle(proxie_tags)
    for tag in proxie_tags:
        proxy = tag.find_all("td")[0].text.strip()
        port = tag.find_all("td")[1].text.strip()
        https = tag.find_all("td")[6].text.strip()
        # country = tag.find_all("td")[3].text.strip()
        # and country == "United States"
        if proxy != current_proxy and not proxy in blocked_proxies and https=="yes":
            if block_status:
                with open(blockedProxies_path, 'a') as f:
                    f.write(current_proxy)
                    f.write("\n")
            return proxy, port

    print("No Proxy")
    sys.exit()


def piplScraper_tester():
    proxy = "144.217.33.52"
    port = "3128"
    emailList = ['leeann.pozos@amd.com', 'ewmeyer@marathonoil.com', 'rodney.miller@gsa.gov', 'aimee.cooper@gsa.gov']
    # pipl_scraper = PiplScraper('','1')
    pipl_scraper = PiplScraper(proxy, port)
    pipl_scraper.starting()

    for email in emailList:
        data1, data2 = pipl_scraper.scrping(email)
        if pipl_scraper.check_accessDenied():
            pipl_scraper.driver.quit()
            pipl_scraper = PiplScraper(proxy, port)
            pipl_scraper.starting()
            data1, data2 = pipl_scraper.scrping(email)

        print(json.dumps(data1, indent=2))
        print(json.dumps(data2, indent=2))


# piplScraper_tester()

