# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 23:36:57 2019

@author: eric
"""
#package load
import pandas as pd
import requests
from selenium import webdriver
import time
import random
from tqdm import tqdm
import request
#pip install request
#pip install beautifulsoup4
from bs4 import BeautifulSoup

#driver load
driver = webdriver.Chrome('C:\\Users\\eric\\Desktop\\chromedriver.exe')

#url.get
url="https://play.google.com/store?hl=en"
driver.get(url)

#keyword_list
searchText_T = ["healthcare", "medical", "health", "diet", "disease prevention", "treatment"]


driver.find_element_by_xpath('//*[@id="gbqfq"]').send_keys(searchText_T[5])
driver.find_element_by_xpath('//*[@id="gbqfb"]/span').click()
#see more 위치인데 자주 바뀌니 확인해야함
driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/c-wiz/c-wiz[4]/c-wiz/div/div[1]/div[2]/a').click()

#1-50 url get
#xpath를 보면 위에서부터 1~50이랑 그 밑에 200개랑 xpath가 다름 그래서 for문 두번 돌림.. 더 좋은 코드가 있긴하겠지..?
app_urls=[]

for i in tqdm(range(1, 50)) :                                                                                          
    try :
        app_title = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[3]/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[2]/div[' + str(i) + ']/c-wiz/div/div/div[1]/div/div/a')
        time.sleep(1)
        url_link = app_title.get_attribute('href')
        app_urls.append(url_link)
        
    except:
        pass
    
#1-200url get    
for i in tqdm(range(1, 200)) :                                                                                          
    try :
        app_title = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[3]/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[2]/c-wiz[' + str(i) + ']/div/div/div[1]/div/div/a')
        time.sleep(1)
        url_link = app_title.get_attribute('href')
        app_urls.append(url_link)
        
    except:
        pass   

#information get
app_description=[]
app_name=[]
app_category=[]
app_info=[]
for url in tqdm(app_urls):
    try:
        request_content=requests.get(url)
        time.sleep(1)
        soup=BeautifulSoup(request_content.content,'html.parser')
        app_description.append([soup.find('div',{'jsname':'sngebd'}).getText(), url])
        app_name.append([soup.find('h1',{'class':'AHFaub'}).getText()])
        app_category.append([soup.find('a',{'itemprop':'genre'}).getText()])
        app_info.append([soup.find('div',{'class':'IxB2fe'}).getText()])
    except:
        pass
    
#dataframe화
app_description = pd.DataFrame(app_description)
app_name = pd.DataFrame(app_name)
app_category = pd.DataFrame(app_category)
app_info = pd.DataFrame(app_info)

result5=pd.concat([app_name,app_category],axis=1)
result5=pd.concat([result5,app_description],axis=1)
result5=pd.concat([result5,app_info],axis=1)
result5.head()
result5.columns=['app_name','app_category','app_description','app_url','app_info']  # 열이름바꾸기
result5.to_csv('app_treatment_crawl.csv',index=False)
app_result=pd.concat([app_result,result5])
app_result=app_result.reset_index(drop= True)
app_result.to_csv('app_all_crawl.csv',index=False)
