#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

Func _downloadSkinsAndMissionsFromDropBox()
	_out($_INFO, "Mise � jour des livr�es", 1)
	Local $http_dropbox_address = "http://dl.dropbox.com/u/73452794/"
	Local $http_PilotesIni = $http_dropbox_address & "pilotes.ini"
	Local $http_dropbox_MissionsFolder = $http_dropbox_address & "Missions/"
	Local $http_dropbox_SkinsFolder = $http_dropbox_address & "Skins/"
	Local $localFile, $remoteFile, $pilotSkin, $liste, $aListe
	Local $local_INI = "temp.ini"
	_try("FileDelete", $local_INI, "Suppression du fichier temporaire �ventuellement laiss� par un run pr�c�dent")
	_try("InetGet", $http_PilotesIni & "," & $local_INI, "T�l�chargement du dernier fichier pilotes.ini")
	Local $aSections = IniReadSectionNames($local_INI)
	If Not IsArray($aSections) Then _out($_ERROR, "Erreur lors du parsing du fichier " & '"pilotes.ini"')
	_ArrayDelete($aSections, 0)
	For $pilot In $aSections
		If $pilot = "default" Then ContinueLoop
		_out($_INFO, $pilot)
		$pilotSkin = IniRead($local_INI, $pilot, "Livr�e", "")
		If $pilotSkin = "" Then
			_out($_DEBUG, "Aucune livr�e pour ce pilote, passage au suivant", -1)
			ContinueLoop
		EndIf
		_tryByRef("ArrayAdd", $_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE, $pilot, False, False, "ajout du pilote � la liste des livr�es � injecter dans le fichier " & '"Graphics.cfg"')
		Local $pilotUpdated = False
		; ZIP
		$localFile = $_TDCSKI_SKINS_FOLDER & $pilot & ".zip"
		$remoteFile = $http_dropbox_SkinsFolder & $pilot & ".zip"
		if __downloadFileIfNecessary($localFile, $remoteFile) then $pilotUpdated = True
		; TXT
		$localFile = $_TDCSKI_SKINS_FOLDER & $pilot & ".txt"
		$remoteFile = $http_dropbox_SkinsFolder & $pilot & ".txt"
		if __downloadFileIfNecessary($localFile, $remoteFile, False) then $pilotUpdated = True
		; LUA
		$localFile = $_A10_LIVERIES_FOLDER & "TDC - " & $pilot & "\description.lua"
		$remoteFile = $http_dropbox_SkinsFolder & $pilot & ".lua"
		_try("DirCreate", $_A10_LIVERIES_FOLDER & "TDC - " & $pilot, "cr�ation du dossier Livery si n�cessaire")
		if __downloadFileIfNecessary($localFile, $remoteFile) then $pilotUpdated = True
		if $pilotUpdated Then
			_out(BitOR($_INFO, $_OUT_SLE), ": pilote mis � jour")
		Else
			_out($_DEBUG, "Le pilote �tait d�j� � jour")
		EndIf
	Next
	_try("FileDelete", $local_INI, "Suppression du fichier temporaire")
	_out($_INFO, "Livr�es � jour", -1)
	If _try("FileExists", $_A10_MISSIONS_FOLDER, "V�rification de l'existence du dossier mission", False) Then
		If Not _try("FileExists", $_A10_MISSIONS_FOLDER_TDC, "V�rification de l'existence du dossier TDC", False) Then
			_try("DirCreate", $_A10_MISSIONS_FOLDER_TDC)
		EndIf
		If Not _try("FileExists", $_A10_MISSIONS_FOLDER_SOLO, "V�rification de l'existence du dossier TDC/SOLO", False) Then
			_try("DirCreate", $_A10_MISSIONS_FOLDER_SOLO)
		EndIf
		If Not _try("FileExists", $_A10_MISSIONS_FOLDER_MULTI, "V�rification de l'existence du dossier TDC/MULTI", False) Then
			_try("DirCreate", $_A10_MISSIONS_FOLDER_MULTI)
		EndIf
		_out($_INFO, "Mises � jour des missions", 1)
		Local $listeMulti = $http_dropbox_MissionsFolder & "Multi/_liste.txt"
		Local $listeSolo = $http_dropbox_MissionsFolder & "Solo/_liste.txt"
		_out($_INFO, "Missions SOLO", 1)
		$liste = _try("InetGetSource", $listeSolo)
		$aListe = StringSplit($liste, @CRLF, 1)
		_tryByRef("ArrayDelete", $aListe, 0)
		For $file In $aListe
			If Not $file Then ContinueLoop
			$localFile = $_A10_MISSIONS_FOLDER_SOLO & $file
			$remoteFile = $http_dropbox_MissionsFolder & "Solo/" & $file
			if __downloadFileIfNecessary($localFile, $remoteFile) then _out($_INFO, "Nouvelle mission t�l�charg�e: " & $file)
		Next
		_out($_INFO, "Synchronisation des missions SOLO termin�e", -1)
		_out($_INFO, "Missions MULTI", 1)
		$liste = _try("InetGetSource", $listeMulti)
		$aListe = StringSplit($liste, @CRLF, 1)
		_tryByRef("ArrayDelete", $aListe, 0)
		For $file In $aListe
			If Not $file Then ContinueLoop
			_try("FileDelete", $_A10_MISSIONS_FOLDER_SOLO & $file)
			$localFile = $_A10_MISSIONS_FOLDER_MULTI & $file
			$remoteFile = $http_dropbox_MissionsFolder & "Multi/" & $file
			if __downloadFileIfNecessary($localFile, $remoteFile) then _out($_INFO, "Nouvelle mission t�l�charg�e: " & $file)
		Next
		_out($_INFO, "Synchronisation des missions Multi termin�e", -1)
		_out($_INFO, "Toutes les mission ont �t� mises � jour", -1)
		Return
	EndIf
EndFunc   ;==>_downloadSkinsAndMissionsFromDropBox

Func __downloadFileIfNecessary($localFile, $remoteFile, $fileIsMandatory = True)
	Local $fileName, $fileDrive, $fileDir, $fileExt, $localFile_size, $remoteFile_size, $return
	_out($_DEBUG, "Traitement du fichier " & $fileExt, 1)
	_PathSplit($localFile, $fileDrive, $fileDir, $fileName, $fileExt)
	$fileName &= $fileExt
	If _try("FileExists", $localFile, "v�rification du fichier local", False) Then
		$localFile_size = _try("FileGetSize", $localFile, "obtention de la taille du fichier local")
;~ 			Local $localFile_size = FileGetSize($localFile)
;~ 			MsgBox(4096, "", "ok")
		$remoteFile_size = _try("InetGetSize", $remoteFile, "obtention de la taille du fichier distant")
		If $localFile_size <> $remoteFile_size Then
			_out($_DEBUG, "Mise � jour du fichier " & '"' & $fileName & '"')
			$return = _try("InetGet", $remoteFile & ',' & $localFile, "", $fileIsMandatory)
		EndIf
	Else
		$return = _try("InetGet", $remoteFile & ',' & $localFile, "", $fileIsMandatory)
		_out($_DEBUG, "T�l�chargement du fichier " & '"' & $fileName & '" r�ussi')
	EndIf
	_out($_DEBUG, "Fin du traitement du fichier " & $fileExt, -1)
	return $return
EndFunc   ;==>__downloadFileIfNecessary
