import GetData_pressure
import GetData_acceleration
import json_handler


pressure_file_path = "json\Pressure_Data.json"
acceleration_file_path = "json\Acceleration_Data.json"

pressure_data = json_handler.get_json_data(pressure_file_path)
pressure_data = pressure_data['case test']['Ship Responses']
loadset_df = GetData_pressure.data_to_pressure(pressure_data)

