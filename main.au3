#NoTrayIcon
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Outfile=test.exe
#AutoIt3Wrapper_Change2CUI=y
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
run("python main.py")
exit
if fileexists("test.git") then
	RunWait(@ComSpec & " /c " & 'dist\bin\git.exe fetch', @workingdir)
	RunWait(@ComSpec & " /c " & 'dist\bin\git.exe merge master', @workingdir)
else
	RunWait(@ComSpec & " /c " & 'dist\bin\git.exe clone https://github.com/caolan/async test.git', @workingdir)
endif
sleep(25000)