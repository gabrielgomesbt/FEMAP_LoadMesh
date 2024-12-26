import API_FEMAP
from API_FEMAP import App, constants


def put_acceleration_df(acceleration_dataframe, rotational_center):

    LoadSet = App.feLoadSet

    for index, row in acceleration_dataframe.iterrows():

        loadsetID = row['LoadSet ID']
        Acc_TX = row['acc_TX']
        Acc_TY = row['acc_TY']
        Acc_TZ = row['acc_TZ']
        Acc_RX = row['acc_RX']
        Acc_RY = row['acc_RY']
        Acc_RZ = row['acc_RZ']

        acceleration_vector = [Acc_TX, Acc_TY, Acc_TZ, Acc_RX, Acc_RY, Acc_RZ]


        LoadSet.Get(loadsetID)
        LoadSet.BodyAccelOn = True
        LoadSet.vBodyOrigin = rotational_center
        LoadSet.vBodyAccel = acceleration_vector
        LoadSet.Put(loadsetID)

    





