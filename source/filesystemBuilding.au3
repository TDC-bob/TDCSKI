#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)




Func _buildFSPaths()
	_out($_INFO, "Construction et vérification des chemins sur le disque", 1)
	; First, we collate some strings together
	$_TDCSKI_FOLDER = $_A10_MAIN_FOLDER & $_TDCSKI_FOLDER
	_out($_INFO, "Dossier du TDCSKI: " & $_TDCSKI_FOLDER)
	$_TDCSKI_BACKUP_FOLDER = $_A10_MAIN_FOLDER & $_TDCSKI_BACKUP_FOLDER
	_out($_INFO, "Dossier de backup: " & $_TDCSKI_BACKUP_FOLDER)
	$_TDCSKI_SKINS_FOLDER = $_A10_MAIN_FOLDER & $_TDCSKI_SKINS_FOLDER
	_out($_INFO, "Dossier des skins: " & $_TDCSKI_SKINS_FOLDER)
	$_A10_GRAPHICS_CFG_FILE = $_A10_MAIN_FOLDER & $_A10_GRAPHICS_CFG_FILE
	_out($_INFO, 'Chemin vers le fichier "graphics.cfg": ' & $_A10_GRAPHICS_CFG_FILE)
	$_A10_LIVERIES_FOLDER = $_A10_MAIN_FOLDER & $_A10_LIVERIES_FOLDER
	_out($_INFO, "Dossier Liveries: " & $_A10_LIVERIES_FOLDER)
	$_A10_TEMPTEXTURES_FOLDER = $_A10_MAIN_FOLDER & $_A10_TEMPTEXTURES_FOLDER
	_out($_INFO, "Dossier TempTextures: " & $_A10_TEMPTEXTURES_FOLDER)

	_out($_INFO, "Vérification des chemins créés", 1)
;~ 	_out($_INFO, "Vérification de l'existence du fichier Graphics.cfg")
	_try("FileExists", $_A10_GRAPHICS_CFG_FILE, "Verification de l'existence du fichier " & '"graphics.cfg".')
;~ 	_out($_INFO, "Vérification de l'existence du dossier Liveries")
	_try("FileExists", $_A10_LIVERIES_FOLDER, "Verification de l'existence du dossier Liveries")
;~ 	_out($_INFO, "Vérification de l'existence du dossier TempTextures")
	_try("FileExists", $_A10_TEMPTEXTURES_FOLDER, "Verification de l'existence du dossier TempTextures")
	if not _try("FileExists", $_TDCSKI_FOLDER, "Vérification de l'existence du répertoire du TDCSKI", false) then _try("DirCreate", $_TDCSKI_FOLDER, "le répertoire n'existe pas, création")
	if not _try("FileExists", $_TDCSKI_BACKUP_FOLDER, "Vérification de l'existence du répertoire de backup du TDCSKI", false) then _try("DirCreate", $_TDCSKI_BACKUP_FOLDER, "le répertoire n'existe pas, création")
	if not _try("FileExists", $_TDCSKI_SKINS_FOLDER, "Vérification de l'existence du répertoire de skins du TDCSKI", false) then _try("DirCreate", $_TDCSKI_SKINS_FOLDER, "le répertoire n'existe pas, création")
	_out($_INFO, "Construction et vérification des chemins sur le disque terminées", -2)
EndFunc   ;==>_buildFSPaths
