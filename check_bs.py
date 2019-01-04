import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from IPython.display import display_html
import re
import numpy as np
import time

britesoft_url = ['http://bo.zeta.britesoft.com','http://bo.beta.britesoft.com','http://bo.sigma.britesoft.com/','http://lavand.com.my/','http://britesoft.com/','http://mygolf2u.com/mygolf','http://m.mygolf2u.com/','http://bo.alpha.britesoft.com','http://bo.sigma.britesoft.com/']

for url in britesoft_url:
    #t_end = time.time() + 5
    res = requests.get(url)
    print res.status_code," - ",url
    #if time.time() > t_end:
    #    continue
#soup = BeautifulSoup(res.content,'lxml')