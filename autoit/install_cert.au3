#NoTrayIcon
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=..\resources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=..\install_cert.exe
#AutoIt3Wrapper_Res_Comment=https://github.com/TDC-bob/TDCSKI.git
#AutoIt3Wrapper_Res_Description=TDCSKI
#AutoIt3Wrapper_Res_Fileversion=0.0.1.15
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_LegalCopyright=http://creativecommons.org/licenses/by-nc-sa/3.0/
#AutoIt3Wrapper_Run_After=signtool sign /v /n "Bob" /d "TDCSKI" /du "https://github.com/TDC-bob/TDCSKI.git" /t http://timestamp.verisign.com/scripts/timstamp.dll "%out%"
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

#include <date.au3>
#include <GuiEdit.au3>
#include "Globals.au3"

local Const $install_cert_log_file = $log_dir & "\" & @YEAR & @MON & @MDAY & " - " & @HOUR & "h" & @MIN & "m" & @SEC & " - install_cert.log"



__install_cert_log("Installation du certificat")
$ca_cer = 'BobCA.cer'
if FileInstall("..\resources\BobCA.cer", $ca_cer) <> 1 Then
	__install_cert_err("Erreur lors de la copie du fichier BobCA.cer")
EndIf
RunWait("certutil -user -addstore Root " & $ca_cer, '',@SW_HIDE)
$error = @error
if $error Then
	__install_cert_err("Erreur lors de l'installation du certificat. Erreur Autoit: " & $error)
EndIf
$error  = EnvGet("ERRORLEVEL ")
if $error <> 0 Then
	__install_cert_err("Erreur lors de l'installation du certificat. Erreur Certutil: " & $error)
EndIf
__install_cert_log("Suppression du fichier certificat temporaire")
if FileDelete($ca_cer) <> 1 Then
	__install_cert_err("Erreur lors de la suppression du fichier temporaire")
EndIf
__install_cert_log("Tout s'est bien passé, le certificat devrait être installé")
exit 0

Func __install_cert_log($msg, $func="install_cert", $TimeStamp = True)
	$hFile = FileOpen($install_cert_log_file, 1)
	If $hFile <> -1 Then
		$msg = _Now() & ' - ' & $func & ' - ' & $msg & @CRLF
		FileWriteLine($hFile, $msg)
		FileClose($hFile)
	EndIf
	_GUICtrlEdit_AppendText($iMemo, $msg)
;~ 	GUICtrlSetData($iMemo, $msg, 1)
EndFunc   ;==>__log

Func __install_cert_err($msg, $func="install_cert")
	__install_cert_log($msg, $func & " - FATAL ERROR")
	Exit 1
EndFunc   ;==>_err