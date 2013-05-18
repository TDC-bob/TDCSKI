#NoTrayIcon

Global $_EXTERNAL_TRACKIR_REG_MAIN = "HKEY_CURRENT_USER\Software\NaturalPoint\NaturalPoint\NPClient Location"
Global $_EXTERNAL_TRACKIR_REG_INSTALL_PATH = "Path"
Global $_EXTERNAL_TRACKIR_EXE = False

Global $_EXTERNAL_HELIOS_REG_MAIN = "HKEY_Global_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\App Paths\HeliosControlCenter.exe"
Global $_EXTERNAL_HELIOS_REG_INSTALL_PATH = "Path"
Global $_EXTERNAL_HELIOS_EXE = False

Func _run_externals()
	Local $return
	if not ProcessExists("TrackIR5.exe") Then
		$return = _try("RegRead", $_EXTERNAL_TRACKIR_REG_MAIN & "," & $_EXTERNAL_TRACKIR_REG_INSTALL_PATH, "", False)
		if $return then $_EXTERNAL_TRACKIR_EXE = $return & "\TrackIR5.exe"
	EndIf
	if not ProcessExists("HeliosControlCenter.exe") Then
		$return = _try("RegRead", $_EXTERNAL_HELIOS_REG_MAIN & "," & $_EXTERNAL_HELIOS_REG_INSTALL_PATH, "", False)
		if $return then $_EXTERNAL_HELIOS_EXE = $return & "\HeliosControlCenter.exe"
	EndIf
	local $donesomething = False
	if $_EXTERNAL_TRACKIR_EXE then
		_try("ShellExecute", $_EXTERNAL_TRACKIR_EXE)
		_out($_OUT_NOT, "TrackIR lancé")
		$donesomething = True
	EndIf
	if $_EXTERNAL_HELIOS_EXE then
		_try("ShellExecute", $_EXTERNAL_HELIOS_EXE)
		_out($_OUT_NOT, "HELIOS lancé")
		$donesomething = True
	EndIf
	return $donesomething
EndFunc

;~ Func _start_A10()
;~ 	_try("ShellExecute", $_EXTERNAL_A10_MAIN_FOLDER & '\bin\launcher.exe, "",' & $_EXTERNAL_A10_MAIN_FOLDER)
;~ EndFunc

Func _open_log()
;~ 	_try("ShellExecute", 'notepad.exe, ' & $_EXTERNAL_LOG & ', "", "", ' & @SW_SHOW)
	ShellExecute("notepad.exe", $_LOG_FILE)
EndFunc
