from collections import defaultdict
import pandas as pd
from time import sleep
import glob
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import chromedriver_binary
from bs4 import BeautifulSoup

import mongo
from companies import cos_list

def get_login():
    '''
    Access keys from external file and placed in a list.

    Parameters
    ----------
    None:

    Returns
    ----------
    creds: (list)
        Return keys used for session.
    '''
    f = open('../data/LI_login.txt', 'r')
    creds = f.readlines()

    for idx, key in enumerate(creds):
        creds[idx] = key.replace('\n', '')

    return creds

def login():
    '''
    Login into LinkedIn and webdriver session for more web manipulation.
    Keys generated from get_login() function.

    Parameters
    ----------
    None:

    Returns
    ----------
    driver: (selenium.webdriver.chrome.webdriver.WebDriver)
        Return webdriver session for web manipulation.
    '''
    # session keys for LI instance
    email, pw = get_login()
    
    # selenium webdriver
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/')
    # log in
    sleep(2)
    driver.find_element_by_id('session_key').send_keys(email)
    sleep(1)
    driver.find_element_by_id('session_password').send_keys(pw+Keys.RETURN)

    return driver

def scrape_location(driver, url, frame=None):
    '''
    Go to LinkedIn user's URL and scrape work location.
    
    Parameters
    ----------
    driver: (selenium.webdriver.chrome.webdriver.WebDriver)
        Selenium Chrome Webdriver for site interaction.
    url: (str)
        LinkedIn user's URL.

    Returns
    ----------
    location: (str)
        Return string of LinkedIn user's work location.
    '''
    sleep(5)
    # frame.to_csv('../data/tech_rec/_techrecruiters_with_location.csv', mode='a', index=False)
    sleep(3)
    driver.get(url)
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    flex_card = soup.find('div', 'flex-1 mr5')
    location = flex_card.find('li', 't-16 t-black t-normal inline-block')
    location = location.text.lstrip().rstrip()
    sleep(3)
    # frame.to_csv('../data/techrecruiters_with_location.csv', mode=)

    return location

def main():
    '''
    Open local CSVs into one DataFrame, scrape LinkedIn users work location and 
    append to original Dataframe. Save new DataFrame to local CSV.

    Parameters
    ----------
    None:

    Returns
    ----------
    None:
    '''
    path = '../data/tech_rec' # use your path
    all_files = glob.glob(path + "/*.csv")
    lst = []
    
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0, names=['recruiter', 'url'])
        co_name = filename
        co_name = co_name.split('/')[-1]
        co_name = co_name[:-4]
        df['co_name'] = co_name
        lst.append(df)
    
    frame = pd.concat(lst, axis=0, ignore_index=True)
    frame['location'] = ''

    if not os.path.exists('../data/tech_rec/_techrecruiters_with_location.csv'):
        open('../data/tech_rec/_techrecruiters_with_location.csv')
        # frame.to_csv('../data/tech_rec/_techrecruiters_with_location.csv', index=False)

    n = 10 # number or rows
    df_seg = [frame[i:i+1] for i in ragne(1, frame.shape[0], n)]
    driver = login()

    for df in df_seg[:1]:
        df['location'] = df['url'].apply(lambda url: scrape_location(driver, url))
        frame.to_csv('../data/tech_rec/_techrecruiters_with_location.csv', mode='a', index=False)
    
    driver.close()

if __name__ == '__main__':
    main()