import pythoncom
import PyFemap
from PyFemap import constants
import sys
import os
import json

'''Connect to FEMAP'''
try:
    existObj = pythoncom.connect(PyFemap.model.CLSID)
    App = PyFemap.model(existObj)
    App.feAppMessage(0,"Python Connected to Femap")
except:
    sys.exit('Femap not open')


elem = App.feElem



Element_Centroids = {}
c=1
while elem.Get(c) == -1:
    centroid = elem.GetCentroid()
    print(elem.ID, centroid[1])
    Element_Centroids['element_' + str(elem.ID)] = centroid[1]
    c+=1



destination_path = r"C:\Users\gabriel.teixeira_pro\VSCode\2215\PME2215\database\nosql"
destination_path = os.path.join(destination_path, 'Elem_Centroids-Medium.json')

    
with open(destination_path, 'w') as file:
    json.dump(Element_Centroids, file, indent=4)