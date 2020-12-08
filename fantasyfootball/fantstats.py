from .scraper import scrape

'''
TODO:
- expose some of the static methods we'd want to use from scraper
- create rankings
'''

YEAR = 2020
PTS_DICT = {'PASSING_YDS': 0.04, 'PASSING_TD': 4,
            'INT': -2, 'RECEIVING_YDS': 0.1, 'RECEIVING_TD': 6,
            'RUSHING_YDS': 0.1, 'RUSHING_TD': 6, 'FUM_LOST': -2}


class FantasyStats:
    def __init__(self, year=YEAR):
        self.players_info_dict = scrape.Scrape.get_player_info(year)

    def _caclulate_fantpts(self, df):
        df['FANT_PTS'] = ((df['RECEIVING_YDS'] * PTS_DICT['RECEIVING_YDS']) +
                          (df['RECEIVING_TD'] * PTS_DICT['RECEIVING_TD']) +
                          (df['RUSHING_YDS'] * PTS_DICT['RUSHING_YDS']) +
                          (df['RUSHING_TD'] * PTS_DICT['RUSHING_TD']) +
                          (df['FUMBLES_FL'] * PTS_DICT['FUM_LOST']))
        return df

    def _caclulate_qb_fantpts(self, df):
        return df

    def _calculate_touches(self, df):
        df['TOUCHES'] = df['RUSHING_ATT'] + df['RECEIVING_REC']
        return df

    def player_fantasy_log(self, player: str):
        ''' Return a pandas df of player's fantasy gamelog '''
        player = player.strip().upper()
        position = self.players_info_dict[player]['POSITION']

        if position not in ['QB', 'RB', 'WR', 'TE']:
            raise KeyError(f'No valid position for {player}')

        df = scrape.Scrape.get_player_gamelog(player, self.players_info_dict)

        if position != 'QB':
            df = self._caclulate_fantpts(df)
            df = self._calculate_touches(df)
        else:
            df = self._caclulate_qb_fantpts(df)

        return df

    def player_fantasy_summary(self, player: str):
        ''' Return a pandas df of player's condensed fantasy gamelog '''
        summary_cols = ['DATE', 'WEEK', 'FANT_PTS', 'TOUCHES']

        df = self.player_fantasy_log(player)

        return df[summary_cols]


# Fantasy = Fantasy()
# # print(Fantasy.player_fantasy_log('DAVANTE ADAMS'))
# print(Fantasy.player_fantasy_summary('DAVANTE ADAMS'))
