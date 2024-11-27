import pythoncom
import PyFemap
from PyFemap import constants
import sys


'''Connect to FEMAP API'''
try:
    existObj = pythoncom.connect(PyFemap.model.CLSID)
    App = PyFemap.model(existObj)
    #App.feAppMessage(0,"Python Connected to Femap")
except:
    sys.exit('Femap not open')


def run_analysis(run=True):
  
    if run == True:
        analysis = App.feAnalysisMgr
        analysis_study = App.feAnalysisStudy
        analysis.Get(1)
        analysis.Analyze(analysis.ID)

        analysis_study.Get(analysis_study.Last())
        analysis_last_ID = analysis_study.ID

        while True:
            analysis_study.Get(analysis_study.Last())

            if analysis_study.ID != analysis_last_ID:
                print('Análise concluída com sucesso!')
                break



def maximum_displacement(TAG, analyze=True):


    #TAG = "TKOD1-TB22-PL-002"

    # Declaração de variáveis do Femap
    rbo = App.feResults

    AllPropSet = App.feSet
    AllPropSet.AddAll(constants.FT_PROP)

    AllElemSet = App.feSet
    AllElemSet.AddAll(constants.FT_ELEM)

    TagElemSet = App.feSet
    TagNodeSet = App.feSet


    prop = App.feProp
    node = App.feNode
    elem = App.feElem



    prop.Get(prop.FirstInSet(AllPropSet.ID))

    while AllPropSet.Next():
        prop.Get(AllPropSet.CurrentID)
        if prop.title == TAG:
            TAG_prop = prop.title
            break
    # >> adicionar tratamento de erro <<

    TagElemSet.AddRule(prop.ID, constants.FGD_ELEM_BYPROP)



    elem.Get(elem.FirstInSet(TagElemSet.ID))

    while TagElemSet.Next():
        elem.Get(TagElemSet.CurrentID)
        TagNodeSet.AddRule(elem.ID, constants.FGD_NODE_ONELEM)



    run_analysis(analyze)
    analysis_study = App.feAnalysisStudy
    analysis_study.Get(analysis_study.Last())



    node.Get(node.FirstInSet(TagNodeSet.ID))

    total_displacement = []
    while TagNodeSet.Next():
        node.Get(TagNodeSet.CurrentID)
        node_displacement = rbo.EntityValueV2(analysis_study.ID, 1, node.ID)
        total_displacement.append((node.ID, node_displacement[1]))


    maior_id, maior_deslocamento = max(total_displacement, key=lambda x: x[1])

    # print(maior_id)
    # print(maior_deslocamento)


    return maior_deslocamento



if __name__ == "__main__":

    Tag = "TKOD1-TB22-PL-002"


    max_tag_displacement = maximum_displacement(Tag)


    print('')
    print(f"Descolamento máximo no TAG {Tag}: ", max_tag_displacement)
    print('')