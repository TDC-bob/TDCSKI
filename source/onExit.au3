#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

Func _userExit()
	$_DONE = True
	_out($_DEBUG, "L'utilisateur a quitté")
	exit 1
EndFunc   ;==>_userExit

Func OnExit()
	_out($_DEBUG, "Script's finished. Exit code: " & @exitCode)
	FileClose($_LOG_handle)
	;---------------------------------------------
	; Something went awry ...
	If @exitcode < 0 Then
		_autoBugReport()
		While 1
			Sleep(250)
			If $___done Then ExitLoop
		WEnd
	ElseIf @exitcode = 2 then
		exit 2
	Else
		If $_GUI_STARTED Then
			While 1
				Sleep(250)
				If $_DONE Then ExitLoop
			WEnd
		EndIf
;~ 		if GUICtrlRead ($_CTRL_AUTOSTART_A10) = $GUI_CHECKED then
;~ 			if _run_externals() then
;~ 				If MsgBox(4097, $_BOX_TITLE, 'Configurez éventuellement le TrackIR et Helios, et cliquez sur "OK" pour lancer A10 (ou sur "Annuler" pour quitter)') = 1 then _start_A10()
;~ 			else
;~ 				_start_A10()
;~ 			EndIf
;~ 		EndIf
	EndIf
EndFunc   ;==>OnExit

