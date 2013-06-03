#NoTrayIcon
#RequireAdmin
#region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=..\resources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=..\tdcski.exe
#AutoIt3Wrapper_Res_Comment=https://github.com/TDC-bob/TDCSKI.git
#AutoIt3Wrapper_Res_Description=TDCSKI
#AutoIt3Wrapper_Res_Fileversion=0.0.1.46
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_LegalCopyright=http://creativecommons.org/licenses/by-nc-sa/3.0/
#AutoIt3Wrapper_Run_After=signtool sign /v /n "Bob" /d "TDCSKI" /du "https://github.com/TDC-bob/TDCSKI.git" /t http://timestamp.verisign.com/scripts/timstamp.dll "%out%"
#AutoIt3Wrapper_Run_Tidy=y
#endregion ;**** Directives created by AutoIt3Wrapper_GUI ****
;~ #AutoIt3Wrapper_Run_After=copy "%out%" \\TEST-PC\Users\Public\TDCSKI

#include <GUIConstantsEx.au3>
#include <EventLog.au3>
#include <Constants.au3>
#include <date.au3>
#include <File.au3>
#include <WindowsConstants.au3>
#include <EditConstants.au3>
#include <Misc.au3>
#include <GuiEdit.au3>
#include "MD5.au3"
;~ #include "zip.au3"
#include "7z.au3"
#include "strings.au3"

_Singleton("TDCSKI")

Global Const $Python33_x86_download_link = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.msi"
Global Const $Python33_x64_download_link = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.amd64.msi"
Global Const $PortableGit_download_link = "https://dl.dropboxusercontent.com/u/73452794/PortableGit-1.8.1.2-preview20130201.7z"

Global Const $repo = @ScriptDir & "\tdcski"
Global Const $repo_remote = "https://github.com/TDC-bob/TDCSKI.git"

Global Const $updater_path = $repo & "\updater.exe"
Global Const $new_version_path = $repo & "\tdcski.exe"

Global Const $log_dir = @ScriptDir & "\logs"
Global Const $log_file = $log_dir & "\" & @YEAR & @MON & @MDAY & " - " & @HOUR & "h" & @MIN & " - TDCSKI.log"
Global $iMemo, $python_path, $git_path, $gui_handle

Global Const $config_file = @ScriptDir & "\tdcski.cfg"

Global $portable_git_folder = @ScriptDir & "\portable-git"

_main()

Exit 0

Func _main()
	Local $func = "main"
	_first_start()
	_rotate_logs($log_dir)
	; Create GUI
	$w = @DesktopWidth * 0.40
	$h = @DesktopHeight * 0.40
	$gui_handle = GUICreate($str_app_name, $w, $h)
;~ 	$iMemo = GUICtrlCreateEdit("", 2, 2, $w - 2, $h)
	$iMemo = _GUICtrlEdit_Create($gui_handle, "", 2, 2, $w - 2, $h, BitOR($ES_MULTILINE, $ES_WANTRETURN, $WS_VSCROLL, $WS_HSCROLL, $ES_AUTOVSCROLL, $ES_AUTOHSCROLL, $ES_READONLY))
	GUICtrlSetFont($iMemo, 9, 400, 0, "Courier New")
	GUISetState()
	_check_python()
	_check_git()
	_check_repo()
	_write_config()
	_check_for_new_version()
	__log("ON LANCE QUELQUE CHOSE !", $func)
	__log("running: " & $python_path & '"' & FileGetLongName(".\tdcski\tdcski.py") & '"', $func)
	ShellExecute($python_path, '"' & FileGetLongName(".\tdcski\tdcski.py") & '"', ".\tdcski")
	__log($str_all_good, $func)
	GUICtrlSetState($iMemo, $GUI_ENABLE)

	Do
	Until GUIGetMsg() = $GUI_EVENT_CLOSE
EndFunc   ;==>_main

Func _first_start()
	If FileExists($config_file) Then
		Return False
	EndIf
	_ask_user($str_app_name, $str_first_start)
EndFunc   ;==>_first_start

Func _write_config()
	Local $func = "write_config"
	Local $to_write[2][2] = [["python_path", $python_path],["git_path", $git_path]]
	__log("Ecriture du fichier de configuration", $func)
	IniWriteSection($config_file, "general", $to_write, 0)
	If @error Then
		_err("Erreur pendant l'écriture du fichier de configuration", $func)
	EndIf
	__log("Fichier de configuration écrit", $func)
;~ 	IniWrite($config_file, "general", "python_path", $python_path)
EndFunc   ;==>_write_config

Func _check_for_new_version()
	$func = "check_for_new_version"
	__log("Vérification de nouvelle version du lanceur", $func)
	If FileExists($new_version_path) Then
		__log("Repo trouvé, comparaison des fichiers", $func)
		$self_hash = __MD5(@ScriptFullPath)
		$other_hash = __MD5($new_version_path)
		If StringCompare($self_hash, $other_hash) <> 0 Then
			__log("Les hash MD5 sont différents, lancement de l'updater", $func)
			$updater = '"' & $updater_path & '"'
			$dest = '"' & @ScriptFullPath & '"'
			$source = '"' & $new_version_path & '"'
			__log("LE LANCEUR DU TDCSKI VA SE METTRE AUTOMATIQUEMENT A JOUR, NE PANIQUEZ PAS, LES FEMMES ET LES CARIBOUS D'ABORD !", $func)
			Sleep(1500)
			Run($updater, $repo)
			Exit 0
			If @error Then
				_err("Erreur fatale lors de la tentative de mise à jour du lanceur", $func)
				Exit 0
			EndIf
		Else
			__log("Les fichiers sont identiques, on continue", $func)
		EndIf
	Else
		__log("Première exécution, pas de repo cloné", $func)
	EndIf
EndFunc   ;==>_check_for_new_version

Func __MD5($file)
	$func = "__MD5"
	__log("Calcul du hash pour le fichier " & $file, $func)
	Local $BufferSize, $FileHandle
	$BufferSize = 0x20000
	$FileHandle = FileOpen($file, 16)
	If $FileHandle = -1 Then
		_err("Erreur lors de l'ouverture du fichier en lecture binaire", $func)
	EndIf
	__log("Initialisation du DLL MD5", $func)
	$MD5CTX = _MD5Init()
	__log("Injection des chunks du fichier dans le parser", $func)
	$chunk = 1
	For $i = 1 To Ceiling(FileGetSize($file) / $BufferSize)
;~ 		__log("Traitement du chunk " & $chunk, $func) ; Generates too much output
		_MD5Input($MD5CTX, FileRead($FileHandle, $BufferSize))
;~ 		__log("Traitement réussi", $func) ;  Generates too much output
		$chunk += 1
	Next
	__log("Parsing terminé, calcul du hash", $func)
	$Hash = _MD5Result($MD5CTX)
	__log("Calcul terminé, le hash pour ce fichier est " & $Hash, $func)
	__log("Fermeture du fichier", $func)
	If FileClose($FileHandle) == 0 Then
		__log("Erreur lors de la fermeture du fichier", $func)
	EndIf
	Return $Hash
EndFunc   ;==>__MD5

Func _check_repo()
	$func = "check_repo"
	__log("Vérification du repo principal", $func)
	If FileExists($repo) Then
		__log("Le repo existe", $func)
		_pull_repo()
	Else
		_clone_repo()
	EndIf
EndFunc   ;==>_check_repo

Func _pull_repo()
	$func = "pull_repo"
	__log("Pulling repo", $func)
	_git_run("pull origin master", $repo)
EndFunc   ;==>_pull_repo

Func _clone_repo()
	$func = "_clone_repo"
	__log("Cloning repo", $func)
;~ 	_cmd_and__log('"' & $git_path & '"' & "  " & $cmd, $wk)
	_git_run("clone " & $repo_remote & ' "' & $repo & '"')
EndFunc   ;==>_clone_repo

Func _git_run($cmd, $wk = '')
	Local $func = "git_run"
	$code = _cmd_and__log('"' & $git_path & '"' & "  " & $cmd, $wk)
	If $code <> 0 Then
		_err("Erreur de command Git: " & $cmd, $func)
	EndIf
EndFunc   ;==>_git_run

Func _create_dir($dir, $exit_on_error = True)
	Local $func = "create_dir"
	__log("Création du répertoire: " & $dir, $func)
	If FileExists($dir) Then
		$attribs = FileGetAttrib($dir)
		If StringInStr($attribs, "D") Then
			__log("Le répertoire existe déjà", $func)
			Return True
		ElseIf StringInStr($attribs, "N") Then
			If $exit_on_error Then
				_err("Le chemin existe déjà, mais c'est un fichier", $func)
			Else
				__log("Le chemin existe déjà, mais c'est un fichier", $func)
			EndIf
			Return False
		EndIf
	EndIf
	DirCreate($dir)
	If @error Then
		If $exit_on_error Then
			_err("Impossible de créer le répertoire", $func)
		Else
			__log("Impossible de créer le répertoire", $func)
		EndIf
		Return False
	EndIf
	Return True
EndFunc   ;==>_create_dir

Func _rotate_logs($sPath)
	$func = "rotate__logs"
	__log($str_logs_rotation, $func)
	__log("Vérification de l'existence du répertoire de journalisation", $func)
	If Not FileExists($log_dir) Then
		__log("Le répêrtoire n'existe pas, création", $func)
		_create_dir($log_dir)
	Else
		__log("Le répertoire existe", $func)
	EndIf
	__log("Recherche de fichier journaux", $func)
	Local $nHandle = FileFindFirstFile($sPath & "\*.log")
	Local $sFileName, $sFileDate, $sToday = @YEAR & @MON & @MDAY
	If $nHandle = -1 Then
		__log($str_logs_no_logfile_found, $func)
		Return
	EndIf

	While 1
		$sFileName = FileFindNextFile($nHandle)
		If @error Then
			__log("Plus de fichier journal", $func)
			ExitLoop; no more files
		EndIf
		__log("Fichier journal suivant: " & $sFileName, $func)
		$sFileDate = StringLeft($sFileName, 8)
		__log("Date du fichier journal: " & $sFileDate, $func)
		If Number($sFileDate) > 0 Then
			If Number($sFileDate) > 20000101 And Number($sFileDate) < 20500101 Then
				$diff = _DateDiff("D", _DateStringWithSlashes($sFileDate), _DateStringWithSlashes($sToday))
				If @error Then
					ConsoleWrite(_DateStringWithSlashes($sFileDate) & @LF)
				EndIf
				If _DateDiff("D", _DateStringWithSlashes($sFileDate), _DateStringWithSlashes($sToday)) > 7 Then; over a week old?
					__log("Le fichier est vieux de plus d'une semaine, suppression", $func)
					_remove_file(@ScriptDir & "\" & $sFileName)
				EndIf
			EndIf
		EndIf
	WEnd
	FileClose($nHandle)
	__log($str_logs_rotation_finished, $func)
EndFunc   ;==>_rotate_logs

Func _DateStringWithSlashes($sString)
	If StringLen($sString) = 8 Then
		Return StringLeft($sString, 4) & "/" & StringMid($sString, 5, 2) & "/" & StringRight($sString, 2)
	Else
		Return $sString
	EndIf
EndFunc   ;==>_DateStringWithSlashes

Func _check_git()
	Local $func = "check_git"
	__log($str_git_checking, $func)
	$git_path = _get_msysgit_path()
	If $git_path Then
		__log("Git a été trouvé", $func)
		Return
	Else
		__log("Git n'a pas été trouvé, installation avec accord utilisateur", $func)
		$git_path = _ask_user($str_app_name, $str_git_ask_install)
		__log("C'est parti, on installe", $func)
		_install_portable_git()
	EndIf
EndFunc   ;==>_check_git

Func _check_python()
	Local $func = "check_python"
	__log($str_python_checking, $func)
	$python_path = _get_python_path()
	If $python_path Then
		__log("Python a été trouvé", $func)
		Return
	Else
		__log("Python n'a pas été trouvé, installation avec accord utilisateur", $func)
		$install_python = _ask_user($str_app_name, $str_python_ask_install)
		__log("C'est parti, on installe", $func)
		install_python()
	EndIf
EndFunc   ;==>_check_python

Func _install_portable_git()
	Local $func, $fancy_name, $temp_zip_file
	$func = "install_portable_git"
	$fancy_name = "Portable Git"
	$temp_zip_file = _TempFile(@ScriptDir, "")
	__log($str_git_install, $func)
	__log("Fichier temporaire: " & $temp_zip_file, $func)
	_download($PortableGit_download_link, $temp_zip_file, $fancy_name)
	_unzip($temp_zip_file, $portable_git_folder)
	__log("Suppression du fichier d'installation", $func)
	_remove_file($temp_zip_file)
	__log("Installation de Git Portable terminée", $func)
	_check_git()
EndFunc   ;==>_install_portable_git

Func _unzip($zip_file, $target_dir)
	$func = "unzip"
	__log("Décompression du fichier ZIP", $func)
	__log("fichier: " & $zip_file, $func)
	__log("cible: " & $target_dir, $func)
	_7z_extract_all($zip_file, $target_dir)
	Local $error = @error
	If $error Then
		_err("Erreur pendant la décompression ! Code retour: " & $error, $func)
	EndIf
	__log("Décompression OK", $func)
EndFunc   ;==>_unzip

Func _remove_file($file)
	Local $func = "remove_file"
	__log("Suppression du fichier: " & $file, $func)
	If FileExists($file) Then
		FileDelete($file)
		If @error Then
			_err("", $func)
		EndIf
	EndIf
	__log("Suppression OK", $func)
EndFunc   ;==>_remove_file

Func start_tdcski()
	Run($python_path & " tdcski.py", @ScriptDir)
	ConsoleWrite(@error & @LF)
EndFunc   ;==>start_tdcski

Func _ExtractZip($sZipFile, $sDestinationFolder, $sFolderStructure = "")
	Local $i
	Do
		$i += 1
		$sTempZipFolder = @TempDir & "\Temporary Directory " & $i & " for " & StringRegExpReplace($sZipFile, ".*\\", "")
	Until Not FileExists($sTempZipFolder) ; this folder will be created during extraction
	Local $oShell = ObjCreate("Shell.Application")
	If Not IsObj($oShell) Then
		Return SetError(1, 0, 0) ; highly unlikely but could happen
	EndIf
	Local $oDestinationFolder = $oShell.NameSpace($sDestinationFolder)
	If Not IsObj($oDestinationFolder) Then
		DirCreate($sDestinationFolder)
	EndIf
	Local $oOriginFolder = $oShell.NameSpace($sZipFile & "\" & $sFolderStructure) ; FolderStructure is overstatement because of the available depth
	If Not IsObj($oOriginFolder) Then
		Return SetError(3, 0, 0) ; unavailable location
	EndIf
	Local $oOriginFile = $oOriginFolder.Items();get all items
	If Not IsObj($oOriginFile) Then
		Return SetError(4, 0, 0) ; no such file in ZIP file
	EndIf
	$oDestinationFolder.CopyHere($oOriginFile, 20) ; 20 means 4 and 16, replaces files if asked
	DirRemove($sTempZipFolder, 1) ; clean temp dir
	Return 1 ; All OK!
EndFunc   ;==>_ExtractZip

Func _download($link, $target, $fancy_name)
	Local $func = "download"
	__log("Téléchargement en cours", $func)
	__log("Name: " & $fancy_name, $func)
	__log("URL: " & $link, $func)
	__log("Cible: " & $target, $func)
	$size = InetGetSize($link, 11)
	If @error Then
		__log("Impossible de récupérer la taille du fichier distant", $func)
	EndIf
	__log('taille du fichier distant: ' & $size, $func)
	ProgressOn($str_app_name, "Téléchargement de " & $fancy_name)
	__log("Début du téléchargement", $func)
	$h = InetGet($link, $target, 27, 1)
	If @error Then
		_err($str_err_download & $fancy_name, $func)
	EndIf
	$progress = 0
	While True
		Sleep(200)
		$error = InetGetInfo($h, 4)
		If $error Then
			_err($str_err_download & $fancy_name & " ERROR: " & $error, $func)
		EndIf
		$progress_bytes = Round(InetGetInfo($h, 0))
		$progress = $progress_bytes / $size * 100
		ProgressSet($progress, Round($progress_bytes / 1024) & " / " & Round($size / 1024) & " KB")
		If InetGetInfo($h, 3) Then
			ProgressOff()
			ExitLoop
		EndIf
	WEnd
	__log("Téléchargement terminé", $func)
EndFunc   ;==>_download

Func _get_msysgit_path()
	Local $path, $func, $local_install
	$func = "get_msysgit_path"
	$local_install = $portable_git_folder & "\bin\git.exe"
	__log($str_git_searching, $func)
	__log("Vérification de l'installation locale", $func)
	If FileExists($local_install) Then
		__log("Installation locale trouvée", $func)
		Return $local_install
	EndIf
	__log("Pas d'installation locale, caribou pouet", $func)
	__log("Vérification du PATH", $func)
	Run("git")
	If Not @error Then
		__log("Git a été trouvé dans le PATH, joie", $func)
		$path = "git"
		Return $path
	EndIf
	__log("Rien dans le PATH", $func)
	$path = RegRead("HKLM\Software\TortoiseGit", "MSysGit")
	If @error Then
		$path = RegRead("HKLM64\Software\TortoiseGit", "MSysGit")
		If @error Then
			$path = RegRead("HKCU\Software\TortoiseGit", "MSysGit")
			If @error Then
				$path = RegRead("HKCU64\Software\TortoiseGit", "MSysGit")
				If @error Then
					__log("Rien dans la base de registre non plus, no joy", $func)
					Return False
				EndIf
			EndIf
		EndIf
	EndIf
	__log("Le chemin vers Git a été trouvé dans la base de registre", $func)
	$path &= "\git.exe"
	__log("Chemin vers Git: " & $path, $func)
	__log("Verification de l'existence du fichier", $func)
	If Not FileExists($path) Then
		__log("Strange, le fichier est renseigné dans la BDR mais n'existe pas dans le FS", $func)
		Return False
	Else
		__log("Le fichier existe bien", $func)
		Return $path
	EndIf
	__log("Hmmm, je n'aurais jamais dû arriver jusqu'ici ... bizarre ! Pas grave ...", $func)
	Return False
EndFunc   ;==>_get_msysgit_path

Func _get_python_path()
	Local $func = "get_python_path"
	__log($str_python_searching, $func)
	__log("Recherche dans le PATH", $func)
	$pid = Run("python")
	If Not @error Then
		__log("Python a été trouvé dans le PATH, joie", $func)
		ProcessClose($pid)
		$python_version = _cmd("python -V")
		__log("Version installée: " & StringStripWS(StringStripCR($python_version), 8), $func)
		If StringInStr($python_version, "Python 3.3") Then
			Return "python"
		EndIf
	EndIf
	__log("Rien dans le PATH", $func)
	$path = RegRead("HKLM\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
	If @error Then
		$path = RegRead("HKLM64\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
		If @error Then
			$path = RegRead("HKCU\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
			If @error Then
				$path = RegRead("HKCU64\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
				If @error Then
					__log("Rien dans la base de registre non plus, no joy", $func)
					Return False
				EndIf
			EndIf
		EndIf
	EndIf
	$path &= "python.exe"
	__log("Chemin vers Python: " & $path, $func)
	Return $path
EndFunc   ;==>_get_python_path

Func install_python()
	Local $func = "install_python"
	__log($str_python_install, $func)
	Switch @OSArch
		Case "x86"
			__log("Architecture détectée : x86", $func)
			$download_link = $Python33_x86_download_link
		Case "x64"
			__log("Architecture détectée : x64", $func)
			$download_link = $Python33_x64_download_link
		Case Else
			_err("Architecture OS inconnue: " & @OSArch, $func)
			Exit 1
	EndSwitch
	$local_file = @ScriptDir & "\python_installer.msi"
	_download($download_link, $local_file, "Python3.3")
	__log("Installation de Python 3.3 ...", $func)
	$msiexec_return_code = RunWait('msiexec /package "' & $local_file & '" /qn ADDLOCAL=ALL')
	If $msiexec_return_code > 0 Then
		__log("L'installation a échoué. Code retour MSIEXEC: " & $msiexec_return_code & @CRLF & "(cfr. http://msdn.microsoft.com/en-us/library/windows/desktop/aa376931(v=vs.85).aspx )", $func)
		_err($str_err_python_install_failed, $func)
	EndIf
	__log("Suppression du fichier d'installation", $func)
	_remove_file($local_file)
	__log("Installation terminée", $func)
	_check_python()
EndFunc   ;==>install_python

Func _ask_user($title, $msg)
	Local $func = "_ask_user"
	$rtn = MsgBox(4132, $title, $msg, 0, $gui_handle)
	Switch $rtn
		Case 6
			Return
		Case 7
			__log($str_err_user_cancel, $func)
			Exit 0
		Case Else
			_err($str_err_strange_error, $func)
	EndSwitch
EndFunc   ;==>_ask_user

Func __log($msg, $func, $TimeStamp = True)
	$hFile = FileOpen($log_file, 1)
	If $hFile <> -1 Then
		$msg = _Now() & ' - ' & $func & ' - ' & $msg & @CRLF
		FileWriteLine($hFile, $msg)
		FileClose($hFile)
	EndIf
	_GUICtrlEdit_AppendText($iMemo, $msg)
;~ 	GUICtrlSetData($iMemo, $msg, 1)
EndFunc   ;==>__log

Func _err($msg, $func)
	__log($msg, $func & " - FATAL ERROR")
	Exit 1
EndFunc   ;==>_err

Func _cmd_and__log($cmd, $wk_dir = "")
	Local $func = "cmd_and__log"
	$hCMD = Run($cmd, $wk_dir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD)
	If @error Then
		_err($str_err_cmd & $cmd, $func)
	EndIf
	Local $Return
	While 1
		$Return &= StdoutRead($hCMD)
		$Return &= StderrRead($hCMD)
		If @error Then ExitLoop
	WEnd
	$Return = StringReplace($Return, @CR, @CRLF & @TAB); Place a tab in each line of the output for a nicer log format
	$Return = StringReplace($Return, "#", @CRLF & @TAB)
	$msg = _Now() & ' - ' & $func & ' - ' & $cmd & @CRLF & 'Output: ' & $Return & @CRLF
	__log($cmd & @CRLF & @TAB & 'Output: ' & $Return, $func)
EndFunc   ;==>_cmd_and__log

Func _cmd($cmd)
	Local $func = "cmd"
	$hCMD = Run($cmd, '', @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD)
	If @error Then
		_err($str_err_cmd & $cmd, $func)
	EndIf
	Local $Return
	While 1
		$Return &= StdoutRead($hCMD)
		$Return &= StderrRead($hCMD)
		If @error Then ExitLoop
	WEnd
	Return $Return
EndFunc   ;==>_cmd