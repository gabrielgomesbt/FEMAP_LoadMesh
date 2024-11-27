Attribute VB_Name = "Align_Curves_Global2"
'ALIGN CURVES GLONAL
'
'Author: Gabriel Gomes Benites Teixeira
'
'Last Update: 26/07/2024 (dd/mm/aaaa)
'
'Objective: Group curves by alignment with the global axis. This macro create 4 groups

Sub Main()

	Dim App As femap.model
	Set App = GetObject(, "femap.model")
	
	Dim AllCurveSet As femap.Set
	Set AllCurveSet = App.feSet
	
	Dim PlacedCurveSet As femap.Set
	Set PlacedCurveSet = App.feSet
	
	Dim analysed_CurveSet As femap.Set
	
	Set analysed_CurveSet = App.feSet
	
	Dim alignedGr_X As femap.Group
	Set alignedGr_X = App.feGroup
	
	Dim alignedGr_Y As femap.Group
	Set alignedGr_Y = App.feGroup
	
	Dim alignedGr_Z As femap.Group
	Set alignedGr_Z = App.feGroup
	
	Dim NotAlignedGr As femap.Group
	Set NotAlignedGr = App.feGroup
	
	Dim curve As femap.curve
	Set curve = App.feCurve
	
	Dim curve2 As femap.curve
	Set curve2 = App.feCurve
	
	Dim point As femap.point
	Set point = App.fePoint
	
	Dim point2 As femap.point
	Set point2 = App.fePoint
	
	Dim pEndA As femap.point
	Set pEndA = App.fePoint
	
	Dim pEndB As femap.point
	Set pEndB = App.fePoint
	
	
	Dim EndA As Long
	Dim EndA2 As Long
	Dim EndB As Long
	Dim EndB2 As Long
	Dim NumCurves As Long
	Dim vecModule As Long
	Dim tolerance As Double
	Dim angleTolerance As Double
	
	Dim attcurves As Variant
	Dim x_vec(2) As Variant
	Dim y_vec(2) As Variant
	Dim z_vec(2) As Variant
	Dim curve1_Vec(2) As Variant
	Dim curve2_Vec(2) As Variant
	
	AllCurveSet.AddAll (FT_CURVE)
	
	alignedGr_X.Get (1)
	alignedGr_Y.Get (1)
	alignedGr_Z.Get (1)
	
	
	'Vetor unit rio x
	x_vec(0) = 1
	x_vec(1) = 0
	x_vec(2) = 0
	
	'Vetor unit rio y
	y_vec(0) = 0
	y_vec(1) = 1
	y_vec(2) = 0
	
	'Vetor unit rio z
	z_vec(0) = 0
	z_vec(1) = 0
	z_vec(2) = 1
	
	
	'tolerance = 0.7
	rc = App.feGetReal("Tolerance angle for alignment (degrees):", 0, 44.9, angleTolerance)
	tolerance = 1 - (Cos(angleTolerance * 3.14159265358979 / 180))
	Debug.Print tolerance
	rc = App.feAppMessage(FCM_NORMAL, "Grouping Curves...")
	
	curve.Get (curve.FirstInSet(AllCurveSet.ID))
	'curve.Get (1825)
	'Debug.Print curve.ID
	
	For j = 1 To AllCurveSet.Count
	    
	    
	    rc = curve.EndPoints(EndA, EndB)
	            
	    pEndA.Get (EndA)
	    pEndB.Get (EndB)
	            
	    curve1_Vec(0) = Abs(pEndB.x - pEndA.x)
	    curve1_Vec(1) = Abs(pEndB.y - pEndA.y)
	    curve1_Vec(2) = Abs(pEndB.Z - pEndA.Z)
	        
	    vecModule = Sqr((curve1_Vec(0) ^ 2) + (curve1_Vec(1) ^ 2) + (curve1_Vec(2) ^ 2))
	        
	        
	    'Normaliza  o do Vetor
	    If vecModule <> 0 Then
	        curve1_Vec(0) = Abs(pEndB.x - pEndA.x) / vecModule
	        curve1_Vec(1) = Abs(pEndB.y - pEndA.y) / vecModule
	        curve1_Vec(2) = Abs(pEndB.Z - pEndA.Z) / vecModule
	    End If
	        
	        
	    
	    If IsParalel(curve1_Vec, x_vec, tolerance) Then
	        rc = alignedGr_X.Add(FT_CURVE, curve.ID)
	            
	            
	    ElseIf IsParalel(curve1_Vec, y_vec, tolerance) Then
	        rc = alignedGr_Y.Add(FT_CURVE, curve.ID)
	           
	            
	    ElseIf IsParalel(curve1_Vec, z_vec, tolerance) Then
	        rc = alignedGr_Z.Add(FT_CURVE, curve.ID)
	            
	    Else
	        rc = NotAlignedGr.Add(FT_CURVE, curve.ID)
	        
	    End If
	    
	    curve.Get (curve.NextInSet(AllCurveSet.ID))
	    'Debug.Print curve.ID
	    
	Next j
	
	     
	alignedGr_X.Title = "Curvas em X"
	alignedGr_X.Put (alignedGr_X.NextEmptyID)
	
	alignedGr_Y.Title = "Curvas em Y"
	alignedGr_Y.Put (alignedGr_Y.NextEmptyID)
	
	alignedGr_Z.Title = "Curvas em Z"
	alignedGr_Z.Put (alignedGr_X.NextEmptyID)
	
	NotAlignedGr.Title = "Curvas em outras dire  es"
	NotAlignedGr.Put (NotAlignedGr.NextEmptyID)

	rc = App.feAppMessage(FCM_NORMAL, "Finished.")

End Sub

Function IsParalel(vetorA As Variant, vetorB As Variant, tolerancia As Double) As Boolean
    Dim produtoEscalar As Double
    Dim moduloA As Double
    Dim moduloB As Double
    Dim cosTheta As Double
    
    ' Calcula o produto escalar dos dois vetores
    produtoEscalar = vetorA(0) * vetorB(0) + vetorA(1) * vetorB(1) + vetorA(2) * vetorB(2)
    
    ' Calcula o m dulo dos vetores
    moduloA = Sqr(vetorA(0) ^ 2 + vetorA(1) ^ 2 + vetorA(2) ^ 2)
    moduloB = Sqr(vetorB(0) ^ 2 + vetorB(1) ^ 2 + vetorB(2) ^ 2)
    
    ' Calcula o cosseno do  ngulo entre os vetores
    cosTheta = produtoEscalar / (moduloA * moduloB)
    
    ' Verifica se o valor absoluto do cosseno est  dentro da toler ncia de 1
    IsParalel = Abs(Abs(cosTheta) - 1) <= tolerancia
End Function
    
    ' Verifica se o valor absoluto do cosseno est  dentro da toler ncia de 1
    IsSameDir = cosTheta > 0
End Function
