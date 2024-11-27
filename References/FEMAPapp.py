import pythoncom
import PyFemap
from PyFemap import constants
import sys
import numpy as np
import math

'''Connect to FEMAP'''
try:
    existObj = pythoncom.connect(PyFemap.model.CLSID)
    App = PyFemap.model(existObj)
    App.feAppMessage(0,"Python Connected to Femap")
except:
    sys.exit('Femap not open')


## Inicilização de variáveis FEMAP ##1

# Sets
AllCurveSet = App.feSet
PlacedCurveSet = App.feSet
analysed_CurveSet = App.feSet

# Groups
alignedGr_X = App.feGroup
alignedGr_Y = App.feGroup
alignedGr_Z = App.feGroup
NotAlignedGr = App.feGroup

# Geometry
point = App.fePoint
point2 = App.fePoint
pEndA = App.fePoint
pEndB = App.fePoint
curve = App.feCurve
curve2 = App.feCurve



def IsParalel(vetorA, vetorB, tolerancia):
    
    # Calcula o produto escalar dos dois vetores
    produto_escalar = np.dot(vetorA, vetorB)
    
    # Calcula o módulo (norma) dos vetores
    moduloA = np.linalg.norm(vetorA)
    moduloB = np.linalg.norm(vetorB)

    if moduloA == 0 or moduloB == 0:
        return False 
    
    # Calcula o cosseno do ângulo entre os vetores
    cos_theta = produto_escalar / (moduloA * moduloB)
    
    # Verifica se o valor absoluto do cosseno está dentro da tolerância de 1
    return np.abs(np.abs(cos_theta) - 1) <= tolerancia


AllCurveSet.AddAll(constants.FT_CURVE)



# Vetor Unitários Globais
x_vec = np.array([1,0,0])
y_vec = np.array([0,1,0])
z_vec = np.array([0,0,1])


angleTolerance = App.feGetReal('Tolerance angle for alignment (degrees): ', 0, 44.9)
angleTolerance = angleTolerance[1]


''' >> OBS1.: 

Diferentemente do VBA em que a variável "angleTolerance" é passada como 
argumento da função "feGetReal", no python "angleTolerance" recebe uma tupla 
(-1, angleTolerance). Aparentemente o primeiro valor da tupla é sempre
o return code (FE_OK = -1, FE_FAIL = 0, etc.)
'''

tolerance = 1 - (math.cos(angleTolerance*(math.pi/180)))


curve.Get(curve.FirstInSet(AllCurveSet.ID))
rc = App.feAppMessage(constants.FCM_NORMAL, 'Grouping Curves...')


for i in range(len(AllCurveSet)):


    EndPoints_tuple = curve.EndPoints()
    EndA = EndPoints_tuple[1]
    EndB = EndPoints_tuple[2]

    ''' >> OBS2.:

    Aqui da mesma forma que indicado na OBS1, "EndPoints_tuple" recebe (-1, valor do End A,
    valor do End B).
    '''

    pEndA.Get(EndA)
    pEndB.Get(EndB)

    curve1_vec = np.array([0,0,0])
    curve1_vec[0] = pEndB.x - pEndA.x
    curve1_vec[1] = pEndB.y - pEndA.y
    curve1_vec[2] = pEndB.z - pEndA.z

    vecModule = np.linalg.norm(curve1_vec)

    if vecModule != 0:
        curve1_vec = curve1_vec/vecModule


    
    if IsParalel(curve1_vec, x_vec, tolerance):
        rc = alignedGr_X.Add(constants.FT_CURVE, curve.ID)

    elif IsParalel(curve1_vec, y_vec, tolerance):
        rc = alignedGr_Y.Add(constants.FT_CURVE, curve.ID)

    elif IsParalel(curve1_vec, z_vec, tolerance):
        rc = alignedGr_Z.Add(constants.FT_CURVE, curve.ID)

    else:
        rc = NotAlignedGr.Add(constants.FT_CURVE, curve.ID)
    
        

    rc = curve.Get(curve.NextInSet(AllCurveSet.ID))
    rc = curve.ID


alignedGr_X.title = 'Curvas em X'
alignedGr_X.Put (alignedGr_X.NextEmptyID())

alignedGr_Y.title = 'Curvas em Y'
alignedGr_Y.Put (alignedGr_Y.NextEmptyID())

alignedGr_Z.title = 'Curvas em Z'
alignedGr_Z.Put (alignedGr_Z.NextEmptyID())

NotAlignedGr.title = 'Curvas em outras direções'
NotAlignedGr.Put(NotAlignedGr.NextEmptyID())

rc = App.feAppMessage(constants.FCM_NORMAL, 'Finished')



