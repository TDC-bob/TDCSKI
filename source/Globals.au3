#include-once
Global $_GUI_MONITOR	= 0
Global $_FATAL         	= True
Global $_ALPHA_CHECK   	= False
Global $_TESTING       	= False
Global $_DONE          	= False
Global $_BOX_TITLE		= $_APP_NAME
Global $___done 		= False
Global $_GUI_STARTED 	= False
Global $_CONFIG_INI		= @scriptdir & "\config.ini"
;---------------------------------------------------------------------------------------------------------------------------------------
; Nom et adresse mail de l'utilisateur
Global $_USER_NAME = ""
Global $_USER_MAIL = ""
;---------------------------------------------------------------------------------------------------------------------------------------
; Skins
Global $_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE[1]
$_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE[0] = 0
;---------------------------------------------------------------------------------------------------------------------------------------
; Versions
Global $_LOCAL_VERSION = "0.0.0.0"
Global $_FAKE_VERSION  = "999.999.999.999"
;---------------------------------------------------------------------------------------------------------------------------------------
; Système de fichiers - TDCSKI
Global $_TDCSKI_FOLDER = "\TDCSkinsInstaller\"
Global $_TDCSKI_BACKUP_FOLDER = $_TDCSKI_FOLDER & "Backups\"
Global $_TDCSKI_SKINS_FOLDER = $_TDCSKI_FOLDER & "Skins\"
Global $_TDCSKI_SKINS_FOLDER_BARE = StringReplace($_TDCSKI_SKINS_FOLDER, "\TDCSkinsInstaller\", "TDCSkinsInstaller\")
;---------------------------------------------------------------------------------------------------------------------------------------
; Système de fichiers - A10
Global $_A10_MAIN_FOLDER = ""
Global $_A10_MISSIONS_FOLDER = @UserProfileDir & "\Saved Games\DCS Warthog\Missions"
Global $_A10_MISSIONS_FOLDER_TDC = $_A10_MISSIONS_FOLDER & "\TDC"
Global $_A10_MISSIONS_FOLDER_SOLO = $_A10_MISSIONS_FOLDER_TDC & "\SOLO\"
Global $_A10_MISSIONS_FOLDER_MULTI = $_A10_MISSIONS_FOLDER_TDC & "\MULTI\"
Global $_A10_GRAPHICS_CFG_FILE = "\Config\graphics.cfg"
Global $_A10_LIVERIES_FOLDER = "\Bazar\Liveries\A-10C\"
Global $_A10_TEMPTEXTURES_FOLDER = "\Bazar\TempTextures"
Global $_A10_DCS_EXE_FILE = ""

