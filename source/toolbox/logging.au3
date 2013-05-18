#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)
#include "Toast.au3"
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Flags for the logging system
Global Const $_OUT_LOG = 0x00000001
Global Const $_OUT_GUI = 0x00000010
Global Const $_OUT_MSG = 0x00000100
Global Const $_OUT_NOT = 0x00001000
Global Const $_OUT_SLE = 0x00010000
Global Const $_OUT_FAT = 0x00100000
Global Const $_OUT_EXT = 0x01000000
Global Const $_OUT_RES = 0x10000000
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Combined flags
Global Const $_DEBUG   = $_OUT_LOG
Global Const $_INFO    = BitOR($_DEBUG, $_OUT_GUI)
Global Const $_WARNING = $_INFO
Global Const $_ERROR   = BitOR($_WARNING, $_OUT_FAT)
Global Const $_RESULT  = BitOR($_OUT_GUI, $_OUT_RES, $_OUT_LOG, $_OUT_SLE)
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Setup logging
Global Const $_LOG_FILE = _PathFull(@ScriptDir & "\log.log")
Global $_LOG_handle = FileOpen($_LOG_FILE, 2)
If $_LOG_handle = -1 Then
	MsgBox(4096, $_BOX_TITLE, "Impossible de créer le fichier log à l'emplacement " &  '"' & $_LOG_FILE & '"')
	Exit -1
EndIf
FileWriteLine($_LOG_handle, "Script démarré le " & @MDAY & "/" & @MON & "/" & @YEAR & " à " & @HOUR _
		& @TAB & "Environnment:" 						& @CRLF _
		& @TAB & "CPUArch: " 		& @CPUArch 			& @CRLF _
		& @TAB & "OSArch: " 		& @OSArch 			& @CRLF _
		& @TAB & "OSType: " 		& @OSType 			& @CRLF _
		& @TAB & "OSVersion: " 		& @OSVersion 		& @CRLF _
		& @TAB & "OSBuild: " 		& @OSBuild 			& @CRLF _
		& @TAB & "ServicePack: " 	& @OSServicePack 	& @CRLF _
		& @TAB & "WorkingDir: " 	& @WorkingDir)

;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Logging functions - Locals
Global $_LOG_SEP = @TAB
Global $_LOG_GUI_IDENT = 0
Global $_LOG_IDENT = 0
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Logging functions - Main output functions
Func _out($pType = $_DEBUG, $pMsg = "", $pIdent = 0)
	If BitAND($pType, $_OUT_LOG) Then _log($pMsg, $pIdent)
	If BitAND($pType, $_OUT_GUI) Then _gui($pMsg, $pIdent, BitAND($pType, $_OUT_SLE))
	If BitAND($pType, $_OUT_NOT) Then _toast($pMsg)
	If BitAND($pType, $_OUT_MSG) Then _msg($pMsg)
	If BitAND($pType, $_OUT_FAT) Then Exit -1
	If BitAND($pType, $_OUT_EXT) Then Exit 2
EndFunc   ;==>_out
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
; Logging functions - Subfunctions
Func _log($pMsg, $pIdent = 0)
	If $pIdent < 0 Then $_LOG_IDENT += $pIdent
	FileWriteLine($_LOG_handle, __time() & @TAB & _StringRepeat($_LOG_SEP, $_LOG_IDENT) & $pMsg)
	If $pIdent > 0 Then $_LOG_IDENT += $pIdent
EndFunc   ;==>_log

Func _msg($pMsg)
	MsgBox(4096, $_BOX_TITLE, $pMsg)
EndFunc   ;==>_msg

Func _toast($pMsg)
	_Toast_Show($_RES_ICON, $_BOX_TITLE, $pMsg, 0, False, False)
EndFunc   ;==>_toast

Func _gui($pMsg, $pIdent, $same_line = False)
	If $_GUI_MONITOR = -1 Then
		_log($_DEBUG, "_gui: tentative d'écriture dans la GUI alors qu'elle n'était pas déclarée. Le message était: " & $pMsg)
		Return
	EndIf
	_GUICtrlEdit_SetText($_GUI_MONITOR, StringRight(_GUICtrlEdit_GetText($_GUI_MONITOR), 28000))
	If $pIdent < 0 Then $_LOG_GUI_IDENT += $pIdent
	If $same_line Then
		_GUICtrlEdit_AppendText($_GUI_MONITOR,$pMsg)
	Else
		_GUICtrlEdit_AppendText($_GUI_MONITOR,@CRLF & _StringRepeat($_LOG_SEP, $_LOG_GUI_IDENT) & $pMsg)
	EndIf
	If $pIdent > 0 Then $_LOG_GUI_IDENT += $pIdent
EndFunc   ;==>_gui

Func __time()
	Return @MIN & ":" & @SEC & "." & @MSEC
EndFunc   ;==>__time

