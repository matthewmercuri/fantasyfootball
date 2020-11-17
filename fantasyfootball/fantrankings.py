import pandas as pd
import time

from fantstats import FantasyStats
from scraper import scrape

YEAR = 2020
SS1_REC_GAMES_BIAS = 0.5
SS2_REC_GAMES_BIAS = 0.75


class Rankings:
    def __init__(self):
        self.FantStats = FantasyStats(year=YEAR)
        self.players_info_dict = self.FantStats.players_info_dict

    def _add_features(self, name, df):
        '''
        TODO:
        - need to add features that are relative to peers
        '''
        data_dict = {}

        data_dict['L5_AVG_TOUCHES'] = df.tail(5)['TOUCHES'].mean()
        data_dict['L10_AVG_TOUCHES'] = df.tail(10)['TOUCHES'].mean()
        data_dict['DIFF_AVG_TOUCHES'] = (data_dict['L5_AVG_TOUCHES'] -
                                         data_dict['L10_AVG_TOUCHES'])

        data_dict['L5_MED_TOUCHES'] = df.tail(5)['TOUCHES'].median()
        data_dict['L10_MED_TOUCHES'] = df.tail(10)['TOUCHES'].median()
        data_dict['DIFF_MED_TOUCHES'] = (data_dict['L5_MED_TOUCHES'] -
                                         data_dict['L10_MED_TOUCHES'])

        data_dict['L5_AVG_FANTPTS'] = df.tail(5)['FANT_PTS'].mean()
        data_dict['L10_AVG_FANTPTS'] = df.tail(10)['FANT_PTS'].mean()
        data_dict['DIFF_AVG_FANTPTS'] = (data_dict['L5_AVG_FANTPTS'] -
                                         data_dict['L10_AVG_FANTPTS'])

        data_dict['L5_MED_FANTPTS'] = df.tail(5)['FANT_PTS'].median()
        data_dict['L10_MED_FANTPTS'] = df.tail(10)['FANT_PTS'].median()
        data_dict['DIFF_MED_FANTPTS'] = (data_dict['L5_AVG_FANTPTS'] -
                                         data_dict['L10_AVG_FANTPTS'])

        data_dict['SPECIAL_SAUCE_V1'] = ((data_dict['L5_AVG_FANTPTS'] *
                                         SS1_REC_GAMES_BIAS) +
                                         (data_dict['L10_AVG_FANTPTS'] *
                                         (1 - SS1_REC_GAMES_BIAS)))
        data_dict['SPECIAL_SAUCE_V2'] = ((data_dict['L5_MED_FANTPTS'] *
                                         SS2_REC_GAMES_BIAS) +
                                         (data_dict['L10_MED_FANTPTS'] *
                                         (1 - SS2_REC_GAMES_BIAS)))

        player_dict = {}
        player_dict[name] = data_dict

        df = pd.DataFrame.from_dict(player_dict, orient='index')

        return df

    def full_fantasy_standings(self, position: str = None, year: int = YEAR):
        """ Returns pandas df of complete fantasy standings table """
        return scrape.Scrape.get_fantasy_standings(position, year)

    def rb_rankings(self):
        """ Adds features and returns rb rankings """
        rbs = [x for x in self.players_info_dict if
               (self.players_info_dict[x]['POSITION'] == 'RB')]

        rbs_dfs = []
        bad_names = []

        total = len(rbs)
        i = 0
        for rb in rbs:
            try:
                df = self.FantStats.player_fantasy_log(rb)
                df = self._add_features(rb, df)
                rbs_dfs.append(df)
                time.sleep(2)
            except Exception as e:
                bad_names.append(rb)
                print(f'Could not calculate required stats to rank {rb}.')
                print(e)

            i += 1
            print(f'{round(((i/total)*100), 2)}% complete!')

        rbs_df = pd.concat(rbs_dfs)

        return rbs_df, bad_names

    def wr_rankings(self):
        """ Adds features and returns wr rankings """
        pass

    def qb_rankings(self):
        """ Adds features and returns qb rankings """
        pass

    def te_rankings(self):
        """ Adds features and returns te rankings """
        pass


Rankings = Rankings()
# print(Rankings.full_fantasy_standings('QB'))
rankings, bad = Rankings.rb_rankings()
rankings.to_csv('test.csv')
print(bad)
