Sub Hull_Draft_Load_FPI()

    Dim inicio As Double
    Dim fim As Double
    

    inicio = Timer



    Dim App As femap.model
    Set App = GetObject(, "femap.model")
    
    
    Dim hull_set As femap.Set
    Set hull_set = App.feSet
    
    Dim draft_set As femap.Set
    Set draft_set = App.feSet
    
    Dim Elem As femap.Elem
    Set Elem = App.feElem
    
    Dim gr As femap.Group
    Set gr = App.feGroup
    
    Dim top_coord As Double
    Dim bot_coord As Double
    
    Dim s_bot As femap.Set
    Set s_bot = App.feSet
    
    Dim e_bot As femap.Elem
    Set e_bot = App.feElem

    
    Dim row As Long
    Dim GroupIDCol As Long
    
    Dim elemID As Long
    Dim grID As Long
    Dim draft As Long
    Dim Density As Double
    Dim coord As Variant
    Dim tolerance As Long
    
    
    
    If s_bot.Select(FT_ELEM, True, "Choose Tank Bottom Element") = FE_OK Then
        While e_bot.NextInSet(s_bot.ID) = FE_OK
            rc = e_bot.GetFaceCentroid(1, coord)
            bot_coord = coord(2)
            rc = App.feAppMessage(FCM_NORMAL, "Top bottom at corrdinate Y : " & bot_coord)
        Wend
    End If
    
    
    
    row = 2
    GroupIDCol = 2
    draft = 3
    Density = 1025 '[kg/m³]
    tolerance = -1 'Tolerancia para a coordenada de baixo
    
    
    
    'If bot_coord(2) < 0 Then
    '    tolerance = -1 * tolerance
    'End If
    

    
    
    'Variáveis de cálculo de norma
    Dim h_s As Long
    Dim Bheta_EPS As Long
    Dim Bheta_EPP As Long
    Dim k_u As Long
    Dim h_de As Long
    
    
    
    h_s = bot_coord + draft
    
    
    
    
    grID = Cells(2, 2)
    gr.Get (grID)
    
    Set hull_set = gr.list(FGR_ELEM)
    
    Dim grTest As femap.Group
    Set grTest = App.feGroup
    
    elemID = hull_set.First
    
    While elemID <> 0
        Elem.Get (elemID)
        
        If Elem.type = FET_L_PLATE Then
            rc = Elem.GetFaceCentroid(1, coord)
            
            If coord(2) <= h_s Then
                draft_set.Add (Elem.ID)
                rc = grTest.Add(FT_ELEM, elemID)
                
            End If
        End If
        elemID = hull_set.Next
    Wend
    
    grTest.Put (grTest.NextEmptyID)
    
    
    
    '======================================
    
    Dim pressure As Double
    Dim v As Variant
    Dim coord1 As Variant
    
    
    Dim LoadSet As femap.LoadSet
    Set LoadSet = App.feLoadSet
    
    Dim LoadMesh As femap.LoadMesh
    Set LoadMesh = App.feLoadMesh
    
    LoadSet.Title = "Draft Hydrostatic Pressure"
    LoadSet.Put (LoadSet.NextEmptyID)
    
    
    
    
    elemID = draft_set.First
    
    While elemID <> 0
    
        Elem.Get (elemID)
        rc = Elem.GetFaceCentroid(1, coord1)
        
        pressure = (Density / (1000000000)) * (9807) * (draft - coord1(2))
        
    
        LoadMesh.setID = LoadSet.ID
        LoadMesh.meshID = Elem.ID
        LoadMesh.type = FLT_EPRESSURE
        LoadMesh.FaceNumber = 1
        
        LoadMesh.pressure = pressure
        
        LoadMesh.Put (LoadMesh.NextEmptyID())
        
        elemID = draft_set.Next
        
    Wend
    
    fim = Timer
 
    Debug.Print fim - inicio
    
End Sub