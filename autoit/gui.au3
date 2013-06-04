#NoTrayIcon
#include <file.au3>
#include <array.au3>
#include <GUIConstantsEx.au3>
#include <GuiRichEdit.au3>
#include <ButtonConstants.au3>

;~ #include "strings.au3"
;~ _spawn("C:\Users\bob\Desktop\tests\tdcski.cfg")

Func _spawn($config_file)
	$rtn = _parse_config($config_file)
;~ 	_ArrayDisplay($rtn[0])
	$mods = $rtn[0]
	$skins = $rtn[1]
	_ArrayDelete($mods, 0)
	_ArrayDelete($skins, 0)
;~ 	for $mod in $mods
;~ 		_ArrayDisplay($mod)
;~ 	Next
;~ 	for $skin in $skins
;~ 		_ArrayDisplay($skin)
;~ 	next
	$h = 200
	$w = 800
	$top = 30
	$left = 20
	$ch = 20
	$h += UBound($mods) * $ch
	$h += UBound($skins) * $ch
	GUICreate($str_app_name, $w, $h)
	GUICtrlCreateGroup("Mods", 10, 10, 780, (UBound($mods) * 30) + 20)
	For $mod In $mods
		ConsoleWrite($mod & @LF)
		Assign($mod[0], GUICtrlCreateCheckbox($mod[0], $left, $top, 180, $ch))
		If $mod[1] == "True" Then
			GUICtrlSetState(Eval($mod[0]), $GUI_CHECKED)
		EndIf
		GUICtrlCreateLabel($mod[2], 200, $top + 5, 570, $ch)
		$top += ($ch + 10)
	Next
	$top += 20
	GUICtrlCreateGroup("Skins", 10, $top, 780, (UBound($skins) * 30) + 20)
	$top += 20
	For $skin In $skins
		ConsoleWrite($skin & @LF)
		Assign($skin[0], GUICtrlCreateCheckbox($skin[0], $left, $top, 150, $ch))
		If $skin[1] == "True" Then
			GUICtrlSetState(Eval($skin[0]), $GUI_CHECKED)
		EndIf
		GUICtrlCreateLabel($skin[2], 200, $top, 570, $ch)
		$top += ($ch + 10)
	Next
	$quit_btn = GUICtrlCreateButton("Quitter", 20, $top + 20, 120, 60, $BS_DEFPUSHBUTTON)
	$start_btn = GUICtrlCreateButton("Appliquer", $w - 140, $top + 20, 120, 60)
	GUISetState()
	While 1
		$msg = GUIGetMsg()
		Select
			Case $msg = $GUI_EVENT_CLOSE Or $msg = $quit_btn
				ExitLoop
			Case $msg = $start_btn
				Local $content[1]
				_FileReadToArray($config_file, $content)
				For $m In $mods
					$state = GUICtrlRead(Eval($m[0]))
					_set_config($content, $m[0], $state)
				Next
				For $s In $skins
					$state = GUICtrlRead(Eval($s[0]))
					_set_config($content, $s[0], $state)
				Next
				$fh = FileOpen($config_file,258)
				_FileWriteFromArray($fh, $content, 1)
				FileClose($fh)
				_run_tdcski()
		EndSelect
	WEnd



EndFunc   ;==>_spawn

Func _set_config(ByRef $content, $name, $state)
	$do = False
	For $i = 1 To $content[0]
		If $content[$i] = "[[" & $name & "]]" Then
			$do = True
		EndIf
		If $do And StringLeft($content[$i], 9) == "installed" Then
			Switch $state
				Case 1
					$content[$i] = StringReplace($content[$i], "= False", "= True")
				Case 4
					$content[$i] = StringReplace($content[$i], "= True", "= False")
			EndSwitch
		EndIf
	Next
EndFunc   ;==>_set_config

Func _parse_config($file)
	Local $content[1]
	Local $mods[1]
	Local $skins[1]
	_FileReadToArray($file, $content)
	For $i = 1 To $content[0]
		If $content[$i] == "[mod]" Then
			$mode = "mod"
		ElseIf $content[$i] == "[skin]" Then
			$mode = "skin"
		EndIf
		If StringLeft($content[$i], 2) == "[[" Then
			$name = StringTrimLeft(StringTrimRight($content[$i], 2), 2)
			Local $to_add[3]
		EndIf
		If StringLeft($content[$i], 4) == "desc" Then
			$desc = _strip($content[$i])
		EndIf
		If StringLeft($content[$i], 9) == "installed" Then
			$param = _strip($content[$i])
			$to_add[0] = $name
			$to_add[1] = $param
			$to_add[2] = $desc
;~ 				_ArrayDisplay($to_add)
			If $mode == "mod" Then
				_ArrayAdd($mods, $to_add)
			ElseIf $mode == "skin" Then
				_ArrayAdd($skins, $to_add)
			EndIf
		EndIf
	Next
;~ 	For $mod In $mods
;~ 		_ArrayDisplay($mod)
;~ 	Next
;~ 	_ArrayDisplay($mods)
	Local $return[2] = [$mods, $skins]
	Return $return
EndFunc   ;==>_parse_config


Func _strip($string)
	$string = StringSplit($string, " = ", 1)
	$string = $string[2]
	$string = StringStripCR(StringStripWS($string, 3))
	If StringLeft($string, 1) = '"' Then
		$string = StringTrimLeft($string, 1)
	EndIf
	If StringRight($string, 1) = '"' Then
		$string = StringTrimRight($string, 1)
	EndIf
	Return $string
EndFunc   ;==>_strip

