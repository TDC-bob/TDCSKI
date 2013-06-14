#NoTrayIcon


#AutoIt3Wrapper_Icon=..\resources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=..\updater.exe
#AutoIt3Wrapper_Res_Comment=https://github.com/TDC-bob/TDCSKI.git
#AutoIt3Wrapper_Res_Description=Written & maintained by TDC-Bob
#AutoIt3Wrapper_Res_Fileversion=0.0.1.7
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_LegalCopyright=http://creativecommons.org/licenses/by-nc-sa/3.0/
#AutoIt3Wrapper_Run_After=signtool sign /v /n "Bob" /d "TDCSKI" /du "https://github.com/TDC-bob/TDCSKI.git" /t http://timestamp.verisign.com/scripts/timstamp.dll "%out%"
#AutoIt3Wrapper_AU3Check_Stop_OnWarning=y
#AutoIt3Wrapper_Run_Tidy=y

#include <File.au3>

;~ Local $szDrive, $szDir, $szFName, $szExt
;~ Local $TestPath = _PathSplit($source, $szDrive, $szDir, $szFName, $szExt)

;~ $exe = $szFName & $szExt

ProcessClose("tdcski.exe")

ProcessWaitClose("tdcski.exe", 5)

Sleep(1000)

If ProcessExists("tdcski.exe") Then
	Exit 1
EndIf

FileCopy("tdcski.exe", "..\tdcski.exe", 1)

Run("..\tdcski.exe", "..")
;~ Run($dest, StringRegExpReplace(@ScriptDir, "\\tdcski\z", ""))

Exit 0