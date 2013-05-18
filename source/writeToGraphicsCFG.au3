#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)


Func _writeToGraphicsCFG()
	_out($_INFO, "Mise � jour du fichier Graphics.cfg")
	_tryByRef("ArrayDelete", $_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE, 0)
	if UBound($_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE) = 0 Then _out($_ERROR, "Le tableau des skins � injecter dans le fichier Graphics.cfg est vide")
	Local $a_GRAPHICS_CFG[1]
	Local $s_ToDelete = ""
	Local $modified = False
	_out($_DEBUG, "Lecture du fichier Graphics.cfg ... ")
	_tryByRef("FileReadToArray", $a_GRAPHICS_CFG, $_A10_GRAPHICS_CFG_FILE)
	Local $pos = -1
	_out($_DEBUG, "D�tection des chemins corrompus par la version 0.7.0.7 du TDCSKI", 1)
	For $i = 1 To $a_GRAPHICS_CFG[0]
		If StringInStr($a_GRAPHICS_CFG[$i], 'path = "TDCSkinsInstaller\Skins\') Then
			_out($_DEBUG, "Chemin corrompu trouv�, ajout pour suppression ... ")
			If StringInStr($s_ToDelete, "[" & $i & "]") > 0 Then ContinueLoop
			$s_ToDelete &= "[" & $i & ']'
			_out($_DEBUG, "ligne ajout�e")
			$modified = True
		EndIf
	Next
	Local $a_ToDelete = StringSplit($s_ToDelete, "[]", 2)
	Local $i_AlreadyDeleted = 0
	For $item In $a_ToDelete
		_out($_DEBUG, "Suppression du chemin corrompu ...")
		If $item > 0 Then
			_ArrayDelete($a_GRAPHICS_CFG, $item - $i_AlreadyDeleted)
			$a_GRAPHICS_CFG[0] -= 1
			$i_AlreadyDeleted += 1
		EndIf
		_out($_DEBUG, "ok")
	Next
	_out($_DEBUG, "Suppression des chemins corrompus termin�e", -1)
	_out($_DEBUG, "Injection des livr�es mises � jour dans le fichier Graphics.cfg", 1)
	For $pack In $_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE
		_out($_DEBUG, "Traitement de la livr�e " & '"' & $pack & '"', 1)
		Local $s_PackString = 'path = "' & StringReplace($_TDCSKI_SKINS_FOLDER_BARE, "\", "/") & $pack & '";'
		_out($_DEBUG, "Chemin vers la livr�e: " & '"' & $s_PackString & '"')
		Local $skip = False
		_out($_DEBUG, "Recherche de la livr�e dans le fichier Graphics.cfg ... ")
		For $i = 1 To $a_GRAPHICS_CFG[0]
			If $a_GRAPHICS_CFG[$i] = "VFSTexturePaths" Then $pos = $i
			If StringInStr($a_GRAPHICS_CFG[$i], $s_PackString) > 0 Then
				_out($_DEBUG, "cette livr�e se trouve d�j� dans le fichier Graphics.cfg, je passe � la suivante", -1)
				$skip = True
				ExitLoop
			EndIf
		Next
		If $skip Then ContinueLoop
		_out($_DEBUG, "la livr�e ne se trouve pas encore dans le fichier Graphics.cfg, je l'ajoute ... ")
		If $pos = -1 Then _out($_ERROR, "_writeToGraphicCFG: impossible de trouver" & '" VFSTexturePaths" dans "' & $_A10_GRAPHICS_CFG_FILE & '"')
		_tryByRef("ArrayInsert", $a_GRAPHICS_CFG, $pos + 3, @TAB & $s_PackString)
		$modified = True
	Next
	If Not $modified Then
		Return _out($_DEBUG, "Aucune modification � apporter � Graphics.cfg", -1)
	EndIf
	Local $h = _try("FileOpen", $_A10_GRAPHICS_CFG_FILE & ",258", "Ouverture du fichier Graphics.cfg en �criture")
	_tryByRef("FileWriteFromArray", $a_GRAPHICS_CFG, $h, 1)
	_out($_DEBUG, "")
	_try("FileClose", $h, "Ecriture termin�e, fermeture du fichier", False)
	Return _out($_INFO, "Le fichier Graphics.cfg a �t� mis � jour avec succ�s", -1)
EndFunc   ;==>_writeToGraphicsCFG
