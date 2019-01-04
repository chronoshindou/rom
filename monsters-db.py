import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from IPython.display import display_html
import re
import numpy as np
import sys

#print "input?", sys.argv[0]

url = "http://www.roguard.net/db/monsters/"
res = requests.get(url)
soup = BeautifulSoup(res.content,'lxml')
nav = soup.find('nav',{'class':'page-list-mobile'})
a_tag = nav.find_all('a',href=True)[2]
#print a_tag
ch = re.findall('(\d+)',a_tag['href'])
ch = int(str(ch).strip("['']"))
print "Scraping "+str(ch)+" pages. Please wait..."
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

    i = 0

    lvl_list = []
    hp_list = []
    base_list = []
    job_list = []

    for stats in table.find_all('td',{'class':'desktop-only'}):
        vLvl = re.findall('Lv (\d+)',str(stats).strip())
        vHP = re.findall('(\d+) Hp',str(stats).strip())
        vBase = re.findall('(\d+) Base Exp',str(stats).strip())
        vJob = re.findall('(\d+) Job Exp',str(stats).strip())
        if len(vLvl)>0:
            #print "Lvl:",vLvl
            lvl_list.append(vLvl)
        if len(vHP)>0:
            #print "Hp:",vHP
            hp_list.append(vHP)
        if len(vBase)>0:
            #print "Base Exp:",vBase
            base_list.append(vBase)
        if len(vJob)>0:
            #print "Job Exp:",vJob
            job_list.append(vJob)
        i = 0
        vLvl = ''
        vHp = ''
        vBase = ''
        vJob = ''
        #print stats
        for stat in stats:
            

            
            #print stat.text
            i += 1
        #print vLvl, vHP, vBase, vJob
    lvl_list = np.array(lvl_list)
    #lvl_list = np.reshape(lvl_list,len(lvl_list),1)
    hp_list = np.array(hp_list)
    #hp_list = np.reshape(hp_list,len(hp_list),1)
    base_list = np.array(base_list)
    #base_list = np.reshape(base_list,len(base_list),1)
    job_list = np.array(job_list)
    #job_list = np.reshape(job_list,len(job_list),1)

    ch_list = np.array(ch_list)
    #ch_list = np.reshape(ch_list,len(ch_list),1)
    mon_list = np.array(mon_list)
    #mon_list = np.reshape(mon_list,(len(mon_list),1))
    #full_list = X.reshape(len(ch_list),len(mon_list))

    full_data = {'Monster Name':mon_list,'Level':lvl_list,'HP':hp_list,'Base':base_list,'Job':job_list}
    #print full_data
    #df = pd.DataFrame(index=ch_list,data=full_data)
    df = pd.DataFrame(full_data)
    #,columns=['Monster Name','Level','HP','Base','Job']
    #print df
    return df

while ch > 0:
    full_df = full_df.append(mon_urlList(ch))
    ch -= 1
full_df.index = full_df.index.map(int)
full_df = full_df.sort_index()
writer = pd.ExcelWriter('output_monsterList.xlsx')
full_df.to_excel(writer,'Monster List')
writer.save()
#print full_df