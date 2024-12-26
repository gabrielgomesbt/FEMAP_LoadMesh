import scripts.API_FEMAP
from scripts.API_FEMAP import App, constants
import numpy as np
import pandas as pd


elem = App.feElem
elem_set = App.feSet

LoadDef = App.feLoadDefinition
LoadMesh = App.feLoadMesh
LoadSet = App.feLoadSet

class LoadMesh:

    def __init__(self, draft, hull_elem_set, rho=1000/10**9, g=9807)
        self.draft = draft
        self.hull_elem_set = hull_elem_set
        self.rho_g = rho * g



    def hydro_pressure(self):
        group_draft = App.feGroup
        group_draft.Get(group_draft.Last())
        group_draft.clear()
        group_draft.title = f"Draft ({self.draft/1000} m)"


        elem.Get(elem.FirstInSet(elem_set.ID))
        elem_array = elem.GetCentroidArray(elem_set.ID)

        Num_elem = elem_array[1]
        elem_id_array = elem_array[2]
        elem_centroid_array = elem_array[3]
        elem_centroid_array = np.array(elem_array[3]).reshape(-1,3)
        elem_centroid_z_array = elem_centroid_array[:,2]

        df = pd.DataFrame()
        df['Elem IDs'] = elem_id_array
        df['Z_Centroid'] = elem_centroid_z_array

        df = df[df['Z_Centroid'] < self.draft]
        df['Liquid Column'] = self.draft - df['Z_Centroid']
        df['Pressure'] =  -1 * self.rho_g * df['Liquid Column']


        wet_elem_set = App.feSet
        elem_id_array = df['Elem IDs'].to_numpy()
        wet_elem_set.AddArray(len(elem_id_array), elem_id_array)
        group_draft.SetAdd(constants.FT_ELEM, wet_elem_set.ID)
        group_draft.Put(group_draft.NextEmptyID())


        Num_elem = df.shape[0]
        elem_id_array = df['Elem IDs'].to_numpy()
        face_id_array = np.tile([1,0,0], Num_elem)
        pressure_array = df['Pressure'].to_numpy()

        ## Formatando para que o vetor de pressão de cada elemento seja do tipo (pressão,0,0,0,0)
        pressure_array_formated = np.empty(len(pressure_array) * 5, dtype=float)  
        pressure_array_formated[::5] = pressure_array  
        pressure_array_formated[1::5] = 0       
        pressure_array_formated[2::5] = 0
        pressure_array_formated[3::5] = 0
        pressure_array_formated[4::5] = 0


        LoadSet.Get(1)
        LoadSet.title = f"Hydrostatic Pressure (Draft = {self.draft/1000} m)"
        LoadSet.Put(LoadSet.NextEmptyID())
        LoadMesh.Get(1)
        LoadMesh.type = constants.FLT_EPRESSURE
        LoadMesh.SetID = LoadSet.ID

        LoadMesh.PutArray(Num_elem, True, True, False, elem_id_array, face_id_array, pressure_array_formated, 0)
    

        print('Finalizado!')
        App.feViewRegenerate(0)




    def tank_mapping(self):
        pass


    def put_load_csv(self, csv_path):
        df = pd.read_csv(csv_path)

        
    










if __name__ == "__main__":

    group = App.feGroup
    group.Get(1)
    elemSet = group.List(constants.FT_ELEM)

    Load = LoadMesh(20000, elemSet)

    Load.hydro_pressure()