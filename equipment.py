import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from IPython.display import display_html
import re
import numpy as np

url = "http://www.roguard.net/db/equipment/"
res = requests.get(url)
soup = BeautifulSoup(res.content,'lxml')
nav = soup.find('nav',{'class':'page-list-mobile'})
a_tag = nav.find_all('a',href=True)[2]
#print a_tag
ch = re.findall('(\d+)',a_tag['href'])
ch = int(str(ch).strip("['']"))
print "Scraping "+ch+" items. Please wait..."
i = 1
full_df = pd.DataFrame()

def mon_urlList(x):      
    res = requests.get(url+'?page='+str(x))
    soup = BeautifulSoup(res.content,'lxml')
    mType = 'mini' #mini mvp
    varMon = "Smokie"
    global full_df
    div = soup.find('div', {'id':'content'})
    table = div.find_all('table')[0]
    mon = table.find_all('a')
    ch_list = []
    mon_list = []
    for a_tag in table.find_all('a', href=True):
        ch = re.findall('(\d+)',a_tag['href'])
        ch_list.append(ch)
        mon_list.append(a_tag.text)
    X = np.append(ch_list,mon_list)

    ch_list = np.array(ch_list)
    ch_list = np.reshape(ch_list,len(ch_list),1)
    mon_list = np.array(mon_list)
    mon_list = np.reshape(mon_list,(len(mon_list),1))
    #full_list = X.reshape(len(ch_list),len(mon_list))
    df = pd.DataFrame(index=ch_list,data=mon_list,columns=['Equipment Name'])
    return df

while ch > 0:
    full_df = full_df.append(mon_urlList(ch))
    ch -= 1
full_df.index = full_df.index.map(int)
full_df = full_df.sort_index()
writer = pd.ExcelWriter('output_eqList.xlsx')
full_df.to_excel(writer,'Equipment List')
writer.save()
print full_df