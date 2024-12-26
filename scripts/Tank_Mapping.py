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


    def _hydro_pressure(self, draft, rho=1000/10**9, g=9807):
        df = pd.DataFrame(self.data)

        df = df[df['Centroid Z'] < draft]
        df['Liquid Column'] = draft - df['Centroid Z']
        df['Hydrostatic Pressure'] = df['Liquid Column'] * rho * g 

        return df

        


    def map_central(self, hydro_pressure=True):
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

        print(len(self.data["Element ID"]))
        df = pd.DataFrame(self.data)
        self.data = df

        if hydro_pressure:
            df = self._hydro_pressure(draft=6000)
        

        csv_path = f"{self.csv_folder_path}//{tank_elem_group.title}.csv"
        df.to_csv(csv_path)
        


    def map_portside(self):
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

        csv_path = f"{self.csv_folder_path}//{tank_elem_group.title}.csv"
        df.to_csv(csv_path)


    def map_starboard(self):
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

        csv_path = f"{self.csv_folder_path}//{tank_elem_group.title}.csv"
        df.to_csv(csv_path)


    def map(self, shipside):
        if shipside == 'central':
            self.map_central()
        elif shipside == 'portside':
            self.map_portside()
        elif shipside =='starboard':
            self.map_starboard()
        else:
            print('Invalid shipside\n', 3*'.\n' 'Valid Entries: central, portside, starboard')


    def get_tank_csv(self):
        df = pd.read_csv(self.csv_folder_path)
        return df





if __name__ == '__main__':

    '''Tank_Map = TankMapping(tank_group_id=2, internal_element_id=47298)
    Tank_Map.map_central(False)'''


    Tank_Map_PS = TankMapping( tank_group_id=3, internal_element_id=54290)
    #Tank_Map_PS.map_portside()
    Tank_Map_PS.map('OI')