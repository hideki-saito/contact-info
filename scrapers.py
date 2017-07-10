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
                                        executable_path=r'/home/hideki/My_work/data_mining/contact_info/lib/geckodriver')

        self.driver.maximize_window()


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
            data['name'] =  self.driver.find_element_by_class_name("header").text
            properties = self.driver.find_elements_by_class_name("row-line")
            for i in properties:
                title = i.find_element_by_class_name("field_label").text
                value = i.find_element_by_class_name('values').text
                data[title] = value
        except:
            pass

        return data


    def scrping(self, email):
        self.search(email)
        data = self.get_data()
        data['email'] = email
        print (json.dumps(data, indent=2))

        return data


def get_proxy():
    try:
        with open("blocked_proxies.txt") as f:
            blocked_proxies = [item.strip("\n") for item in f.readlines()]
            current_proxy = blocked_proxies[-1]
    except:
        with open("blocked_proxies.txt", 'w') as f:
            f.write("")
            blocked_proxies = []
            current_proxy = ''

    print(current_proxy)
    print (blocked_proxies)
    url = "https://free-proxy-list.net/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content)
    proxie_tags = soup.find('table', attrs={'id':'proxylisttable'}).find_all('tr')[1:-1]

    for tag in proxie_tags:
        proxy = tag.find_all("td")[0].text.strip()
        port = tag.find_all("td")[1].text.strip()
        if proxy!=current_proxy and not proxy in blocked_proxies:
            with open("blocked_proxies.txt", 'a') as f:
                f.write(proxy)
                f.write("\n")
            return proxy, port

    print("No Proxy")
    sys.exit()


def getProx_test():
    get_proxy()
    get_proxy()
    get_proxy()
    get_proxy()
    get_proxy()

getProx_test()


def piplScraper_tester():
    proxy = "204.13.204.110"
    port = "8080"
    emailList = ['leeann.pozos@amd.com', 'ewmeyer@marathonoil.com', 'rodney.miller@gsa.gov', 'aimee.cooper@gsa.gov']
    pipl_scraper = PiplScraper('','1')
    pipl_scraper.starting()

    for email in emailList:
        pipl_scraper.scrping(email)
        if not pipl_scraper.check_accessDenied():
            pipl_scraper.driver.quit()
            pipl_scraper = PiplScraper(proxy, port)
            pipl_scraper.starting()
            pipl_scraper.scrping(email)

# pipl_scraper.driver.get("http://whatismyipaddress.com")

