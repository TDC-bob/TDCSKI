#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)


func _getLocalVersion()
If @Compiled Then
	$_LOCAL_VERSION = FileGetVersion(@ScriptFullPath, "FileVersion")
	If @error = 1 Then _out($_ERROR, "Erreur lors de la r�cup�ration de la version locale du programme")
	_out($_DEBUG, "Version compil�e: " & $_LOCAL_VERSION)
Else
	$_LOCAL_VERSION = $_FAKE_VERSION
	_out($_DEBUG, "Version non compil�e: " & $_LOCAL_VERSION)
EndIf
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Update Message Boxes title
$_BOX_TITLE &= " v" & $_LOCAL_VERSION
EndFunc