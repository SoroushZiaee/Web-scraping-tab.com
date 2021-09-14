from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import pandas as pd
import re
from tqdm import tqdm
import time


class UrlData(object):
    def __init__(self, season='2020-2021'):
        self._season = season
        self.URL_DICT = {
            'english premier league': 'https://www.tab.com.au/sports/betting/Soccer/competitions/English%20Premier%20League',
            'french ligue 1': 'https://www.tab.com.au/sports/betting/Soccer/competitions/French%20Ligue%201',
            'german bundesliga': 'https://www.tab.com.au/sports/betting/Soccer/competitions/German%20Bundesliga',
            'italian serie a': 'https://www.tab.com.au/sports/betting/Soccer/competitions/Italian%20Serie%20A',
            'spanish primera division': 'https://www.tab.com.au/sports/betting/Soccer/competitions/Spanish%20Primera%20Division'
        }

        self.URL_HISTORY = {
            'english premier league': {
                '2020-2021':'https://globalsportsarchive.com/competition/soccer/premier-league-2020-2021/regular-season/47188/',
                '2019-2020':'https://globalsportsarchive.com/competition/soccer/premier-league-2019-2020/regular-season/32365/',
                '2018-2019':'https://globalsportsarchive.com/competition/soccer/premier-league-2018-2019/regular-season/22226/',
                '2017-2018':'https://globalsportsarchive.com/competition/soccer/premier-league-2017-2018/regular-season/12875/',
                '2016-2017':'https://globalsportsarchive.com/competition/soccer/premier-league-2016-2017/regular-season/8171/',
                },
            'french ligue 1': {
                '2020-2021':'https://globalsportsarchive.com/competition/soccer/ligue-1-uber-eats-2020-2021/regular-season/46313/',
                '2019-2020':'https://globalsportsarchive.com/competition/soccer/ligue-1-conforama-2019-2020/regular-season/32460/',
                '2018-2019':'https://globalsportsarchive.com/competition/soccer/ligue-1-conforama-2018-2019/regular-season/22368/',
                '2017-2018':'https://globalsportsarchive.com/competition/soccer/ligue-1-conforama-2017-2018/regular-season/12876/',
                '2016-2017':'https://globalsportsarchive.com/competition/soccer/ligue-1-2016-2017/regular-season/8078/',
                },
            'german bundesliga': {
                '2020-2021':'https://globalsportsarchive.com/competition/soccer/bundesliga-2020-2021/regular-season/46282/',
                '2019-2020':'https://globalsportsarchive.com/competition/soccer/bundesliga-2019-2020/regular-season/32358/',
                '2018-2019':'https://globalsportsarchive.com/competition/soccer/bundesliga-2018-2019/regular-season/22112/',
                '2017-2018':'https://globalsportsarchive.com/competition/soccer/bundesliga-2017-2018/regular-season/12874/',
                '2016-2017':'https://globalsportsarchive.com/competition/soccer/bundesliga-2016-2017/regular-season/8135/',
                },
            'italian serie a': {
                '2020-2021':'https://globalsportsarchive.com/competition/soccer/serie-a-tim-2020-2021/regular-season/48277/',
                '2019-2020':'https://globalsportsarchive.com/competition/soccer/serie-a-tim-2019-2020/regular-season/33487/',
                '2018-2019':'https://globalsportsarchive.com/competition/soccer/serie-a-tim-2018-2019/regular-season/23375/',
                '2017-2018':'https://globalsportsarchive.com/competition/soccer/serie-a-tim-2017-2018/regular-season/13503/',
                '2016-2017':'https://globalsportsarchive.com/competition/soccer/serie-a-tim-2016-2017/regular-season/8404/',
                },
            'spanish primera division': {
                '2020-2021':'https://globalsportsarchive.com/competition/soccer/laliga-santander-2020-2021/regular-season/48255/',
                '2019-2020':'https://globalsportsarchive.com/competition/soccer/laliga-santander-2019-2020/regular-season/33486/',
                '2018-2019':'https://globalsportsarchive.com/competition/soccer/laliga-santander-2018-2019/regular-season/23337/',
                '2017-2018':'https://globalsportsarchive.com/competition/soccer/laliga-santander-2017-2018/regular-season/13847/',
                '2016-2017':'https://globalsportsarchive.com/competition/soccer/laliga-santander-2016-2017/regular-season/8403/',
            }
        }


class WebScrapping(object):
    def __init__(self, name_league, verbose=False):
        self._verbose = verbose
        self._name_league = name_league
        self._driver_path = 'chromedriver_mac64/chromedriver'
        self._urls = UrlData().URL_DICT

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self._browser = webdriver.Chrome(self._driver_path, options=options)

        if self._verbose:
            print('-Set The Driver')
        self._set_up(self._urls[self._name_league.lower()])

    def _set_up(self, url, timeout=20, tag_name='match-name-text'):
        if self._verbose:
            print(f"-Get The URL and Wait for '{tag_name}' to loaded")
        self._browser.get(url)
        try:
            WebDriverWait(self._browser, timeout=timeout).until(
                EC.visibility_of_element_located((By.CLASS_NAME, tag_name))
            )
        except TimeoutException:
            print('Timed out waiting for page to load')
            self._browser.quit()

    def _get_response(self, tag_name='match-name-text'):
        return self._browser.find_elements_by_class_name(tag_name)

    @staticmethod
    def _is_exist(path):
        return os.path.isfile(path)

    def _get_result(self):
        if self._verbose:
            print('-Get The Data of matches and chances')
        matches = [match.text.split(' v ') for match in self._get_response('match-name-text')]
        temp_chances = self._get_response('animate-odd')
        chances = [[temp_chances[i].text, temp_chances[i + 1].text, temp_chances[i + 2].text] for i in range(0, len(temp_chances) - 2, 3)]

        return [[match[0], match[1], chance[0], chance[1], chance[2]] for match, chance in zip(matches, chances)]

    def crawl(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'data')):
            os.mkdir(os.path.join(os.getcwd(), 'data'))

        path = os.path.join(os.getcwd(), 'data', f'{self._name_league}.csv')

        if self._is_exist(path):

            if self._verbose:
                print('-Update The Result of Matches')
            columns = ['home_team', 'away_team', 'home_result', 'draw', 'away_result']
            df = pd.DataFrame(self._get_result(), columns=columns)
            df.to_csv(path, sep=',', index=False)

        else:
            columns = ['home_team', 'away_team', 'home_result', 'draw', 'away_result']
            df = pd.DataFrame(self._get_result(), columns=columns)
            if self._verbose:
                print('-Save The Result of Matches')
            df.to_csv(path, sep=',', index=False)


class WebScrappingHistory(object):
    def __init__(self, name_league, season='2020-2021', verbose=False): 
        self._verbose = verbose
        self._season = season
        self._name_league = name_league
        self._driver_path = 'chromedriver_mac64/chromedriver'
        self._url = UrlData(self._season).URL_HISTORY

        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        self._browser = webdriver.Chrome(self._driver_path)

        if self._verbose:
            print('-Set The Driver')

        self._set_up(self._url[self._name_league.lower()][self._season], timeout=20, tag_name='gsa-c-team_full')

    def _set_up(self, url, timeout=20, tag_name='match-name-text'):
        if self._verbose:
            print(f"-Get The URL and Wait for '{tag_name}' to loaded")
        self._browser.get(url)
        try:
            WebDriverWait(self._browser, timeout=timeout).until(
                EC.visibility_of_element_located((By.CLASS_NAME, tag_name))
            )
        except TimeoutException:
            print('Timed out waiting for page to load')
            self._browser.quit()

    def _get_response(self, tag_name='match-name-text'):
        return self._browser.find_elements_by_class_name(tag_name)

    @staticmethod
    def _is_exist(path):
        return os.path.isfile(path)

    @staticmethod
    def _convert_one_hot_result(sample_list: list):
        final_result = []
        for item in sample_list:
            if item[0] == item[1]:
                final_result.append([0, 1, 0])
        
            elif item[0] > item[1]:
                final_result.append([1, 0, 0])
            
            else:
                final_result.append([0, 0, 1])
        
        return final_result

    def _get_result(self):
        if self._verbose:
            print('-Get The Data of matches and result')

        gameweek = int(re.findall(r'\d+', self._browser.find_element_by_id('week_sel').text)[0])    
        week_pre = self._browser.find_element_by_id('week_prev')
        final_result = []

        for i in tqdm(range(gameweek+1)):
            time.sleep(1)
            team_list = self._get_response('gsa-c-team_full')
            matches = [(team_list[i].text, team_list[i+1].text) for i in range(0, len(team_list) - 1, 2)]
            result_list = self._get_response('gsa-c-match-c3')
            results = self._convert_one_hot_result([list(map(int, item.text.strip().replace(' ', '').split(':'))) for item in result_list])
            
            final_result += [[team[0], team[1], result[0], result[1], result[2]]for team, result in zip(matches, results)]
            week_pre.click()
        
        return final_result

    def crawl(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'data')):
            os.mkdir(os.path.join(os.getcwd(), 'data'))

        path = os.path.join(os.getcwd(), 'data', f'{self._name_league}-{self._season}.csv')

        if self._is_exist(path):

            if self._verbose:
                print('-Update The Result of Matches')
            columns = ['home_team', 'away_team', 'home_result', 'draw', 'away_result']
            df = pd.DataFrame(self._get_result(), columns=columns)
            df.to_csv(path, sep=',', index=False)

        else:
            columns = ['home_team', 'away_team', 'home_result', 'draw', 'away_result']
            df = pd.DataFrame(self._get_result(), columns=columns)
            if self._verbose:
                print('-Save The Result of Matches')
            df.to_csv(path, sep=',', index=False)
        



        
        

        
