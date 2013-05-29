#NoTrayIcon
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Outfile=test.exe
#AutoIt3Wrapper_Change2CUI=n
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

consolewrite(get_python_path())
;run("python main.py")

func get_python_path()
	$path = regread("HKCU\Software\Pythonn\PythonCore\3.3\InstallPath","")
	if @error then
		python_not_found()
		return
	endif
	return $path & "python.exe"
endfunc

func python_not_found()
	consolewrite("handle error here" & @CRLF)
endfunc
