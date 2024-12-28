import API_FEMAP
from API_FEMAP import App, constants
import pandas as pd
import numpy as np


## Variáveis FEMAP ## 
LoadMesh = App.feLoadMesh
LoadSet = App.feLoadSet

elem = App.feElem


class DFLoadMesh:
    def __init__(self, load_df, name='Pressure', period='', direction=''):
        self.load_df = load_df
        self.name = name
        self.period = period
        self.direction = direction
        self.loadset_id = None


    def put_load_df(self):
        
        num_elem = self.load_df.shape[0]
        elem_id_array = self.load_df['Element ID'].to_numpy()
        face_id_array = np.tile([1,0,0], num_elem)

        # Tratamento para o caso de anteparas de vante em tanque
        try:
            self.load_df['Pressure'] = self.load_df['Pressure'] * self.load_df['Normal Factor']
        except:
            pass
        pressure_array = self.load_df['Pressure'].to_numpy()

        ## Formatando para que o vetor de pressão de cada elemento seja do tipo (pressão,0,0,0,0)
        pressure_array_formated = np.empty(len(pressure_array) * 5, dtype=float)  
        pressure_array_formated[::5] = pressure_array  
        pressure_array_formated[1::5] = 0       
        pressure_array_formated[2::5] = 0
        pressure_array_formated[3::5] = 0
        pressure_array_formated[4::5] = 0

        LoadSet.Get(1)

        if self.period == '' and self.direction == '':
            LoadSet.title = self.name
        else:
            LoadSet.title = f"{self.name}_Period_{self.period}_Direction_{self.direction}"
        LoadSet.Put(LoadSet.NextEmptyID())
        LoadMesh.Get(1)
        LoadMesh.type = constants.FLT_EPRESSURE
        LoadMesh.SetID = LoadSet.ID
        self.loadset_id = LoadSet.ID

        #LoadMesh.PutArray(3, True, True, False, (7,8,9), ([1,0,0], [1,0,0], [1,0,0], ), [123,0,0,0,0, 898,0,0,0,0, 637,0,0,0,0], 0 ) ## Referência
        LoadMesh.PutArray(num_elem, True, True, False, elem_id_array, face_id_array, pressure_array_formated, 0)




if __name__ == "__main__":

    data = {
        'Element ID': [1,2,3,4,5],
        'Pressure': [100, 200, 300, 400, 500],
        'Normal Factor': [1,1,1,1,1]
    }


    data_df = pd.DataFrame(data)


    pressure1 = DFLoadMesh(data_df, "Hydrodynamic_Load", "3.0 [s]", "0.0" )
    pressure1.put_load_df()
