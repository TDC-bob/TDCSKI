#NoTrayIcon
#region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=resources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=tdcski.exe
#AutoIt3Wrapper_Res_Icon_Add=resources\TDCSKI.ico
#AutoIt3Wrapper_Run_After=copy "%out%" \\TEST-PC\Users\Public
#endregion ;**** Directives created by AutoIt3Wrapper_GUI ****

Global Const $Python33_x86_download_path = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.msi"
Global Const $Python33_x64_download_path = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.amd64.msi"
Global Const $app_name = "TDCSKI"

Global Const $str_python_not_found = "Le " & $app_name & " a besoin de Python 3.3 pour fonctionner" & @CRLF & @CRLF & "Voulez-vous l'installer maintenant ?"

$python_path = get_python_path()
If $python_path Then
	start_tdcski()
Else
	$install_python = ask_user($app_name, $str_python_not_found)
	If Not $install_python Then
		Exit 0
	EndIf
	install_python()
	start_tdcski()
EndIf

Func start_tdcski()
	ConsoleWrite($python_path & " tdcski.py" & @LF)
	Run($python_path & " tdcski.py", @ScriptDir)
	ConsoleWrite(@error & @LF)
EndFunc   ;==>start_tdcski

Func get_python_path()
	$path = RegRead("HKLM\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
	If @error Then
		$path = RegRead("HKLM64\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
		If @error Then
			$path = RegRead("HKCU\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
			If @error Then
				$path = RegRead("HKCU64\SOFTWARE\Python\PythonCore\3.3\InstallPath", "")
				If @error Then
					Return False
				EndIf
			EndIf
		EndIf
	EndIf
	Return $path & "python.exe"
EndFunc   ;==>get_python_path

Func install_python()
	; $source: URL to the remote file
	; $target: local path to download the file to

	#region - choose correct link depending on OS arch
	Switch @OSArch
		Case "x86"
			$download_link = $Python33_x86_download_path
		Case "x64"
			$download_link = $Python33_x64_download_path
		Case Else
			_error("Architecture OS inconnue: " & @OSArch)
			Exit 1
	EndSwitch
	$local_file = @ScriptDir & "\python_installer.msi"
	#endregion - choose correct link depending on OS arch

	#region - download python
	$size = InetGetSize($download_link, 11)
	ProgressOn($app_name, "Téléchargement de Python3.3")
	$h = InetGet($download_link, $local_file, 27, 1)
	$progress = 0
	While True
		Sleep(200)
		$error = InetGetInfo($h, 4)
		If $error Then
			_error("Erreur pendant le téléchargement de Python")
		EndIf
		$progress_bytes = InetGetInfo($h, 0)
		$progress = $progress_bytes / $size * 100
		ProgressSet($progress, $progress_bytes / 1024 & " / " & $size / 1024 & " KB")
		If InetGetInfo($h, 3) Then
			ExitLoop
		EndIf
	WEnd
	#endregion - download python

	#region - run msiexec installer
	SplashTextOn($app_name, "Installation de Python 3.3 ...")
	RunWait("msiexec /package " & $local_file & " /qn ADDLOCAL=ALL")
	SplashOff()
	#endregion - run msiexec installer
EndFunc   ;==>install_python

Func _error($msg)
	MsgBox(262144, $app_name, $msg)
	Exit 1
EndFunc   ;==>_error

Func ask_user($title, $msg)
	$rtn = MsgBox(4100, $title, $msg)
	Switch $rtn
		Case 6
			Return True
		Case 7
			Return False
		Case Else
			ConsoleWrite("handle error here")
	EndSwitch
EndFunc   ;==>ask_user

