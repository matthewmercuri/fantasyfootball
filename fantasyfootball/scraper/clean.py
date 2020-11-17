import pandas as pd


class Cleaner:

    @staticmethod
    def clean_fantasy_standings(df):
        cols = df.columns

        new_cols = []
        for col in cols:
            upper_col, lower_col = col
            if upper_col[:2] == 'Un':
                new_cols.append(lower_col.strip().upper())
            else:
                new_col = f'{upper_col}_{lower_col}'.strip().upper()
                new_cols.append(new_col)

        df.columns = new_cols

        df.drop(df.loc[df['AGE'] == 'Age'].index, inplace=True)
        df.drop('RK', axis=1, inplace=True)

        df['PLAYER'] = df['PLAYER'].astype(str)
        df['FANTPOS'] = df['FANTPOS'].astype(str)
        df['TM'] = df['TM'].astype(str)

        df['PLAYER'] = df['PLAYER'].apply(lambda x: x.strip().upper())
        df['FANTPOS'] = df['FANTPOS'].apply(lambda x: x.strip().upper())
        df['TM'] = df['TM'].apply(lambda x: x.strip().upper())

        df[df.columns[4:]] = df[df.columns[4:]].apply(pd.to_numeric)

        df.fillna(0, inplace=True)
        df.sort_values(by='FANTASY_FANTPT', ascending=False, inplace=True)
        df.reset_index(inplace=True, drop=True)

        return df

    @staticmethod
    def clean_rb_gamelog(df):
        '''
        tgt	Rec	Yds	Y/R	TD	Ctch%	Y/Tgt
        '''
        NEEDED_COLS = ['RUSHING_ATT', 'RUSHING_YDS', 'RUSHING_Y/A',
                       'RUSHING_TD', 'RECEIVING_TGT', 'RECEIVING_REC',
                       'RECEIVING_YDS', 'RECEIVING_Y/R', 'RECEIVING_TD',
                       'RECEIVING_CTCH%', 'RECEIVING_Y/TGT', 'FUMBLES_FL']

        cols = df.columns

        new_cols = []
        for col in cols:
            upper_col, lower_col = col
            if upper_col[:2] == 'Un':
                new_cols.append(lower_col.strip().upper())
            else:
                new_col = f'{upper_col}_{lower_col}'.strip().upper()
                new_cols.append(new_col)

        df.columns = new_cols
        df.rename(columns={'UNNAMED: 7_LEVEL_1': 'LOCATION'}, inplace=True)
        df.drop(df.loc[df['AGE'] == 'Age'].index, inplace=True)
        df.drop(df.tail(1).index, inplace=True)
        df.drop('RK', axis=1, inplace=True)

        nan_values = {'LOCATION': 'H', 'GS': 'NO'}
        df.fillna(value=nan_values, inplace=True)
        df.fillna(0, inplace=True)

        df[df.columns[9:]] = df[df.columns[9:]].astype(str)
        df[df.columns[10:]] = df[df.columns[10:]].apply(pd.to_numeric,
                                                        errors='ignore')

        df['G#'] = df['G#'].astype(int)
        df['WEEK'] = df['WEEK'].astype(int)
        df['AGE'] = df['AGE'].astype(float)

        cleaned_cols = df.columns
        for needed_col in NEEDED_COLS:
            if needed_col not in cleaned_cols:
                df[needed_col] = 0

        df.reset_index(inplace=True, drop=True)

        return df
