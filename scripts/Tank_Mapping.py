import API_FEMAP
from API_FEMAP import App, constants
import pandas as pd


tank_elem_set = App.feSet
tank_elem_group = App.feGroup
elem = App.feElem


tank_elem_group.Get(1)
tank_elem_set = tank_elem_group.List(constants.FT_ELEM)

elem.Get(elem.FirstInSet(tank_elem_set.ID))
#elem_array = elem.GetMultiFaceInfoArray()


data  = {"Element ID": [],
         "Centroid Z": [],
         "Normal Factor": []
         }


while tank_elem_set.Next():

    elem.Get(tank_elem_set.CurrentID)
    elem_id = elem.ID
    elem_centroid = elem.GetCentroid()
    centroid_z = elem.GetCentroid()[1][2]
    normal_vec = elem.GetFaceNormal(1)
    if normal_vec[1][0] < 0:
        normal_factor = -1
    else:
        normal_factor = 1


    data["Element ID"].append(elem_id)
    data["Centroid Z"].append(centroid_z)
    data["Normal Factor"].append(normal_factor)


df = pd.DataFrame(data)

csv_path = "CSV//Teste.csv"
df.to_csv(csv_path)

print(df)





#print(elem_array)


#tank_elem_set.Select(constants.FT_ELEM, True, "Select Tank Elements")
