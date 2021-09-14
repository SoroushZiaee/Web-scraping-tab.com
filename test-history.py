from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import pandas as pd
import re
import time
from tqdm import tqdm



driver_path = 'chromedriver_mac64/chromedriver'
season = '2020-2021'
url = f'https://globalsportsarchive.com/competition/soccer/laliga-santander-{season}/regular-season/48255/'
browser = webdriver.Chrome(driver_path)
timeout = 20


try:
    browser.get(url)
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'gsa-c-team_full')))
    gameweek = int(re.findall(r'\d+', browser.find_element_by_id('week_sel').text)[0])
    week_pre = browser.find_element_by_id('week_prev')
    columns = ['home_team', 'away_team', 'home_result', 'draw', 'away_result']
    result = []
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    for i in tqdm(range(gameweek+1)):
        time.sleep(1)

        selenium_team_list = browser.find_elements_by_class_name('gsa-c-team_full')
        selenium_result_list = browser.find_elements_by_class_name(('gsa-c-match-c3'))
        team_name = [(selenium_team_list[i].text, selenium_team_list[i+1].text) for i in range(0, len(selenium_team_list) - 1, 2)]
        result_match = [list(map(int, item.text.strip().replace(' ', '').split(':'))) for item in selenium_result_list]
        final_resutl = []
        for item in result_match:
            if item[0] == item[1]:
                final_resutl.append([0, 1, 0])
            
            elif item[0] > item[1]:
                final_resutl.append([1, 0, 0])
            
            else:
                final_resutl.append([0, 0, 1])
        
        result += [[team[0], team[1], result[0], result[1], result[2]]for team, result in zip(team_name, final_resutl)]
        # 

        week_pre.click()
        # time.sleep(0.5)
        

    df = pd.DataFrame(result, columns=columns)
    df.to_csv(f'{season}.csv')
    browser.close()

except TimeoutException:
    print('Timed out waiting for page to load')
    browser.quit()


browser.quit()
