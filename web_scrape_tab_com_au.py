from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import pandas as pd


class UrlData(object):
    URL_DICT = {
        'english premier league': 'https://www.tab.com.au/sports/betting/Soccer/competitions/English%20Premier%20League',
        'french ligue 1': 'https://www.tab.com.au/sports/betting/Soccer/competitions/French%20Ligue%201',
        'german bundesliga': 'https://www.tab.com.au/sports/betting/Soccer/competitions/German%20Bundesliga',
        'italian serie a': 'https://www.tab.com.au/sports/betting/Soccer/competitions/Italian%20Serie%20A',
        'spanish primera division': 'https://www.tab.com.au/sports/betting/Soccer/competitions/Spanish%20Primera%20Division'
    }


class WebScrapping(object):
    def __init__(self, name_league, verbose=False):
        self._verbose = verbose
        self._name_league = name_league
        self._driver_path = 'chromedriver_mac64/chromedriver'
        self._urls = UrlData().URL_DICT
        self._browser = webdriver.Chrome(self._driver_path)
        # self._browser = webdriver.PhantomJS()

        if self._verbose:
            print('-Set The Driver')
        self._set_up(self._urls[self._name_league.lower()])

    def _set_up(self, url, timeout=20, tag_name='match-name-text'):
        if self._verbose:
            print("-Get The URL and Wait for 'match-name-text' to loaded")
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



