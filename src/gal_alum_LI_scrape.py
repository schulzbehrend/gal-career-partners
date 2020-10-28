from collections import defaultdict

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
