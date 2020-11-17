from bs4 import BeautifulSoup
import pandas as pd
import requests
from typing import Union

from .clean import Cleaner

BASE_URL = 'https://www.pro-football-reference.com'
YEAR = 2020


class Scrape:

    @staticmethod
    def get_fantasy_standings(position: str = None, year: int = YEAR):
        """ Returns a pandas dataframe of fantasy standings  """
        r = requests.get(BASE_URL + f'/years/{year}/fantasy.htm')
        soup = BeautifulSoup(r.text, 'lxml')
        df = pd.read_html(soup.prettify())[0]
        df = Cleaner.clean_fantasy_standings(df)

        valid_positons = ['QB', 'TE', 'RB', 'WR']

        if position is not None and position.upper() in valid_positons:
            df = df[df['FANTPOS'] == position]
            df.reset_index(drop=True, inplace=True)
        elif position is not None and position not in valid_positons:
            raise KeyError(f'{position} is not one of {valid_positons}')

        return df

    @staticmethod
    def get_player_info(year: int = YEAR):
        """ Returns dict containing player's PFR links and posititions """
        player_info_dict = {}

        df = Scrape.get_fantasy_standings()

        URL = BASE_URL + f'/years/{year}/fantasy.htm'
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml')

        players_raw = soup.find_all('td', {'data-stat': 'player'})

        for player_raw in players_raw:
            name = player_raw.find('a').contents[0].upper().strip()
            prof_link = player_raw.find('a', href=True)['href']

            pos = df.loc[df['PLAYER'] == name]['FANTPOS'].iloc[0]

            player_info_dict[name] = {'PROFILE': prof_link, 'POSITION': pos}

        return player_info_dict

    @staticmethod
    def get_player_gamelog(player: str, player_info_dict: dict = None):
        """ Returns a pandas df of the player's career games """
        player = player.strip().upper()

        # Note if we repeatedly called this method we would want to pass
        # the dict to ensure we do not cause too much traffic to PFR
        if player_info_dict is None:
            player_info_dict = Scrape.get_player_info()

        position = player_info_dict[player]['POSITION']
        prof_link = player_info_dict[player]['PROFILE']

        URL = BASE_URL + prof_link[:-4] + '/gamelog/'
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml')
        df = pd.read_html(soup.prettify())[0]

        if position != 'QB':
            df = Cleaner.clean_rb_gamelog(df)
        # else:
        #     df = Cleaner.clean_qb_gamelog(df)

        return df

    @staticmethod
    def save_player_gamelogs(players: Union[list, str]):
        """ Locally saves gamelogs for players to a csv file """
        pass
