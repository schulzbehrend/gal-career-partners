from collections import defaultdict
import pandas as pd
from time import sleep

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

def li_login():
    '''
    Login into LinkedIn and webdriver session for more web manipulation.
    Sets up flow to search in LinkedIn head search bar.
dd
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
    co = co.replace('.', '')
    global_srch = 'https://www.linkedin.com/search/results/companies/?keywords=&origin=SWITCH_SEARCH_VERTICAL'
    driver.get(global_srch)
    wait = WebDriverWait(driver, 10)
    # Element IDs and XPATHs
    srch_x_path = '//*[@id="ember16"]/input'
    emp_srch_id = 'people-search-keywords'
    tech_rec = 'technical recruiter'
    area = 'Austin, TX Area'
    
    
    driver.find_element_by_xpath(srch_x_path).send_keys(co + Keys.RETURN)
    sleep(3)
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    first_hit = soup.find_all('a')[16]['id']
    
    if first_hit == 'globalfooter-accessibility':
        mongo.insert_one({co: 'Company Page 404'})
        return None
    
    up = ActionChains(driver)
    up.send_keys(Keys.HOME)
    up.perform()
    sleep(3)
    wait.until(EC.element_to_be_clickable((By.ID, first_hit)))
    driver.find_element_by_id(first_hit).click()
    
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'People')))
        driver.find_element_by_link_text('People').click()
    except:
        mongo.insert_one({co: 'People Link 404'})
        return None
        
    wait.until(EC.element_to_be_clickable((By.ID, emp_srch_id))) 
    driver.find_element_by_id(emp_srch_id).send_keys(tech_rec + Keys.RETURN)
    sleep(5)
    driver.find_element_by_id(emp_srch_id).send_keys(area + Keys.RETURN)
    
    wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'ul'))) 
    scroll_to_end(driver, 3)
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    # TODO insert mongo raw scrape
    results = soup.find('ul', 'org-people-profiles-module__profile-list')
    
    if results is None:
        mongo.insert_one({co: 'No results'})
        return None
    
    d = construct_record(results, co)
    mongo.insert_one(d)
    return None

def scroll_to_end(driver, timeout):
    # TODO docstring
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

def construct_record(results, co):
    # TODO docstring
    contact_elements = results.find_all('li', 'org-people-profiles-module__profile-item')
    
    d = defaultdict(dict)
    
    for contact in contact_elements:
        name = contact.find('div', 'org-people-profile-card__profile-title t-black lt-line-clamp lt-line-clamp--single-line ember-view')
        if name is None:
            continue
        name = name.text.rstrip().replace(' ', '', 2)
        name = name.replace('.', '')
        link = 'https://www.linkedin.com' + contact.a['href']

        if co not in d:
            d[co]

        if name not in co:
            d[co][name] = link
    
    return d


if __name__ == '__main__':
    cos = pd.Series(cos_list)

    driver = li_login()

    mongo.connect_mongo()
    mongo.connect_coll('gal_part_proj', 'ATX_tech_rec')

    # testing segments of company list
    #   First: first 10, 0:9
    cos[:9].apply(lambda x: scrape_contacts(driver, x))

    mongo.close_mongo()
    driver.close()