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


LoadSet.Get(1)
LoadMesh.type = constants.FLT_EPRESSURE
LoadMesh.SetID = LoadSet.ID


AllElemSet = App.feSet
AllElemSet.AddAll(constants.FT_ELEM)

elem = App.feElem

group = App.feGroup
group_draft = App.feGroup



#LoadMesh.LoadDefinitionID = 1


LoadDef.Get(LoadDef.Last())
LoadDef.loadType = constants.FLT_EPRESSURE
LoadDef.DataType = constants.FT_SURF_LOAD

LoadDef.PutAll(LoadDef.NextEmptyID(), constants.FT_SURF_LOAD, constants.FT_ELEM, "")

LoadMesh.LoadDefinitionID = 1



App.feViewRegenerate(0)


