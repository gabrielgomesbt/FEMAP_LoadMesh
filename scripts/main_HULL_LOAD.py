import GetData_pressure
import GetData_acceleration
import Put_Acceleration
import json_handler
import pandas as pd

# Caminhos dos arquivos de input
pressure_file_path = "json\Pressure_Data_(6).json"
acceleration_file_path = "json\Acceleration_Data.json"


# Aplicação de pressões e geração do LoadSet dataframe
pressure_data = json_handler.get_json_data(pressure_file_path)
pressure_data = pressure_data['case test']['Ship Responses']
loadset_df = GetData_pressure.data_to_pressure(pressure_data)


# Geração do dataframe de pressões
acceleration_data = json_handler.get_json_data(acceleration_file_path)
data = acceleration_data['case test']['Ship Responses']
rotation_center = acceleration_data['case test']['CoG [m]']

df = GetData_acceleration.data_to_acceleration_df(data, rotation_center)


# Cruzamento de dataframes e geração de dataframe com aceleração e loadsets
merged_df = pd.merge(loadset_df, df, on=['Period', 'Direction'], how='left')
print(merged_df)

# Aplicação de acelerações no modelo
Put_Acceleration.put_acceleration_df(merged_df, rotation_center)