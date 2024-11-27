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



LD = App.feLoadDefinition
LoadMesh = App.feLoadMesh
LoadSet = App.feLoadSet


LoadSet.Get(1)
LoadMesh.type = constants.FLT_EPRESSURE
LoadMesh.SetID = LoadSet.ID


AllElemSet = App.feSet
AllElemSet.AddAll(constants.FT_ELEM)




elem = App.feElem

group = App.feGroup
group_draft = App.feGroup





#LoadMesh.Get(LoadMesh.Last())
#a = LoadMesh.GetAllArray()
#LoadMesh.PutArray(3, True, True, False, (7,8,9), ([1,0,0], [1,0,0], [1,0,0], ), [123,0,0,0,0, 898,0,0,0,0, 637,0,0,0,0], 0 )

#print(a)




elem.Get(elem.FirstInSet(AllElemSet.ID))


'''while AllElemSet.Next():
    
    elem.Get(AllElemSet.CurrentID)
    centroid = elem.GetCentroid()
    print(elem.ID, centroid)'''

array = elem.GetCentroidArray(AllElemSet.ID)
print(array)



App.feViewRegenerate(0)


