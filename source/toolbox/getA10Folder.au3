#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)


Func _getFolderFromUser($msg)
	Local $return = _try("FileSelectFolder", $msg & ', "", 2', "Demande du dossier d'installation � l'utilisateur", False)
	If $return = "" Then
		_userExit()
	EndIf
	Return $return
EndFunc   ;==>_getFolderFromUser

Func _retrieveA10Folder()
	_out($_INFO, "Recherche du dossier d'installation d'A10", 1)
	$_A10_MAIN_FOLDER = ""
	_out($_INFO, "Recherche d'une installation normale d'A10 dans la base de registre")
	$_A10_MAIN_FOLDER = _try("RegRead", $_REG_DCS_A10_MASTER_KEY &","& $_REG_DCS_A10_PATH, "Recherche du dossier A10 dans la base de registre", False)
	if $_A10_MAIN_FOLDER = "" then
		_out($_INFO, "Recherche d'une installation STEAM d'A10 dans la base de registre")
		$_A10_MAIN_FOLDER = _try("RegRead", $_REG_STEAM_MASTER_KEY & "," & $_REG_STEAM_INSTALL_PATH, "Recherche du dossier A10 pour la version STEAM", False) & "\steamapps\common\dcs a-10c warthog"
		EndIf
	$_A10_MAIN_FOLDER = StringReplace($_A10_MAIN_FOLDER, "/", "\")
	If $_A10_MAIN_FOLDER = "" Then
		_out($_INFO, "Aucune installation trouv�e dans la base de registre, demande � l'utilsiateur")
		$_A10_MAIN_FOLDER = _getFolderFromUser("Je ne suis pas parvenu � trouver une installation valide de DCS A10 dans la base de registre." _
				 & "Serait-il possible de m'indiquer le chemin vers le r�pertoire du jeu ?")
	EndIf
	_out($_INFO, "V�rification du dossier d'installation ... ")
	$_A10_DCS_EXE_FILE = $_A10_MAIN_FOLDER & "\bin\dcs.exe"
	_try("FileExists", $_A10_DCS_EXE_FILE, 'Verification de la pr�sence de "DCS.EXE" dans le r�pertoire "' & $_A10_MAIN_FOLDER & '\bin"')
	_out($_RESULT, " v�rification ok")
	_out($_INFO, "Dossier A10 trouv�: " & '"' & $_A10_MAIN_FOLDER & '"', -1)
EndFunc   ;==>_retrieveA10Folder
