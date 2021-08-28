from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver_path = 'chromedriver_mac64/chromedriver'
start = time.time()
url = 'https://www.tab.com.au/sports/betting/Soccer/competitions/Spanish%20Primera%20Division'
browser = webdriver.Chrome(executable_path=driver_path)
browser.get(url)
timeout = 20

try:
    WebDriverWait(browser, timeout=timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "match-name-text")))
    match_list = browser.find_elements_by_class_name('match-name-text')
    home_list = browser.find_elements_by_class_name('animate-odd')
    match_list_text = [item.text for item in match_list]
    home_chance = [[home_list[i].text, home_list[i+1].text, home_list[i+2].text] for i in range(len(home_list) - 2)]
    print(match_list_text)
    print(home_chance)
    print(f'The Time Of Execution {time.time() - start}')
    browser.quit()
except TimeoutException:
    print('Timed out waiting for page to load')
    browser.quit()


