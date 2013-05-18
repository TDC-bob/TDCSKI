#NoTrayIcon
#RequireAdmin
#region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Version=beta
#AutoIt3Wrapper_Icon=C:\Users\Bob\Desktop\Git\TDCSKI\ressources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=C:\Users\Bob\Desktop\Git\TDCSKI\build\TDC_Skin_Installer.exe
#AutoIt3Wrapper_Res_Comment=Créé pour pour les TDC par Bob
#AutoIt3Wrapper_Res_Description=Installation automatique des livrées TDC pour DCS:A10
#AutoIt3Wrapper_Res_Fileversion=0.8.23.0
#AutoIt3Wrapper_Res_LegalCopyright=source code licensed under GPL
#AutoIt3Wrapper_Res_Language=2060
#AutoIt3Wrapper_Res_requestedExecutionLevel=asInvoker
#AutoIt3Wrapper_AU3Check_Parameters=-q -d -w 3 -w 4 -w 5 -w 6
#AutoIt3Wrapper_Run_Tidy=y
#endregion ;**** Directives created by AutoIt3Wrapper_GUI ****
; ----------------------------------------------------------
; Directives de compilation
; ----------------------------------------------------------
; Includes & header
AutoItSetOption("MustDeclareVars", 1)
Global Const $_APP_NAME	 				= "TDC Skins Installer"
Global Const $_APP_GUID 				= "7B1DB1E8-C6FC-4925-975E-F745BBBB6603"
Global Const $_APP_ONLINE_VERSION_FILE 	= "TDCInstallerVersion"
Global Const $_APP_ONLINE_SETUP_FILE 	= "TDC_Skin_Installer.zip"
Global Const $_APP_MOTD					= 'Pour rappel: si quelque chose devait mal se passer, vous pouvez toujours restaurer le backup qui se trouve dans le répertoire "A10/TDCSkinsInstaller/Backup" ! '
Global $_OAER_ERROR_DATA[2]

#include "_includes.au3"
#include "Globals.au3"
#include "RessourcesFiles.au3"
#include "RegistryKeys.au3"
#include "HTTPLinks.au3"
#include "toolbox\Logging.au3"
#include "toolbox\toolbox.au3"
#include "toolbox\userNameAndMail.au3"
#include "toolbox\SendReport.au3"
#include "OnExit.au3"
HotKeySet("{ESC}", "_userExit")
OnAutoItExitRegister("OnExit")
#include "GUI.au3"
#include "checkConnection.au3"
#include "toolbox\localVersion.au3"
#include "toolbox\7z.au3"
#include "checkVersion.au3"
#include "toolbox\getA10Folder.au3"
#include "filesystemBuilding.au3"
#include "fileBackup.au3"
#include "dropbox.au3"
#include "writeToGraphicsCFG.au3"
#include "toolbox\StringSize.au3"

; ----------------------------------------------------------
; Parsing de la ligne de commande
parseCmdLine()
Func parseCmdLine()
	If $cmdLine[0] > 0 Then
		For $i = 1 To $cmdLine[0]
			Local $s = $cmdLine[$i]
			Select
				Case $s = "/ALPHA" Or $s = "/A"
					$_ALPHA_CHECK = True
				Case Else
					_out(BitOR($_WARNING, $_OUT_MSG, $_OUT_EXT), 'Le programme a été lancé avec le paramètre non recconu suivant: "' & $s & '"' & ". Vérifiez votre raccourci!")
			EndSelect
		Next
	EndIf
EndFunc   ;==>parseCmdLine
; ----------------------------------------------------------
; Vérification de session unique
Singleton($_APP_GUID)
; ----------------------------------------------------------
; Démarrage du programme en tant que tel
_getLocalVersion()
_gui_monitor_start()
_tryToReadUserInfo()
_checkConnection()
_checkForNewerVersion()
_retrieveA10Folder()
_buildFSPaths()
_backupFile($_A10_GRAPHICS_CFG_FILE)
_downloadSkinsAndMissionsFromDropBox()


;~ _out($_INFO, "Connexion au serveur FTP des TDC en cours ... ")
;~ $_FTP_TDC_SESSION_ID = _try("FTPConnect", $_FTP_TDC_SERVER_IP & "," & $_FTP_TDC_USER & "," & $_FTP_TDC_PASS)
;~ _out($_RESULT, " connecté")
;~ _downloadAndInstallSkins()
_writeToGraphicsCFG()
;~ _sync_missions()
_out(BitOR($_INFO, $_OUT_NOT), "Tout s'est bien passé, bons vols ! =þ")
Exit


