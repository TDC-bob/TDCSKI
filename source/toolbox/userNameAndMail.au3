#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

Func _tryToReadUserInfo()
	_out($_DEBUG, "Lecture des informations utilisateur", 1)
	if _try("FileExists", $_CONFIG_INI, "Vérification de l'existence du fichier config.ini", False) Then
		$_USER_NAME = IniRead($_CONFIG_INI, "User", "Name", "")
		$_USER_MAIL = IniRead($_CONFIG_INI, "User", "Mail", "")
	Else
		_out($_DEBUG, "Le fichier config.ini n'existe pas, abandon de la récupération des informations utilisateur", -1)
	EndIf
EndFunc   ;==>_tryToReadUserInfo

Func _writeUserInfo($pName, $pMail)
	_out($_DEBUG,"Ecriture des informations utilisateur", 1)
	IniWrite($_CONFIG_INI, "User", "Name", $pName)
	IniWrite($_CONFIG_INI, "User", "Mail", $pMail)
	_out("Ecriture terminée", -1)
EndFunc   ;==>_writeUserInfo