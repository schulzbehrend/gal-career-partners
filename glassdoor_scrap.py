import pandas as pd 
from bs4 import BeautifulSoup
import requests
import json
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient

client = MongoClient()
db = client.web_scrape
# db.html.drop()
html = db.html
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(executable_path="/Users/jrw/Desktop/chromedriver", options=options)
driver.set_window_size(1120, 1000)
driver.implicitly_wait(1)
# response = requests.get(url)
# content = response.content
# content
# soup = BeautifulSoup(content, 'html.parser')
# soup.find_all('div', 'row d-flex flex-wrap')

# html.find({'_id': '5f97ec870ae40ad8cf97afa0'})
# html.delete_one({'html':'test'})

#looping through and inserting html into mongo, may need to go back and run again
#used selenium instead of requests because requests sent errors(maybe lack of headers)
# for i in range(1,677):
#     url = f'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3.5&page={i}&isHiringSurge=0&locId=60&locType=M&locName=Austin,%20TX%20Area'
#     driver.get(url)
#     content = driver.page_source
#     html.insert_one({'html': content})
#     time.sleep(1)

#different method than above, too many duplicates with that logic, gonna try click
url = 'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3.5&page=671&isHiringSurge=0&locId=60&locType=M&locName=Austin,%20TX%20Area'
driver.get(url)
html.insert_one({'html': driver.page_source})
driver.find_element_by_xpath('/html/body/article/div/div/div/div/div/div[3]/div/ul/li[1]/button').click()
wait = WebDriverWait(driver,5)

for i in range(671,676):
    
    driver.find_element_by_xpath('/html/body/article/div/div/div/div/div/div[3]/div/ul/li[7]/button').click()
    time.sleep(2.5)
    # wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/article/div')))
    content = driver.page_source
    html.insert_one({'html': content})
    

# count = 0
# for i in html.find():
#     print(i)
#     count += 1
#     if count > 2:
#         break

test = []
for content in html.find():
    soup = BeautifulSoup(content['html'], 'html.parser')
    companies = soup.find_all('div', 'row d-flex flex-wrap')
    # print(content['html'])
    test.append(companies)
    # count += 1
    # if count > 10:
    #     break

df = []
for companies in test:
    for company in companies:
        df1= {}
        df1['name']= company.find('h2').text
        df1['size']= company.find_all('span', 'common__commonStyles__subtleText d-block mt-0')[1].text
        df1['industry']= company.find_all('span', 'common__commonStyles__subtleText d-block mt-0')[2].text
        df1['job_url']= 'glassdoor.com' + company.find_all('a')[-2]['href']
        df1['overview_url']= 'glassdoor.com' + company.find_all('a')[-1]['href']
        df.append(df1)

df1 = pd.DataFrame.from_records(df)
df1.name.nunique()
df1.name.value_counts()
df1.info()

df1.head()
df1.tail()
df1.to_csv('glassdoor_scrape_1.csv')


company_names

'''ok, we have reached a good stopping point for the morning. looks like we have a bunch of
scrapes of the first page. next steps are going to be formulating the logic to get everything
into a dataframe to then get it into a csv to take into google sheets and play around with, will
probably have to scrape a bit more. might have something to do with the specific url I am using.
If we notice that we did not get the majority of companies we were looking for, then we can
scrape again.'''






soup = BeautifulSoup(content, 'html.parser')

#this will snag the container all the info i need is in
companies = soup.find_all('div', 'row d-flex flex-wrap')

#name of company
companies[0].find('h2').text

#this will be a list of info that i will need to grab, 1 & 2 i think but check
companies[0].find_all('span', 'common__commonStyles__subtleText d-block mt-0')[2].text

#list of hrefs that need to be concatenated with glassdoor.com, probs will want -1, -2
'glassdoor.com' + companies[0].find_all('a')[-1]['href']

