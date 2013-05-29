#NoTrayIcon
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=TDCSKI.ico
#AutoIt3Wrapper_Outfile=test_x86.exe
#AutoIt3Wrapper_Outfile_x64=test_x64.exe
#AutoIt3Wrapper_Res_Icon_Add=TDCSKI.ico
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

Global Const $Python33_x86_download_path = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.msi"
Global Const $Python33_x64_download_path = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.amd64.msi"
Global Const $app_name = "TDCSKI"

Global Const $str_python_not_found = "Le " & $app_name & " a besoin de Python 3.3 pour fonctionner" & @CRLF & @CRLF & "Voulez-vous l'installer maintenant ?"



func start_main()
	run("python main.py")
endfunc   ;==>start_main

func get_download_link()
	switch @OSArch
		case "x86"
			$download_link = $Python33_x86_download_path
		case "x64"
			$download_link = $Python33_x64_download_path
		case else
			exit 1
	endswitch
	return $download_link
endfunc   ;==>get_download_link

func install_python()
	$python_install_dir = @scriptdir & "\Python3.3"
	; 1° download python
	$download_link = get_download_link()
	InetGet($download_link, @tempdir, 19, 0)
	if @error then
		consolewrite("handle errors")
		exit 1
	endif
	; 2° make dir
	dircreate($python_install_dir)
	run("msiexec TARGETDIR=" & $python_install_dir & " /qn ALLUSERS=0 ADDLOCAL=ALL")
endfunc   ;==>install_python

func get_python_path()
	$path = regread("HKCU\Software\Pythonn\PythonCore\3.3\InstallPath", "")
	if @error then
		return False
	endif
	return $path & "python.exe"
endfunc   ;==>get_python_path

func ask_user($title, $msg)
	$rtn = msgbox(4100, $title, $msg)
	switch $rtn
		case 6
			return True
		case 7
			return False
		case else
			consolewrite("handle error here")
	endswitch
endfunc   ;==>ask_user

func start_launcher()
	$python_path = get_python_path()
	if $python_path then
		consolewrite("should start program here")
		;start_main()
	else
		$install_python = ask_user($app_name, $str_python_not_found)
		if not $install_python then
			exit 0
		endif
		install_python()
	endif
endfunc   ;==>start_launcher

start_launcher()