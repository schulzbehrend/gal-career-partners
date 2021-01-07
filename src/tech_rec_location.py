from collections import defaultdict
import pandas as pd
import numpy as np
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
# import scroll

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
    # sleep(3)
    driver.get(url)
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    flex_card = soup.find('div', 'flex-1 mr5')
    try:
        location = flex_card.find('li', 't-16 t-black t-normal inline-block')
        if location == None:
            return 'Information not provided.'
    except:
        return '404'
    location = location.text.lstrip().rstrip()
    # frame['location'].append(location, ignore_index=True)
    sleep(3)
    # frame.to_csv('../data/techrecruiters_with_location.csv', mode='a')

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
    path = '../data/tech_rec'
    all_files = glob.glob(path + "/*.csv")
    csv_name = '../data/tech_rec/_techrecruiters_with_location.csv'
    lst = []
    # scroll.main()
    
    #TODO: functionize
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0, names=['recruiter', 'url'])
        co_name = filename
        co_name = co_name.split('/')[-1]
        co_name = co_name[:-4]
        df['co_name'] = co_name
        lst.append(df)
    
    frame = pd.concat(lst, axis=0, ignore_index=True)
    frame['location'] = ''
    df = pd.DataFrame(columns=frame.columns)

    if not os.path.exists(csv_name):
        df.to_csv(csv_name, index=False)

    driver = login()
    #TODO: functionize
    for idx, row in frame[2202:3200].iterrows():
        location = scrape_location(driver, row['url'])
        row['location'] = location
        df = df.append(row)
        print(df.loc[idx:])
        df.loc[idx:].to_csv(csv_name, mode='a', index=False, header=False)
    
    driver.close()

if __name__ == '__main__':
    main()