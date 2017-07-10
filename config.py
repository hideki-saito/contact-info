import os

rootpath = os.path.dirname(os.path.realpath(__file__))


filename = "temp.xlsx"


more_info = [1,2,6,7]
like_info = [1,3,4,5,7]


key_columns = {'webinars':'Email',
               'Hello Bar June 2017':'Contact Email Address',
               "ISM US 2017":"Email",
               "Inc 5000":"Website",
               "2016 Events":'Email',
               "Integrated Camp Lead Score 25+":'Email Address',
               "in Eloqua but not SFDC":'Email Address'}


delay_min = 8
delay_max = 15


pipl = {"init_url": "https://pipl.com",
        "login_url": "https://pipl.com/accounts/login/",
        "email":"saito_hideki.1127@outlook.com",
        "password": "pipl1127",
        "delay": 10}


