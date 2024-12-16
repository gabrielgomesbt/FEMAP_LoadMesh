import json_handler
import pandas as pd



def data_to_acceleration_df(data, rotation_center):
    df = pd.DataFrame(columns=['Period', 'Directiom', 'acc_TX', 'acc_TY', 'acc_TZ', \
                                    'acc_RX', 'acc_RY', 'acc_RZ'])

    for periods, directions in data.items():
        period = periods
        for direction, accelerations in directions.items():
            acc_TX = accelerations['Acc1']['Mod [m/s2]']
            acc_TY = accelerations['Acc2']['Mod [m/s2]']
            acc_TZ = accelerations['Acc3']['Mod [m/s2]']
            acc_RX = accelerations['Acc4']['Mod [rad/s2]']
            acc_RY = accelerations['Acc5']['Mod [rad/s2]']
            acc_RZ = accelerations['Acc6']['Mod [rad/s2]']

            # df = pd.DataFrame(columns=['Period', 'Directiom', 'acc_TX', 'acc_TY', 'acc_TZ', \
            #                         'acc_RX', 'acc_RY', 'acc_RZ'])
            
            df_line = [period, direction, acc_TX, acc_TY, acc_TZ, acc_RX, acc_RY, acc_RZ]
            new_line = pd.DataFrame([df_line], columns=df.columns)
            df = pd.concat([df, new_line], ignore_index=True)

    return df



if __name__ == '__main__':


    acceleration_file_path = "json\Acceleration_Data.json"

    acceleration_data = json_handler.get_json_data(acceleration_file_path)
    data = acceleration_data['case test']['Ship Responses']

    rotation_center = acceleration_data['case test']['CoG [m]']

    df = data_to_acceleration_df(data, rotation_center)
    print(df)