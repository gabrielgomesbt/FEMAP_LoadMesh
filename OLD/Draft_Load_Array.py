'''
DESCRIÇÃO: Gera carregamento hidrostático de maneira muito mais eficiente e rápida através de abordagem de arrays e dataframes

ÚLTIMA ATUALIZAÇÃO: 28/11/2024

AUTOR: Gabriel Gomes Benites Teixeira

'''

import pythoncom
import PyFemap
from PyFemap import constants
import sys
import numpy as np
import pandas as pd


'''Connect to FEMAP API'''
try:
    existObj = pythoncom.connect(PyFemap.model.CLSID)
    App = PyFemap.model(existObj)
    #App.feAppMessage(0,"Python Connected to Femap")
except:
    sys.exit('Femap not open')



LoadDef = App.feLoadDefinition
LoadMesh = App.feLoadMesh
LoadSet = App.feLoadSet


AllElemSet = App.feSet
AllElemSet.AddAll(constants.FT_ELEM)


elemSet = App.feSet


elem = App.feElem

group = App.feGroup
group_draft = App.feGroup




def hydro_pressure(draft, elemSet, rho=1000/10**9, g=9807):
    group_draft.Get(group_draft.Last())
    group_draft.clear()
    group_draft.title = f"Draft ({draft/1000} m)"


    rho_g = rho * g

    elem.Get(elem.FirstInSet(elemSet.ID))
    elem_array = elem.GetCentroidArray(elemSet.ID)

    Num_elem = elem_array[1]
    elem_id_array = elem_array[2]
    elem_centroid_array = elem_array[3]
    elem_centroid_array = np.array(elem_array[3]).reshape(-1,3)
    elem_centroid_z_array = elem_centroid_array[:,2]


    df = pd.DataFrame()
    df['Elem IDs'] = elem_id_array
    df['Z_Centroid'] = elem_centroid_z_array
    #print(df)

    df = df[df['Z_Centroid'] < draft]
    df['Liquid Column'] = draft - df['Z_Centroid']
    df['Pressure'] =  -1 * rho_g * df['Liquid Column']



    # Grupo contendo os elementos abaixo do calado
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

    #print(pressure_array_formated)



    LoadSet.Get(1)
    LoadSet.title = f"Hydrostatic Pressure (Draft = {draft/1000} m)"
    LoadSet.Put(LoadSet.NextEmptyID())
    LoadMesh.Get(1)
    LoadMesh.type = constants.FLT_EPRESSURE
    LoadMesh.SetID = LoadSet.ID

#LoadMesh.PutArray(3, True, True, False, (7,8,9), ([1,0,0], [1,0,0], [1,0,0], ), [123,0,0,0,0, 898,0,0,0,0, 637,0,0,0,0], 0 ) ## Referência
    LoadMesh.PutArray(Num_elem, True, True, False, elem_id_array, face_id_array, pressure_array_formated, 0)
    

    print('Finalizado!')
    App.feViewRegenerate(0)



def load_mesh_put_df(elemSet):
    pass



if __name__ == "__main__":


    group.Get(1)
    elemSet = group.List(constants.FT_ELEM)

    i=1000
    while i <= 24000:
        hydro_pressure(i, elemSet)
        i += 1000

    #hydro_pressure(20000, elemSet)


    App.feViewRegenerate(0)