import os

rootpath = os.path.dirname(os.path.realpath(__file__))


source_file = os.path.join(rootpath, 'input', "Contactable Database - consolidated contacts_6.27.17.xlsx")
output = os.path.join(rootpath, 'output', "output.xlsx")
image_path = os.path.join(rootpath, 'check_images')


# more_info = [1,2,6,7]
# like_info = [1,3,4,5,7]


key_columns = {'webinars':'Email',
               'Hello Bar June 2017':'Contact Email Address',
               "ISM US 2017":"Email",
               "Inc 5000":"Unnamed: 12",
               "2016 Events":'Email',
               "Integrated Camp Lead Score 25+":'Email Address',
               "in Eloqua but not SFDC":'Email Address'}

output_newColumns = ['additional name', 'associated with', 'career', 'education', 'location', 'phone', 'place', 'age', 'image', 'fullname']


delay_min = 10
delay_max = 15

ticker_min = 25
ticker_max = 40


pipl = {"init_url": "https://pipl.com",
        "login_url": "https://pipl.com/accounts/login/",
        "email":"email",
        "password": "pw",
        "delay": 10}


import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = os.path.join(rootpath, 'log', 'log')
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.addHandler(my_handler)

