#NoTrayIcon


#AutoIt3Wrapper_Icon=..\resources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=..\updater.exe
#AutoIt3Wrapper_Res_Comment=https://github.com/TDC-bob/TDCSKI.git
#AutoIt3Wrapper_Res_Description=Written & maintained by TDC-Bob
#AutoIt3Wrapper_Res_Fileversion=0.0.0.4
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_LegalCopyright=http://creativecommons.org/licenses/by-nc-sa/3.0/
#AutoIt3Wrapper_AU3Check_Stop_OnWarning=y
#AutoIt3Wrapper_Run_Tidy=y

#include <File.au3>

$source = $CmdLine[0]
$dest = $CmdLine[1]

Local $szDrive, $szDir, $szFName, $szExt
Local $TestPath = _PathSplit($source, $szDrive, $szDir, $szFName, $szExt)

$exe = $szFName & $szExt

ProcessWaitClose($exe, 5)

Sleep(1000)

If ProcessExists($exe) Then
	Exit 1
EndIf

FileCopy($source, $dest, 1)

Run($dest)

Exit 0