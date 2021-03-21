import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import os
import time
import logging

logging.basicConfig(filename='./Desktop/log/104.log',level=logging.ERROR,format='%(asctime)s:%(levelname)s:%(message)s')

resource_path = './Desktop/104/'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)


search_url = "https://www.104.com.tw/jobs/search/?ro=0&keyword=%E5%A4%A7%E6%95%B8%E6%93%9A&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=14&asc=0&page={}&mode=s&jobsource=2018indexpoc"


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'} 


df = pd.DataFrame(columns = ["工作職稱", "公司名稱", "工作內容:", "連結" ,"接受身分" ,"聯絡人" ,"email" ,"所需技能" ])

l=1
n=1
for i in range(1,n+1):
    res = requests.get(search_url.format(i), headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article = soup.select('article')
    
    
    for each_article in article:
        try:
    #         P_class = each_article.find('p').getText()
            P_class = each_article.select('p')[0].text     #此方法和上面一樣
            
            #json
            s = 'https:' + each_article.a['href']
            s1 = s.split("?") 
            link = s1[0]
            s2 = s1[0].split("/")
            json_url = "https://www.104.com.tw/job/ajax/content/"+s2[4]
            headers1 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            "Referer": "{}".format(link)} 
            response = requests.get(url = json_url, headers = headers1)
            data = json.loads(response.text)
            
            #內文
            tempj = ','.join(j['description']for j in data['data']['condition']['acceptRole']['role'])
            tempK = '"'+ (','.join([ k['description'] for k in data['data']['condition']['specialty'] ])) + '"'
            df.loc[l] = [each_article["data-job-name"], each_article["data-cust-name"],P_class, link,
                        tempj,
                        data['data']['contact']['hrName'],
                        data['data']['contact']['email'] ,
                        tempK
                        ]
            l += 1
            
            
            
            
        except Exception as e:
            logging.error(search_url,exc_info=True)
            # print(e)
           
df.to_csv('./Desktop/104/104_1.csv', index=False, encoding='utf-8')

    


        
    
   
    

