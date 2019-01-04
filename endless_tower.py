import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from IPython.display import display_html
import re
import numpy as np
import sys
url = 'http://www.roguard.net/game/endless-tower/'


res = requests.get(url)

soup = BeautifulSoup(res.content,'lxml')
mType = sys.argv[1] 
#'mini' #mini mvp
varMon = sys.argv[2]
varMon = varMon.capitalize()
print "Scraping for ",mType," - ",varMon,". Please wait..."
#"Eclipse"
div = soup.find('div', {'id':'et-'+mType+'-list'})
table = div.find_all('table')[0]
floor_list = []
i = 0
for thead in table.find_all('thead'):
    for floor in thead.find_all('th'):
        floor_list.append(floor.text.strip())
        i += 1
ch_list = []
content_list = []
col_no = 1
k = 0
for tbody in table.find_all('tbody'):
    k = 0
    for row in tbody.find_all('tr'):
        col_no = 1
        for channel in row.find_all('td'):
            ch = re.match("(\d+)",channel.text)
            if ch:
                ch_list.append(ch.group(0))
            if len(channel.contents) >= 3:
                mon_list = str(channel.contents)
                matched = re.findall('title="([\w\s]+)',mon_list)
                matched = [m.strip() for m in matched]
                m_list = ",".join(matched)
                content_list.append(m_list)
            elif len(channel.contents) == 1:
                content_list.append(channel.contents[0])

            col_no += 1
        k += 1

mon_list = []
X = np.array(content_list,dtype=object)

#print ch_list
#print floor_list

content_list = X.reshape(len(ch_list),len(floor_list))
td = table.find_all('td',{'class':'align-middle'})

df = pd.DataFrame(index=ch_list,columns=floor_list,data=content_list)
df.pop('')
f = df.copy()
floor_list.pop(0)


filtered = []
varCntFlr = 0

_df = df.transpose()




writer = pd.ExcelWriter('./output/et/'+mType+'-'+varMon+'.xlsx')
df.to_excel(writer,'Sheet1')
_df.to_excel(writer,'Sheet2')
vX = 0
for x in floor_list:
    xdf = df[df[x].str.contains(varMon)]
    xdf_t = xdf.transpose()
    xdfN = xdf[x].shift(-1)
    xdfN = xdfN.str.contains(varMon)
    #xdfN = df[df[x].str.contains(varMon)]
    
    #___xdf = f.loc[f[x].str.contains(varMon)]
    #xdfN = xdf[x].shift(-1)
    #x_next = next(x)
    
    #xdfN.to_excel(writer,x)
    xdf.to_excel(writer,x)
    #xdf_t.to_excel(writer,'T-'+x)
    
    
    #___xdf.to_excel(writer,'Filtered '+x)
    #print xdfN
    #xdf.to_excel(writer,'SheetA')
    #xdfN.to_excel(writer,'SheetB')
    #__df = df.loc[df[x]=='Smokie']
    #__df = __df.loc[__df[x].shift(-1)=='Smokie']
    #__df.to_excel(writer,x)
    vX += 1
writer.save()
print "Done"
#print "For ",mType," - ",varMon
#writer.save()

for x in floor_list:
    _f = f.loc[f[x]=="Smokie"]

def not_used():
    
    for x in floor_list:
        #print [f[x]=="Smokie"]
        _f = f.loc[f[x] == 'Smokie']
        if _f:
            filtered.append(f.loc[f[x] == 'Smokie'])
        '''if :
            filtered.append(x)
            
            filtered = dict([
                (x,f[x]=="Smokie")
            ])
            
        '''
        print _f
        varCntFlr += 1