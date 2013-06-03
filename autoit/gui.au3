#NoTrayIcon
#include <file.au3>
#include <array.au3>
#include <GUIConstantsEx.au3>
#include <GuiRichEdit.au3>
#include "strings.au3"
_spawn("C:\Users\bob\Desktop\tests\tdcski.cfg")

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
		if $mod[1] == "True" Then
			GUICtrlSetState(eval($mod[0]), $GUI_CHECKED)
		EndIf
		GUICtrlCreateLabel($mod[2], 200, $top+5, 570, $ch)
		$top += ($ch + 10)
	Next
	$top += 20
	GUICtrlCreateGroup("Skins", 10, $top, 780, (UBound($skins) * 30) + 20)
	$top += 20
	For $skin In $skins
		ConsoleWrite($skin & @LF)
		Assign($skin[0], GUICtrlCreateCheckbox($skin[0], $left, $top, 150, $ch))
		if $skin[1] == "True" Then
			GUICtrlSetState(eval($skin[0]), $GUI_CHECKED)
		EndIf
		GUICtrlCreateLabel($skin[2], 200, $top, 570, $ch)
		$top += ($ch + 10)
	Next

	GUISetState(@SW_SHOWNORMAL)
	Do
	Until GUIGetMsg() = $GUI_EVENT_CLOSE

	local $content[1]
;~ 	_FileReadToArray($config_file, $content)
	for $m in $mods
		$state = GUICtrlRead(eval($m[0]))
		switch $state
			case 1
				IniWrite($config_file, "[" & $m[0] & "]", "installed", "True")
			case 4
				IniWrite($config_file, "[" & $m[0] & "]", "installed", "False")
		EndSwitch
;~ 		_set_config($content, $m[0], $state)
	Next
	for $s in $skins
		$state = GUICtrlRead(eval($s[0]))
		switch $state
			case 1
				IniWrite($config_file, "[" & $s[0] & "]", "installed", "True")
			case 4
				IniWrite($config_file, "[" & $s[0] & "]", "installed", "False")
		EndSwitch
;~ 		_set_config($content, $s[0], $state)
	Next
;~ 	_FileWriteFromArray($config_file, $content, 1)
EndFunc   ;==>_spawn

Func _set_config(ByRef $content, $name, $state)
	$do = False
	for $i = 1 to $content[0]
		if $content[$i] = "[[" & $name & "]]" Then
			$do = True
		EndIf
		if $do and StringLeft($content[$i], 9) == "installed" then
			switch $state
				case 1
					$content[$i] = StringReplace($content[$i], "= False", "= True")
				case 4
					$content[$i] = StringReplace($content[$i], "= True", "= False")
			EndSwitch
		EndIf
	Next
EndFunc

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
	local $return[2] = [ $mods, $skins ]
	Return $return
EndFunc   ;==>_parse_config


Func _strip($string)
	$string = StringSplit($string, " = ", 1)
	$string = $string[2]
	$string = StringStripCR(StringStripWS($string, 3))
	if StringLeft($string,1) = '"' Then
		$string = StringTrimLeft($string,1)
	EndIf
	if stringRight($string, 1) = '"' Then
		$string = StringTrimRight($string,1)
	EndIf
	return $string
EndFunc   ;==>_strip

