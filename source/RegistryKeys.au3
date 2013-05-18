#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

;---------------------------------------------
; Base de registre
Switch $_APP_NAME
	Case "TDC Skins Installer"
		Global $_REG_OWN_MASTER_KEY = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{" & $_APP_GUID & "}_is1"
	case "Update Version"

	Case Else
		MsgBox(4096, "Erreur", "application non reconnue: " & $_APP_NAME & " (RegistryKey.au3, ligne 11)")
		exit -1
EndSwitch
Global $_REG_DCS_A10_MASTER_KEY = "HKEY_CURRENT_USER\Software\Eagle Dynamics\DCS A-10C"
Global $_REG_DCS_A10_PATH = "Path"
;---------------------------------------------
; Steam
Global $_REG_STEAM_MASTER_KEY = "HKEY_CURRENT_USER\Software\Valve\Steam"
Global $_REG_STEAM_INSTALL_PATH = "SteamPath"
;---------------------------------------------
; User name and email address
Global $_REG_USER_NAME = "UserName"
Global $_REG_USER_MAIL = "UserMail"
