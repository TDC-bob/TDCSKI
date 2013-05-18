;~ #include "includes.au3"
AutoItSetOption("MustDeclareVars", 1)


Func _7z_extract_file($archive, $dir, $file, $outputDirectory)
	Local $cmd = 'e "' & $archive & '" -y -o"' & $outputDirectory & '" ' & $file & ''
	__7Z_RUN($cmd, $dir)
	_try("FileExists", $outputDirectory & "\" & $file)
EndFunc   ;==>_7z_extract_file

Func _7z_update_file($archive, $dir, $file)
	Local $cmd = 'u "' & $archive & '" "' & $file & '"'
	Local $return = __7Z_RUN($cmd, $dir)
	return $return
EndFunc   ;==>_7z_update_file

Func __7Z_RUN($cmd, $dir, $fatal = True)
	_out($_DEBUG, '__7Z_RUN: running: "' & $_RES_7Z & " " & $cmd & '" in dir "' & $dir & '"')
	if FileExists($_RES_7Z) = 0 Then _out($_ERROR, "Impossible d'accéder à 7zip.exe via le chemin " & '"' & $_RES_7Z & '"')
	Local $exitCode = ShellExecuteWait($_RES_7Z, $cmd, $dir, "open", @SW_HIDE)
	Switch $exitCode
		Case -1
			_out($_ERROR, "__7Z_RUN: 7zip is not installed")
		Case 0
			Return _out($_DEBUG, "__7Z_RUN: succesfully ran command: " & $cmd)
		Case 1
			Return _out($_DEBUG, "__7Z_RUN: succesfully ran command, with minor errors: " & $cmd)
		Case 2
			Return _out($_ERROR, "__7Z_RUN: fatal error with command: " & $cmd, $fatal = True)
		Case 7
			Return _out($_ERROR, "__7Z_RUN: command line error: " & $cmd, $fatal = True)
		Case 8
			Return _out($_ERROR, "__7Z_RUN: not enough memory for operation: " & $cmd, $fatal = True)
		Case 255
			Return _out($_ERROR, "__7Z_RUN: user stopped the process: " & $cmd, $fatal = True)
		Case Else
			MsgBox(4096, "", $exitCode)
			Return _out($_ERROR, "__7Z_RUN: unhandled exit code: " & $cmd, $fatal = True)
	EndSwitch
EndFunc   ;==>__7Z_RUN
