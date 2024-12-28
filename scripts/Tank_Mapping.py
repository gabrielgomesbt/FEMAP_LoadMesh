import API_FEMAP
from API_FEMAP import App, constants
import pandas as pd
import numpy as np


tank_elem_set = App.feSet
tank_elem_set2 = App.feSet
tank_elem_group = App.feGroup
elem = App.feElem
internal_elem = App.feElem



class TankMapping:
    def __init__(self, tank_group_id, internal_element_id, csv_folder_path='CSV', tank_name=None):

        self.data  = {"Element ID": [],
                        "Centroid Z": [],
                        "Normal Factor": []
                }
        
        self.tank_group_id = tank_group_id
        self.internal_element_id = internal_element_id
        internal_elem.Get(internal_element_id)
        self.centroid_internal_element = np.array(internal_elem.GetCentroid()[1])
        self.centroid_internal_element[2] = self.centroid_internal_element[2] + 100    # Soma para evitar que o z do elemento escolhido seja coincidente com o tank top
        self.csv_folder_path = csv_folder_path

        


    def map(self):
        tank_elem_group.Get(self.tank_group_id)
        tank_elem_set = tank_elem_group.List(constants.FT_ELEM)

        elem.Get(elem.FirstInSet(tank_elem_set.ID))

        while tank_elem_set.Next():

            elem.Get(tank_elem_set.CurrentID)
            elem_id = elem.ID

            elem_centroid = np.array(elem.GetCentroid()[1])
            centroid_z = elem.GetCentroid()[1][2]
            normal_vec = elem.GetFaceNormal(1)
            normal_vec = np.array(normal_vec[1])
            
            scalar_product = np.dot(normal_vec, (self.centroid_internal_element - elem_centroid))

            if scalar_product < 0:
                normal_factor = -1
            else:
                normal_factor = 1


            self.data["Element ID"].append(elem_id)
            self.data["Centroid Z"].append(centroid_z)
            self.data["Normal Factor"].append(normal_factor)

        df = pd.DataFrame(self.data)
        self.data = df
        

        csv_path = f"{self.csv_folder_path}//{tank_elem_group.title}.csv"
        df.to_csv(csv_path)
        print(f'Tank {tank_elem_group.title} successfully mapped.')
        



    def get_tank_csv(self):
        df = pd.read_csv(self.csv_folder_path)
        return df





if __name__ == '__main__':

    '''Tank_Map = TankMapping(tank_group_id=2, internal_element_id=47298)
    Tank_Map.map(False)'''


    Tank_Map_1 = TankMapping( tank_group_id=1, internal_element_id=50310)
    Tank_Map_2 = TankMapping( tank_group_id=2, internal_element_id=46522)
    Tank_Map_3 = TankMapping( tank_group_id=3, internal_element_id=54290)
    Tank_Map_4 = TankMapping( tank_group_id=4, internal_element_id=25441)
    Tank_Map_5 = TankMapping( tank_group_id=5, internal_element_id=22)
    Tank_Map_6 = TankMapping( tank_group_id=6, internal_element_id=4308)
    Tank_Map_7 = TankMapping( tank_group_id=7, internal_element_id=40222)
    Tank_Map_8 = TankMapping( tank_group_id=8, internal_element_id=34652)
    Tank_Map_9 = TankMapping( tank_group_id=9, internal_element_id=35399)

    Tank_Map_1.map()
    Tank_Map_2.map()
    Tank_Map_3.map()
    Tank_Map_4.map()
    Tank_Map_5.map()
    Tank_Map_6.map()
    Tank_Map_7.map()
    Tank_Map_8.map()
    Tank_Map_9.map()