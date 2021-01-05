from collections import defaultdict
import pandas as pd
from time import sleep
import glob

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

def scrape_location(driver, url):
    '''scrape tech recruiters location info'''
    sleep(3)
    driver.get(url)
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    flex_card = soup.find('div', 'flex-1 mr5')
    location = flex_card.find('li', 't-16 t-black t-normal inline-block')
    location = location.text.lstrip().rstrip()
    sleep(3)

    return location

def main():
    path = '../data/tech_rec' # use your path
    all_files = glob.glob(path + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0, names=['recruiter', 'url'])
        co_name = filename
        co_name = co_name.split('/')[-1]
        co_name = co_name[:-4]
        df['co_name'] = co_name
    li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)

    driver = login()
    location = frame['url'].apply(lambda x: scrape_location(driver, x))
    frame['location'] = location
    frame.to_csv('../data/tech_rec/techrecruiters_with_location.csv')

if __name__ == '__main__':
    main()