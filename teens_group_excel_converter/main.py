import os
import pandas as pd
from datetime import datetime
import easygui

path = ''
while True:
    path = easygui.fileopenbox()
    if path[-3:] == 'csv':
        break
    easygui.msgbox('Invalid (.csv) file!')


try:
    filename = os.path.basename(path)
    workdir = os.path.dirname(path)

    df_original = pd.read_csv(path)
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

    save_path = f'{workdir}/{datetime.now().strftime('%Y%m%d%H%M')
                             }_{filename}'
    df.to_csv(save_path)
    easygui.msgbox(f'Success! File is saved at {save_path}')
except Exception as err:
    easygui.msgbox(f'Error: {err}')
