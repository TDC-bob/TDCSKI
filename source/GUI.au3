#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)
Opt("GUIOnEventMode", 1)
;---------------------------------------------------------------------------------------------------------------------------------------
; Globals
Global $_GUI_MAIN
Global $_CTRL_AUTOSTART_A10
;---------------------------------------------------------------------------------------------------------------------------------------
; Alignement


Func _GUI_Monitor_Start()
;~ 	Local $lastTitle[999]
;~ 	Local $offset 						= 0
	Local $vSep 						= 20
	Local $hSep 						= 20
	Local $size_Status_Bar_Height 		= 20
	Local $size_Gui_Width 				= 1200
	; TDC picture
	Local $size_Pic_Width 				= $size_Gui_Width - 2 * $hSep
	Local $size_Pic_Height 				= 120
	Local $pos_Pic 						= $vSep
	; Control section
	Local $size_Control_Section_Width 	= $size_Gui_Width - 2 * $hSep
	Local $size_Control_Section_Height 	= 200
	Local $pos_Control_Section 			= $pos_Pic + $size_Pic_Height + $vSep
	; Monitor Window
	Local $size_MonitorWindow_Width 		= $size_Gui_Width - 2 * $hSep
	Local $size_MonitorWindow_Height 		= 250
	Local $pos_Monitor_Window 			= $pos_Control_Section + $size_Control_Section_Height + $vSep
	; Gui size
	Local $size_Gui_Height 				= $pos_Monitor_Window + $size_MonitorWindow_Height + $vSep + $size_Status_Bar_Height
	; Labels
;~ 	Local $link_TDC_text 				= 'Site web des Tueurs De Chars'
;~ 	Local $link_TDCSKI_text 			= 'Site web du TDCSKI'
	$_GUI_STARTED 						= True
	$_GUI_MAIN 							= GUICreate($_BOX_TITLE, $size_Gui_Width, $size_Gui_Height)
;~ 	Local $ctrl_Pic 					= GUICtrlCreatePic($_RES_LOGO, $hSep, $pos_Pic, $size_Pic_Width, $size_Pic_Height)
	GUICtrlCreatePic($_RES_LOGO, $hSep, $pos_Pic, $size_Pic_Width, $size_Pic_Height)

	Local $link_TDC_text    = 'Site web des Tueurs De Chars'
	Local $link_TDCSKI_text = 'Site web du TDCSKI'
	Local $link_contact 	= "Contacter l'auteur de ce programme"
	Local $link_report 	  	= "Rapporter un bug ou un problème"
	Local $link_askForSkin  = "Demander votre livrée personnalisée"
	Local $link_getInvolved = "Participez au développement du TDCSKI"
	Local $link_tuto		= "Comment mettre en ligne une mission ou une livrée"
	Local $link_changelog	= "Voir la liste complète des changements"
;~ 	Local $link_openLog     = "Ouvrir le fichier log"
;~ 	Local $chkbox_autostartA10= "Lancer automatiquement A10 à la sortie du programme"

;~ 	Local $ctrl_TDC_Link = GUICtrlCreateLabel($link_TDC_text, $hSep, $pos_Control_Section + $vSep, 250, 15)
	GUICtrlCreateLabel("LIENS:", $hSep, $pos_Control_Section + $vSep, 250, 15)
	GUICtrlSetBkColor(-1, -2)
	GUICtrlSetColor(-1, 0x000000)

;~ 	Local $ctrl_TDC_Link = GUICtrlCreateLabel($link_TDC_text, $hSep, $pos_Control_Section + $vSep, 250, 15)
	GUICtrlCreateLabel($link_TDC_text, $hSep, $pos_Control_Section + $vSep * 2, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "LinkTDC")

	_out($_DEBUG, "Création du lien vers le site du TDCSKI")
;~ 	Local $ctrl_TDCSKI_Link = GUICtrlCreateLabel($link_TDCSKI_text, $hSep, $pos_Control_Section + $vSep * 2, 250, 15)
	GUICtrlCreateLabel($link_TDCSKI_text, $hSep, $pos_Control_Section + $vSep * 3, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "LinkTDCSKI")

	_out($_DEBUG, "Création du lien de contact")
;~ 	Local $ctrl_contact_Link = GUICtrlCreateLabel($link_contact, $hSep, $pos_Control_Section + $vSep * 3, 250, 15)
	GUICtrlCreateLabel($link_contact, $hSep, $pos_Control_Section + $vSep * 4, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "_contactAuthor")

	_out($_DEBUG, "Création du lien de rapport")
;~ 	Local $ctrl_TDCSKI_Link = GUICtrlCreateLabel($link_report, $hSep, $pos_Control_Section + $vSep * 4, 250, 15)
	GUICtrlCreateLabel($link_report, $hSep, $pos_Control_Section + $vSep * 5, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "_manualBugReport")

	_out($_DEBUG, "Création du lien de demande de livrée personnalisée")
;~ 	Local $ctrl_TDCSKI_Link = GUICtrlCreateLabel($link_askForSkin, $hSep, $pos_Control_Section + $vSep * 5, 250, 15)
	GUICtrlCreateLabel($link_askForSkin, $hSep, $pos_Control_Section + $vSep * 6, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "LinkCustomSkin")

	_out($_DEBUG, "Création du lien pour participer au développement du TDCSKI")
;~ 	Local $ctrl_TDCSKI_Link = GUICtrlCreateLabel($link_getInvolved, $hSep, $pos_Control_Section + $vSep * 6, 250, 15)
	GUICtrlCreateLabel($link_getInvolved, $hSep, $pos_Control_Section + $vSep * 7, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "LinkGetInvolved")

	_out($_DEBUG, "Création du lien vers le tuto")
	GUICtrlCreateLabel($link_tuto, $hSep, $pos_Control_Section + $vSep * 8, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "LinkTuto")

	_out($_DEBUG, "Création du lien vers le changelog")
	GUICtrlCreateLabel($link_changelog, $hSep, $pos_Control_Section + $vSep * 9, 250, 15)
	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetColor(-1, 0x3366FF)
	GUICtrlSetCursor(-1, 0)
	GUICtrlSetOnEvent(-1, "LinkChangelog")

	If IsDeclared("_APP_MOTD") Then
		GUICtrlCreateLabel(Eval("_APP_MOTD"), 250 + 2*$hSep, $pos_Control_Section + $vSep, $size_Control_Section_Width -(250 + 2*$hSep), $size_Control_Section_Height * 0.25 - $vSep)
	EndIf

	If @Compiled Then
		Local $lastChanges = "CHANGEMENTS DEPUIS LA DERNIERE VERSION:" & @CRLF
		Local $aTmp[1]
		Local $sFormatted = ""
		_tryByRef("FileReadToArray", $aTmp, @ScriptDir & "\changelog.txt")
		_tryByRef("ArrayDelete", $aTmp, 0)
		_tryByRef("ArrayDelete", $aTmp, 0)
		Local $i = 0
		While $aTmp[$i] <> ""
			$sFormatted = _StringSize($aTmp[$i], Default, Default, Default, "", $size_Control_Section_Width -(250 + 2*$hSep))
			$lastChanges &= $sFormatted[0] & @CRLF
			$i += 1
		WEnd
		GUICtrlCreateLabel($lastChanges, 250 + 2 * $hSep, $pos_Control_Section + $vSep + $size_Control_Section_Height * 0.25, $size_Control_Section_Width -(250 + 2*$hSep), $size_Control_Section_Height * 0.75 - $vSep)
	EndIf

;~ 	_out($_DEBUG, "Création du lien pour le fichier log")
;~ 	Local $ctrl_TDCSKI_OpenLog = GUICtrlCreateLabel($link_openLog, $hSep, $pos_Control_Section + $vSep * 7, 250, 15)
;~ 	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
;~ 	GUICtrlSetColor(-1, 0x3366FF)
;~ 	GUICtrlSetCursor(-1, 0)
;~ 	GUICtrlSetOnEvent(-1, "_open_log")

;~ 	_out($_DEBUG, "Création du bouton de lancement de A10")
;~ 	$_CTRL_AUTOSTART_A10 = GUICtrlCreateCheckbox($chkbox_autostartA10, $hSep, $pos_Control_Section + $vSep * 9, 300, 15)
;~ 	GUICtrlSetBkColor(-1, -2)
;~ 	GUICtrlSetColor(-1, 0xFFFFFF)
;~ 	GUICtrlSetColor(-1, 0x3366FF)
;~ 	GUICtrlSetCursor(-1, 0)

;~ 	Local $aSize
;~ 	$aSize 						= _StringSize($link_TDC_text, Default, Default, Default, Default,(($size_Gui_Width - 2 * $hSep) - $hSep) / 2)
;~ 	Local $ctrl_TDC_Link 				= GUICtrlCreateButton($aSize[0], $hSep, $pos_Control_Section + $vSep, $aSize[2] + 10, $aSize[3] + 10)
;~ 	$aSize 						= _StringSize($link_TDCSKI_text, Default, Default, Default, Default,(($size_Gui_Width - 2 * $hSep) - $hSep) / 2)
;~ 	Local $ctrl_TDCSKI_Link 			= GUICtrlCreateButton($aSize[0], $hSep, $pos_Control_Section + $vSep + 30, $aSize[2] + 10, $aSize[3] + 10)

	$_GUI_MONITOR 						= GUICtrlCreateEdit("Lancement du programme ...", $hSep, $pos_Monitor_Window, $size_MonitorWindow_Width, $size_MonitorWindow_Height, $ES_AUTOVSCROLL + $WS_VSCROLL + $ES_READONLY)
	GUISetOnEvent($GUI_EVENT_CLOSE, "CLOSEClicked")
;~ 	GUICtrlSetOnEvent($ctrl_TDC_Link, "LinkTDC")
;~ 	GUICtrlSetOnEvent($ctrl_TDCSKI_Link, "LinkTDCSKI")
	GUISetState(@SW_SHOW)
EndFunc   ;==>_GUI_Monitor_Start

Func CLOSEClicked()
	_userExit()
EndFunc   ;==>CLOSEClicked

Func LinkTDC()
	ShellExecute("http://tueurdechars.xooit.be/portal.php")
EndFunc   ;==>LinkTDC

Func LinkTDCSKI()
	ShellExecute("http://tdcski.daribouca.net")
EndFunc   ;==>LinkTDCSKI

Func LinkCustomSkin()
	ShellExecute("https://sites.google.com/a/daribouca.net/tdcski/demander-une-livree-personnalisee")
EndFunc   ;==>LinkCustomSkin

Func LinkGetInvolved()
	ShellExecute("https://github.com/daribouca/TDCSkinsInstaller_AUTOIT")
	ShellExecute("https://github.com/daribouca/TDCSkinsInstaller_AUTOIT/issues?labels=&milestone=&page=1&state=open")
EndFunc   ;==>LinkGetInvolved

Func LinkTuto()
	ShellExecute("https://docs.google.com/a/daribouca.net/file/d/0B7vvW7GYaD8oaDMyaFBoQjQwMmM/edit#")
EndFunc   ;==>LinkTuto

Func LinkChangelog()
	ShellExecute('notepad', @ScriptDir & '\changelog.txt')
EndFunc   ;==>LinkChangelog



