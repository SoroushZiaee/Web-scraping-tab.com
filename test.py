import time

import pandas as pd
import os
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

match_list = ['Real Betis v Real Madrid', 'Barcelona v Getafe', 'Cadiz v Osasuna',
              'Rayo Vallecano v Granada', 'Atletico Madrid v Villarreal CF',
              'Levante v Rayo Vallecano', 'Espanyol v Atletico Madrid', 'Real Madrid v Celta Vigo',
              'Villarreal CF v Alaves', 'Sevilla v Barcelona', 'Cadiz v Real Sociedad', 'Osasuna v Valencia',
              'Getafe v Elche Cf', 'Granada v Real Betis', 'Athletic Bilbao v Mallorca']

chance_list = ['28.00', '7.00', '3.00', '1.40', '4.50', '7.50', '3.20', '3.00',
               '2.30', '2.50', '3.10', '2.80', '1.80', '3.20', '4.75', '1.87',
               '3.40', '4.00', '3.80', '3.20', '2.00', '1.40', '4.75', '6.50',
               '1.52', '4.25', '5.50', '2.80', '3.30', '2.40', '4.75', '3.40',
               '1.75', '2.40', '3.20', '2.90', '1.80', '3.30', '4.50', '2.90',
               '3.20', '2.40', '1.75', '3.50', '4.50']

columns = ['home_team', 'away_team', 'home_result', 'draw', 'away_result']

print(match_list)
print(chance_list)

preprocess_chance_list = [[float(chance_list[i]), float(chance_list[i+1]), float(chance_list[i+2])] for i in range(0, len(chance_list) - 2, 3)]
print(preprocess_chance_list)

preprocess_match_list = [item.split(' v ') for item in match_list]
print(preprocess_match_list)

# print(len(preprocess_match_list) == len(preprocess_chance_list))
final_list = [(match[0], match[1], chance[0], chance[1], chance[2]) for match, chance in zip(preprocess_match_list, preprocess_chance_list)]
print(final_list)

if not os.path.exists(os.path.join(os.getcwd(), 'data')):
    os.mkdir(os.path.join(os.getcwd(), 'data'))

path = os.path.join('data', '{}.csv'.format('spanish primera division'))
print(path)

start = time.time()
if os.path.isfile(path):
    os.remove(path)
    df = pd.DataFrame(final_list, columns=columns)
    # for new_list in final_list:
    #     if ([new_list[0], new_list[1]] in df[['home_team', 'away_team']].values.tolist()) and\
    #             ([new_list[2], new_list[3], new_list[4]] not in df[['home_result', 'draw', 'away_result']].values.tolist()):
    #
    #         df.loc[(df['home_team'] == new_list[0]) & (df['away_team'] == new_list[1]), 'home_result'] = new_list[2]
    #         df.loc[(df['home_team'] == new_list[0]) & (df['away_team'] == new_list[1]), 'draw'] = new_list[3]
    #         df.loc[(df['home_team'] == new_list[0]) & (df['away_team'] == new_list[1]), 'away_result'] = new_list[4]

    df.to_csv(path, sep=',', index=False)
    print(df.head())

else:
    df = pd.DataFrame(final_list, columns=columns)
    df.to_csv(path, sep=',', index=False)
    print(df.head())

print(time.time() - start)
