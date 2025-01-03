'''
Last Update: 03/01/2024

@author: Gabriel Gomes Benites Teixeira

DESCRIPTION: This code is used to apply hydrostatic load in tanks previously mapped. It uses the tanks CSVs and
an input of draft.  

'''

'_______________________________________ Imports _____________________________________'

import API_FEMAP
from API_FEMAP import App, constants
import pandas as pd
import DFLoadMesh

'_______________________________________ Back End _____________________________________'

def tank_hydro_df(tank_name, draft, rho=1000/10**9, g=9807):

    csv_path = 'CSV'
    df = pd.read_csv(f'{csv_path}//{tank_name}.csv')

    if 'Centroid Z' in df.columns:
        centroid_col = 'Centroid Z'
    elif 'Centroid Y' in df.columns:
        centroid_col = 'Centroid Y'
    else:
        raise Exception("The dataframe don't have any centroid column.")
    

    df = df[df[centroid_col] < draft]
    df['Liquid Column'] = draft - df[centroid_col]
    df['Pressure'] = df['Liquid Column'] * rho * g * (-1)


    tank_load = DFLoadMesh.DFLoadMesh(df, name=f'{tank_name}_(draft:{draft/1000}m)')
    tank_load.put_load_df()
    return df



if __name__ == '__main__':

    tank_hydro_df('TK_1_C', 10000)
    tank_hydro_df('TK_1_PS', 8000)
    tank_hydro_df('TK_1_SB', 12000)
    tank_hydro_df('TK_2_C', 8000)
    tank_hydro_df('TK_2_PS', 9500)
    tank_hydro_df('TK_2_SB', 10000)
    tank_hydro_df('TK_3_C', 10000)
    tank_hydro_df('TK_3_PS', 10000)
    tank_hydro_df('TK_3_SB', 10000)
