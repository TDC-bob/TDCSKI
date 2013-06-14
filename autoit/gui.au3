#NoTrayIcon
#include <file.au3>
#include <array.au3>
#include <GUIConstantsEx.au3>
#include <GuiRichEdit.au3>
#include <ButtonConstants.au3>
;~ AutoItSetOption("GUICoordMode", 0)

#include "Globals.au3"
;~ _spawn("C:\Users\bob\Desktop\tests\tdcski.cfg")

Func _spawn($config_file)
	local $test[1]
	local $mod_ok = False
	local $skin_ok = False
	_FileReadToArray($config_file, $test)
	for $i = 0 to $test[0]
		if $test[$i] = "[mod]" then $mod_ok = True
		if $test[$i] = "[skin]" then $skin_ok = True
	Next
	if not ($mod_ok and $skin_ok) then
		_err("le fichier de configuration n'est pas complet, il y a probablement eu un problème pendant l'exécution du script Python. Vérifiez le fichier journal", "spawn_gui")
	EndIf
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
;~ 	$h += $h_offset
;~ 	$h_checkbox_and_label = 30
;~ 	$h_group_sep = 20
;~ 	$w_group_sep = 10
;~ 	$top = $h_offset + $h_group_sep
;~ 	$left = $w_offset + $w_group_sep
;~ 	$h_checkbox_offset = 5
;~ 	$w_sep = 20
;~ 	$h_sep = 10


	$h = 200
	if @DesktopWidth > 1000 then
		$w = 1000
	Else
		$w = 800
	EndIf
	$h_margin = 25
	$w_margin = 10
	$checkbox_h = 25
	$checkbox_h_sep = 5
	$checkbox_w = $w - ( 4*$w_margin )
	$checkbox_left = 2*$w_margin

	$group_w = $w - ( 2*$w_margin )
	$group_left = $w_margin
	$group_sep = 25
	$group_mods_h = ( UBound($mods) * $checkbox_h ) + ( $h_margin ) + $group_sep
	$group_skins_h = ( UBound($skins) * $checkbox_h ) + ( $h_margin ) + $group_sep
	$group_skins_top = $group_mods_h + ( 2*$h_margin )

	$button_w = 120
	$button_h = 60

	$button_top = ( 3*$h_margin ) + $group_mods_h + $group_skins_h
	$button_quit_left = $w_margin
	$button_cert_left = ( $w/2 ) - ( $button_w/2 )
	$button_question_left = ( $w/2 ) + ( $button_w/2 ) + $w_margin
	$button_apply_left = $w - ( $button_w + $h_margin )

	$h = ( 4*$h_margin ) + $button_h + $group_mods_h + $group_skins_h

	GUICreate($str_app_name & " v" & $version, $w, $h)
	local $top = $h_margin
	GUICtrlCreateGroup("Mods", $group_left, $top, $group_w, $group_mods_h)
	$top += $group_sep
	For $mod In $mods
		Assign($mod[0], GUICtrlCreateCheckbox($mod[0] & " -> " & $mod[2], $checkbox_left, $top, $checkbox_w, $checkbox_h))
		$top += $checkbox_h
		If $mod[1] == "True" Then
			GUICtrlSetState(Eval($mod[0]), $GUI_CHECKED)
		EndIf
	Next
	$top = $group_skins_top
	GUICtrlCreateGroup("Skins", $group_left, $top, $group_w, $group_skins_h)
	$top += $group_sep
	For $skin In $skins
		Assign($skin[0], GUICtrlCreateCheckbox($skin[0] & " -> " & $skin[2], $checkbox_left, $top, $checkbox_w, $checkbox_h))
		$top += $checkbox_h
		If $skin[1] == "True" Then
			GUICtrlSetState(Eval($skin[0]), $GUI_CHECKED)
		EndIf
	Next
	$top = $button_top
	$quit_btn = GUICtrlCreateButton("Quitter", $button_quit_left, $button_top, $button_w, $button_h)
	$install_cert_btn = GUICtrlCreateButton("Installer le certificat de Bob", $button_cert_left, $button_top, $button_w, $button_h, $BS_MULTILINE)
	$question_mark_btn = GUICtrlCreateButton("Certificat ?", $button_question_left, $button_top, $button_h, $button_h, $BS_MULTILINE)
	$start_btn = GUICtrlCreateButton("Lancer le TDCSKI", $button_apply_left, $button_top, $button_w, $button_h, $BS_DEFPUSHBUTTON)
	GUISetState()
	local $count = 0
	local $timer = False
	While 1
		$msg = GUIGetMsg()
		Select
			Case $msg = $GUI_EVENT_CLOSE Or $msg = $quit_btn
				ExitLoop
			Case $msg = $question_mark_btn
				_cert_help()
			Case $msg = $install_cert_btn
				if not $timer then $timer = TimerInit()
				if TimerDiff($timer) > 5000 then
					$timer = TimerInit()
					$count = 1
				Else
					$count += 1
					if $count > 5 then
						MsgBox(4096, "Hey!", "Inutile de cliquer comme un taré, s'il ne se passe rien, c'est parce que le certificat est déjà installé!")
					EndIf
				EndIf
				_install_cert()
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

Func _cert_help()
	ShellExecute("http://tueurdechars.xooit.be/t1039-Comment-pourquoi-installer-un-certificat-SSL.htm")
EndFunc

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

Func _install_cert()
	local $func = "install_cert"
	local $rtn_code = ShellExecuteWait(".\tdcski\install_cert.exe")
	if $rtn_code <> 0 Then
		_err("Une erreur s'est produite pendant l'installation du certificat. Code retour: " & $rtn_code, $func)
	EndIf
	__log("Installation du certificat réussie", $func)
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
			If $mode == "mod" Then
				_ArrayAdd($mods, $to_add)
			ElseIf $mode == "skin" Then
				_ArrayAdd($skins, $to_add)
			EndIf
		EndIf
	Next
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

