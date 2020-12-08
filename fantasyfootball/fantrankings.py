import pandas as pd
import time

from .fantstats import FantasyStats
from .scraper import scrape

YEAR = 2020
SS1_REC_GAMES_BIAS = 0.5
SS2_REC_GAMES_BIAS = 0.75


class Rankings:
    def __init__(self):
        self.FantStats = FantasyStats(year=YEAR)
        self.players_info_dict = self.FantStats.players_info_dict

    def _add_features(self, name, df):
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
        data_dict['SS_MESHED'] = ((data_dict['L10_MED_FANTPTS'] * 0.66) +
                                  (data_dict['L5_AVG_FANTPTS'] * 0.33))

        player_dict = {}
        player_dict[name] = data_dict

        df = pd.DataFrame.from_dict(player_dict, orient='index')

        return df

    def _add_relative_features(self, df):
        average_lastfive_touches = df['L5_AVG_TOUCHES'].mean()
        df['EXCESS_L5_AVG_TOUCHES'] = (df['L5_AVG_TOUCHES'] -
                                       average_lastfive_touches)

        average_ss1 = df['SPECIAL_SAUCE_V1'].mean()
        df['EXCESS_SS1'] = df['SPECIAL_SAUCE_V1'] - average_ss1

        average_ss2 = df['SPECIAL_SAUCE_V2'].mean()
        df['EXCESS_SS2'] = df['SPECIAL_SAUCE_V2'] - average_ss2

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
        rbs_df = self._add_relative_features(rbs_df)

        rbs_df.sort_values(by='EXCESS_SS2', ascending=False, inplace=True)

        return rbs_df, bad_names

    def wr_rankings(self):
        """ Adds features and returns wr rankings """
        wrs = [x for x in self.players_info_dict if
               (self.players_info_dict[x]['POSITION'] == 'WR')]

        wrs_dfs = []
        bad_names = []

        total = len(wrs)
        i = 0
        for wr in wrs:
            try:
                df = self.FantStats.player_fantasy_log(wr)
                df = self._add_features(wr, df)
                wrs_dfs.append(df)
                time.sleep(2)
            except Exception as e:
                bad_names.append(wr)
                print(f'Could not calculate required stats to rank {wr}.')
                print(e)

            i += 1
            print(f'{round(((i/total)*100), 2)}% complete!')

        wrs_df = pd.concat(wrs_dfs)
        wrs_df = self._add_relative_features(wrs_df)

        wrs_df.sort_values(by='EXCESS_SS2', ascending=False, inplace=True)

        return wrs_df, bad_names

    def te_rankings(self):
        """ Adds features and returns te rankings """
        tes = [x for x in self.players_info_dict if
               (self.players_info_dict[x]['POSITION'] == 'TE')]

        tes_dfs = []
        bad_names = []

        total = len(tes)
        i = 0
        for te in tes:
            try:
                df = self.FantStats.player_fantasy_log(te)
                df = self._add_features(te, df)
                tes_dfs.append(df)
                time.sleep(2)
            except Exception as e:
                bad_names.append(te)
                print(f'Could not calculate required stats to rank {te}.')
                print(e)

            i += 1
            print(f'{round(((i/total)*100), 2)}% complete!')

        tes_df = pd.concat(tes_dfs)
        tes_df = self._add_relative_features(tes_df)

        tes_df.sort_values(by='EXCESS_SS2', ascending=False, inplace=True)

        return tes_df, bad_names

    def qb_rankings(self):
        """ Adds features and returns qb rankings """
        pass


# Rankings = Rankings()
# # print(Rankings.full_fantasy_standings('QB'))
# rankings, bad = Rankings.te_rankings()
# rankings.to_csv('test3.csv')
# print(bad)
