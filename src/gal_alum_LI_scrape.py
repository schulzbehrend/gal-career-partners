from collections import defaultdict
import pandas as pd
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from bs4 import BeautifulSoup

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

def li_login():
    '''
    Login into LinkedIn and webdriver session for more web manipulation.
    Sets up flow to search in LinkedIn head search bar.

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
    driver.find_element_by_id('session_key').send_keys(email)
    driver.find_element_by_id('session_password').send_keys(pw)
    driver.find_element_by_id('session_password').send_keys(Keys.RETURN)

    return driver

def scrape_contacts(driver, co):
    '''
    Search company (co) in LinkedIn head search bar and scrape that company's contacts of interest.
    Returns dictionary of {co: {name: link}}

    Parameters
    ----------
    driver: (selenium.webdriver.chrome.webdriver.WebDriver)
        Webdriver session for web manipulation.
    co: (str)
        Company string to search in head search bar.

    Returns
    ----------
    d: (dict)
        Return dictionary for mongo DB insert.
    '''
    # XPaths
    # Click first item when search company
    srch_x_path = '//*[@id="ember16"]/input'
    co_x_path = '/html/body/div[7]/div[3]/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/span/div/span/span/a'
    ppl_x_path = '/html/body/div[7]/div[3]/div/div[3]/div[2]/div[1]/div/div/nav/ul/li[5]/a'
    
    
    sleep(5)
    driver.find_element_by_xpath(srch_x_path).send_keys(co + Keys.RETURN)
    sleep(2)
    try:
        driver.find_element_by_xpath(co_x_path).click()
        driver.find_element_by_xpath(srch_x_path).clear()
        return 'PASS', co
    except:
        driver.find_element_by_xpath(srch_x_path).clear()
        return 'FAIL', co
    sleep(2)

def main():




if __name__ == '__main__':
    df = pd.read_csv('../data/glassdoor_scrape_1.csv')
    df.dropna(inplace=True)
    edu_flag = df['industry'].apply(lambda x: True if 'College' in x else False)
    cos = pd.Series(df.name[~edu_flag].unique())

    driver = li_login()
    cos_scrape = cos.apply(lambda x: scrape_contacts(driver, x))
    pickle.dump(cos_scrape, open( "save.pkl", "wb" ))
