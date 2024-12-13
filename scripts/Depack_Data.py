import json_handler
import pandas as pd
import DFLoadMesh
from DFLoadMesh import DFLoadMesh



pressure_file_path = "json\Pressure_Data.json"
acceleration_file_path = "json\Acceleration_Data.json"

pressure_data = json_handler.get_json_data(pressure_file_path)
pressure_data = pressure_data['case test']['Ship Responses']



elem_id_list = []
pressure_list = []
for periods, directions in pressure_data.items():
    period = periods
    for direction, shipsides in directions.items():
        for shipside, shipside_list in shipsides.items():
            for item in shipside_list:

                elem_id = int(item['ID'])
                pressure = item['Mod []']
                elem_id_list.append(elem_id)
                pressure_list.append(pressure)

            df = pd.DataFrame()
            df['Elem IDs'] = elem_id_list
            df['Pressure'] = pressure_list

            load = DFLoadMesh(df,"Pressure", period, direction)
            load.put_load_df()

            elem_id_list = []
            pressure_list = []
