from datetime import datetime

import pandas as pd


def process_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    try:
        df_original = dataframe.copy()
        cols = list(df_original)
        cols = cols[24:31] + cols[:24] + cols[31:]
        df = df_original[cols]

        df.rename({
            'Address 1': 'Address',
            'Location': 'State',
            'First Name.1': 'Child First Name',
            'Last Name.1': 'Child Last Name',
            'Gender.1': 'Child Gender',
            'First Name': 'Membership First Name',
            'Last Name': 'Membership Last Name',
            'Gender': 'Membership Gender',
        }, axis=1, inplace=True)
        df['Address 3'] = df['Address 3'].astype(str)
        df[['Address', 'Address 2', 'Address 3']] = df[['Address',
                                                        'Address 2', 'Address 3']].fillna('').replace('nan', '')
        df['Address'] = df[['Address', 'Address 2', 'Address 3']].agg(
            ' '.join, axis=1).transform(str.strip)
        df = df.drop(['Address 2', 'Address 3'], axis=1)

        for i in ['Child First Name', 'Child Last Name', 'Child Gender', 'Date of Birth (DD/MM/YYYY)', 'Age', 'Did the child attend the BSV Dhamma School in 2024?']:
            df[i] = df[i].str.split(', ')
        df['Grade/Year Level at school at start of 2025'] = df.apply(lambda row: row['Grade/Year Level at school at start of 2025'].split(
            ', ') if len(row['Child First Name']) > 1 else [row['Grade/Year Level at school at start of 2025']], axis=1)
        df = df.explode(['Child First Name', 'Child Last Name', 'Child Gender', 'Date of Birth (DD/MM/YYYY)', 'Age',
                        'Grade/Year Level at school at start of 2025', 'Did the child attend the BSV Dhamma School in 2024?'])
        return df
    except Exception as err:
        raise err
