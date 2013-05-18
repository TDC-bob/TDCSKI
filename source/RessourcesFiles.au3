#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

Global $_RES_ICON
Global $_RES_LOGO
Global $_RES_7Z
Global $_RES_BASE_DIR

If Not @Compiled Then
	Switch @ComputerName
		Case "DARIBOUCA"
			$_RES_BASE_DIR 	= "C:\Users\Bob\Desktop\GIT\master.git\"
		Case "DARIBOUFIX"
			$_RES_BASE_DIR 	= "D:\bob\devel\GIT_WorkingCopies\TDCSKI\"
	EndSwitch
	$_RES_ICON 						= $_RES_BASE_DIR & "ressources\TDCSKI.ico"
	$_RES_LOGO    					= $_RES_BASE_DIR & "ressources\logoTDC.jpg"
	$_RES_7Z						= $_RES_BASE_DIR & "ressources\7zip\7za.exe"
Else
	$_RES_ICON 						= @ScriptFullPath
	$_RES_LOGO    					= @ScriptDir & "\logoTDC.jpg"
	$_RES_7Z 						= @ScriptDir & "\7zip\7za.exe"
EndIf
