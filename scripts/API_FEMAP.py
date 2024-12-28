import pythoncom
import PyFemap
from PyFemap import constants
import sys
import datetime
from datetime import datetime


'''Connect to FEMAP API'''
try:
    existObj = pythoncom.connect(PyFemap.model.CLSID)
    App = PyFemap.model(existObj)
    App.feAppMessage(0,f"Python Connected to Femap {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
except:
    sys.exit('Femap not open')