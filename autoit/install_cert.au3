#NoTrayIcon

#AutoIt3Wrapper_Icon=..\resources\TDCSKI.ico
#AutoIt3Wrapper_Outfile=..\install_cert.exe
#AutoIt3Wrapper_Res_Comment=https://github.com/TDC-bob/TDCSKI.git
#AutoIt3Wrapper_Res_Description=TDCSKI
#AutoIt3Wrapper_Res_Fileversion=0.0.1.10
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_LegalCopyright=http://creativecommons.org/licenses/by-nc-sa/3.0/
#AutoIt3Wrapper_AU3Check_Stop_OnWarning=n

$ca_cer = 'BobCA.cer'
FileInstall("..\resources\BobCA.cer", $ca_cer)
RunWait("certutil -user -addstore Root " & $ca_cer, '',@SW_HIDE)
FileDelete($ca_cer)
exit 1