#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

Global Const $_NEW_ALPHA_MSG = "Une nouvelle version ALPHA du TDCSKI est disponible en ligne. Merci du temps que vous prenez pour tester et am�liorer le TDCSKI !! Mettre � jour maintenant?"
Global Const $_NEW_BETA_MSG = "Une nouvelle version BETA du TDCSKI est disponible. Cette version a �t� test�e, mais il est possible qu'il reste des probl�mes encore non-d�couverts. Voulez-vous contribuer � l'am�lioration du TDCSKI ?"
Global Const $_NEW_MINOR_MSG = "Une nouvelle version mineure du TDCSKI est disponible. Cette version apporte de nouvelle fonctionnalit�, ou des corrections. Voulez-vous faire la mise � jour maintenant ?"
Global Const $_NEW_MAJOR_MSG = "Une nouvelle version majeure du TDCSKI est disponible. Cette version apporte de grands changements au TDCSKI, c'est pourquoi il est recommand� de (re)lire les fichier README et CHANGELOG une fois la " & _
		"mise � jour effectu�e. Voulez-vous lancer le t�l�chargement?"

Func _checkForNewerVersion($pLocalVersion = $_LOCAL_VERSION, $pOnlineVersion = "")
	Local $aOnlineVersion, $aLocalVersion
	_out($_INFO, "Recherche d'une nouvelle version", 1)
;~ 	If $_ALPHA_CHECK Then _check_ALPHA()
	$aLocalVersion = _splitVersion($pLocalVersion)
	_out($_INFO, "_checkForNewerVersion: version locale: " & _ArrayToString($aLocalVersion))
	If $pOnlineVersion = "" Then
		$aOnlineVersion = _retrieveOnlineVersion($_HTTP_VERSION_FILE)
	Else
		$aOnlineVersion = _splitVersion($pOnlineVersion)
	EndIf
	_out($_INFO, "_checkForNewerVersion: version en ligne: " & _ArrayToString($aOnlineVersion))
	Local $sOnlineVersion = $aOnlineVersion[1] & "." & $aOnlineVersion[2] & "." & $aOnlineVersion[3] & "." & $aOnlineVersion[4]
	Local $msg[5][3]
	$msg[1][1] = $_NEW_MAJOR_MSG
	$msg[1][2] = "_checkForNewerVersion: nouvelle version majeure disponible"
	$msg[2][1] = $_NEW_MINOR_MSG
	$msg[2][2] = "_checkForNewerVersion: nouvelle version mineure disponible"
	$msg[3][1] = $_NEW_BETA_MSG
	$msg[3][2] = "_checkForNewerVersion: nouvelle version BETA disponible"
	$msg[4][1] = $_NEW_ALPHA_MSG
	$msg[4][2] = "_checkForNewerVersion: nouvelle version BETA disponible"
	Local $newVersionFound = False
	For $i = 1 To 4
		If $aLocalVersion[$i] < $aOnlineVersion[$i] Then
			_out($_INFO, $msg[$i][2])
			$newVersionFound = True
			If Not $_TESTING Then _update($msg[$i][1], $_HTTP_SETUP_FILE, $sOnlineVersion)
		EndIf
	Next
	If Not $newVersionFound Then _out($_INFO, "_checkForNewerVersion: pas de nouvelle version disponible", -1)
	Return
EndFunc   ;==>_checkForNewerVersion

;~ Func _check_ALPHA($pLocalVersion = $_LOCAL_VERSION, $pOnlineVersion = "")
;~ 	_title("V�rification de nouvelle version ALPHA")
;~ 	Local $aLocalVersion = _splitVersion($pLocalVersion)
;~ 	_log("_check_ALPHA: version locale: " & _ArrayToString($aLocalVersion))
;~ 	If $pOnlineVersion <> "" Then
;~ 		Local $aOnlineVersion = _splitVersion($pOnlineVersion)
;~ 	Else
;~ 		Local $aOnlineVersion = _retrieveOnlineVersion($_ONLINE_VERSION_FILE_ALPHA)
;~ 	EndIf
;~ 	_log("_check_ALPHA: version en ligne: " & _ArrayToString($aOnlineVersion))
;~ 	Local $sOnlineVersion = $aOnlineVersion[1] & "." & $aOnlineVersion[2] & "." & $aOnlineVersion[3] & "." & $aOnlineVersion[4]
;~ 	If $aLocalVersion[4] < $aOnlineVersion[4] Then
;~ 		_end("_checkForNewerVersion: nouvelle version alpha disponible")
;~ 		if not $_TESTING then _update($_NEW_ALPHA_MSG, $_ONLINE_ZIP_FILE_ALPHA, $sOnlineVersion)
;~ 	EndIf
;~ EndFunc   ;==>_check_ALPHA

Func _update($msg, $link = $_HTTP_SETUP_FILE, $pNewVersion = "0.0.0.0")
	_out($_DEBUG, "D�but de la proc�dure de mise � jour", 1)
	If MsgBox(4100, $_BOX_TITLE, $msg) = 6 Then
		_out($_DEBUG, "L'utilisateur a accept� de faire la mise � jour")
		Local $downloadLocation = _TempFile(@ScriptDir, "", ".zip")
		_out($_DEBUG, "La nouvelle version sera t�l�charg�e vers " & '"' & $downloadLocation & '"')
		_try("InetGet", $link & "," & $downloadLocation & ", 1", "T�l�chargement de la nouvelle version")
		_out($_DEBUG, "Extraction du fichier Setup.exe")
		_7z_extract_file($downloadLocation, @ScriptDir, "Setup_TDCSKI_v" & $pNewVersion & ".exe", @ScriptDir)
		_try("FileDelete", $downloadLocation, "Suppression du fichier temporaire t�l�charg�", false)
		_out($_DEBUG, "Lancement du fichier Setup.exe extrait")
		ShellExecute(@ScriptDir & "\Setup_TDCSKI_v" & $pNewVersion & ".exe", "/SILENT")
		Exit 2
	EndIf
	_out($_INFO, "La mise � jour a �t� postpos�e par l'utilisateur", -1)
EndFunc   ;==>_update


Func _splitVersion($version)
	_out($_DEBUG, "Eclatement des num�ros de version � partir de la chaine " & '"' & $version & '"', 1)
	Local $aVersion = StringSplit($version, ".")
	If @error Then
		_out($_ERROR, "_splitVersion: erreur pendant le split de la version locale: " & '"' & _ArrayToString($aVersion) & '"', -1)
		Return
	ElseIf $aVersion[0] <> 4 Then
		_out($_ERROR, "_splitVersion: le split de la version locale a donn� des r�sultats innatendus: " & '"' & _ArrayToString($aVersion) & '"', -1)
		Return
	EndIf
	For $i = 1 To 4
		$aVersion[$i] = Int($aVersion[$i])
	Next
	_out($_DEBUG, "_splitversion: �clatement r�ussi; tableau obtenu: " & '"' & _ArrayToString($aVersion) & '"', -1)
	Return $aVersion
EndFunc   ;==>_splitVersion

Func _retrieveOnlineVersion($pLink)
	_out($_DEBUG, "Obtention de la version en ligne", 1)
	Local $sOnlineVersion = _try("InetGetSource", $pLink, "R�cup�ration du num�ro de la version en ligne")
	_out($_DEBUG, "Eclatement de la version obtenue")
	Local $aOnlineVersion = _splitVersion($sOnlineVersion)
	_out($_DEBUG, "Version en ligne r�cup�r�e et �clat�e, retour", -1)
	Return $aOnlineVersion
EndFunc   ;==>_retrieveOnlineVersion
