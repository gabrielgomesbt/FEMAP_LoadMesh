'''



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



def get_lower_coord(elemSet):

    elem.Get(elem.FirstInSet(elemSet.ID))

    while elemSet.Next():
        elem.Get(elemSet.CurrentID)
        centroid = elem.GetCentroid()
        print(elem.D, centroid)




def rotated_z(CG: tuple, trim, heel):
    pass




def hydro_pressure(draft, elemSet, rho=1000/10**9, g=9807):
    group_draft.Get(group_draft.Last())
    group_draft.clear()
    group_draft.title = f"Draft ({draft/1000} m)"


    rho_g = rho * g
    

    elem_id_tuple = elemSet.GetArray()
    underwater_centroids = []

    for elem_id in elem_id_tuple[2]:

        elem.Get(elem_id)
        centroid_z = elem.GetCentroid()[1][2]
        if centroid_z < draft:
            #pressure = rho_g * (draft - centroid_z)
            liquid_column = draft - centroid_z
            underwater_centroids.append((elem_id, liquid_column))
            group_draft.Add(constants.FT_ELEM, elem_id)



    df = pd.DataFrame(underwater_centroids)
    df['Pressure'] = rho_g * df[1] 
    print(df)
    print('Aplicando carregamento...')

    
    LoadSet.Get(1)
    LoadSet.title = f"Hydrostatic Pressure (Draft = {draft/1000} m)"
    LoadSet.Put(LoadSet.NextEmptyID())
    LoadMesh.Get(1)


    for _, row in df.iterrows():

        elemID = int(row[0])
        pressure = row['Pressure']
        #print("ID: ", elemID, "Pressure: ", pressure)

        LoadMesh.type = constants.FLT_EPRESSURE
        LoadMesh.SetID = LoadSet.ID
        LoadMesh.meshID = elemID
        LoadMesh.FaceNumber = 1
        LoadMesh.Pressure = -1 * pressure

        LoadMesh.Put(LoadMesh.NextEmptyID())
        a = LoadMesh.GetAllArray()

 

    #print(underwater_centroids)
    print('Finalizado!')
    group_draft.Put(group_draft.NextEmptyID())
    App.feViewRegenerate(0)




if __name__ == "__main__":


    group.Get(1)
    elemSet = group.List(constants.FT_ELEM)


    hydro_pressure(1500,elemSet)

