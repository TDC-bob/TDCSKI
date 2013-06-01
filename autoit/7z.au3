;~ #include "includes.au3"
#include <file.au3>

$_RES_7Z = _TempFile(@ScriptDir, '', '.exe')



Func _7z_extract_all($archive, $outputDirectory, $wk_dir = '')
	If Not FileExists($outputDirectory) Then
		DirCreate($outputDirectory)
	EndIf
	Local $cmd = 'x "' & $archive & '" -y -o"' & $outputDirectory
	__7Z_RUN($cmd, $wk_dir)
;~ 	_try("FileExists", $outputDirectory)
EndFunc   ;==>_7z_extract_all

Func _7z_extract_file($archive, $file, $outputDirectory, $wk_dir = '')
	Local $cmd = 'e "' & $archive & '" -y -o"' & $outputDirectory & '" ' & $file & ''
	__7Z_RUN($cmd, $wk_dir)
;~ 	_try("FileExists", $outputDirectory & "\" & $file)
EndFunc   ;==>_7z_extract_file

Func _7z_update_file($archive, $file, $wk_dir = '')
	Local $cmd = 'u "' & $archive & '" "' & $file & '"'
	Local $return = __7Z_RUN($cmd, $wk_dir)
	Return $return
EndFunc   ;==>_7z_update_file

Func __7Z_RUN($cmd, $wk_dir = '', $fatal = True)
	If FileExists($_RES_7Z) = 0 Then
		FileInstall("..\resources\7zip\7za.exe", $_RES_7Z)
;~ 		_out($_ERROR, "Impossible d'accéder à 7zip.exe via le chemin " & '"' & $_RES_7Z & '"')
	EndIf
	Local $exitCode = ShellExecuteWait($_RES_7Z, $cmd, $wk_dir, "open", @SW_HIDE)
	Switch $exitCode
		Case -1
;~ 			_out($_ERROR, "__7Z_RUN: 7zip is not installed")
		Case 0
;~ 			Return _out($_DEBUG, "__7Z_RUN: succesfully ran command: " & $cmd)
		Case 1
;~ 			Return _out($_DEBUG, "__7Z_RUN: succesfully ran command, with minor errors: " & $cmd)
		Case 2
;~ 			Return _out($_ERROR, "__7Z_RUN: fatal error with command: " & $cmd, $fatal = True)
		Case 7
;~ 			Return _out($_ERROR, "__7Z_RUN: command line error: " & $cmd, $fatal = True)
		Case 8
;~ 			Return _out($_ERROR, "__7Z_RUN: not enough memory for operation: " & $cmd, $fatal = True)
		Case 255
;~ 			Return _out($_ERROR, "__7Z_RUN: user stopped the process: " & $cmd, $fatal = True)
		Case Else
			MsgBox(4096, "", $exitCode)
;~ 			Return _out($_ERROR, "__7Z_RUN: unhandled exit code: " & $cmd, $fatal = True)
	EndSwitch
	ProcessWaitClose($_RES_7Z)
	FileDelete($_RES_7Z)
EndFunc   ;==>__7Z_RUN
