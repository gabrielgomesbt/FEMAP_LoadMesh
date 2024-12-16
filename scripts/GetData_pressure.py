import json_handler
import pandas as pd
import DFLoadMesh
from DFLoadMesh import DFLoadMesh


def data_to_pressure(data):
    elem_id_list = []
    pressure_list = []
    loadset_df = pd.DataFrame(columns=['Period', 'Direction', 'LoadSet ID'])
    c=0 # contador para garantir que o load seja criado para bombordo e boreste no mesmo LoadSet

    for periods, directions in data.items():
        period = periods
        for direction, shipsides in directions.items():
            for shipside, shipside_list in shipsides.items():
                for item in shipside_list:
                    
                    elem_id = int(item['ID'])
                    pressure = item['Mod []']
                    elem_id_list.append(elem_id)
                    pressure_list.append(pressure)
                c+=1
                if c == 2:
                    df = pd.DataFrame()
                    df['Elem IDs'] = elem_id_list
                    df['Pressure'] = pressure_list

                    load = DFLoadMesh(df,"Pressure", period, direction)
                    load.put_load_df()
                    loadset_id = load.loadset_id

                    elem_id_list = []
                    pressure_list = []
                    c=0

                    # Criação do dataframe de loadsets para vincular com acelerações
                    loadset_df_line = [period, direction, loadset_id]
                    new_line = pd.DataFrame([loadset_df_line], columns=loadset_df.columns)
                    loadset_df = pd.concat([loadset_df, new_line], ignore_index=True)
    return loadset_df


if __name__ == "__main__":

    pressure_file_path = "json\Pressure_Data.json"
    acceleration_file_path = "json\Acceleration_Data.json"

    pressure_data = json_handler.get_json_data(pressure_file_path)
    pressure_data = pressure_data['case test']['Ship Responses']


    df = data_to_pressure(pressure_data)
    print(df)