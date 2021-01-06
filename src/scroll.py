from time import sleep
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
    
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/')
    sleep(2)
    driver.find_element_by_id('session_key').send_keys(email)
    sleep(1)
    driver.find_element_by_id('session_password').send_keys(pw+Keys.RETURN)

    return driver

def inf_scroll(driver, timeout):
    '''
    Scroll to end of page.

    Parameters
    ----------
    driver: (selenium.webdriver.chrome.webdriver.WebDriver)
        Webdriver session for web manipulation.
    timoeut: (int)
        Number of seconds (s) to sleep before next action.

    Returns
    ----------
    None: (NoneType)
    '''
    scroll_pause_time = timeout

    while True:
        # Scroll 100 pixels?
        sleep(scroll_pause_time)
        # driver.execute_script("window.scrollTo(0, 100);")
        driver.execute_script("window.scrollTo(0, window.scrollY + 3000)")
    return None

def main():
    '''
    log in
    whilte tech_rec_location.py ### --> kick off when starting?
        sleep(30)
        small scroll
    '''
    driver = login()
    inf_scroll(driver, 45)


if __name__ == '__main__':
    main()
