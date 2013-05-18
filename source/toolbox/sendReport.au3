#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)
Opt("GUIOnEventMode", 1)
Global $_SENDREPORT_USER_NAME_CTRL, $_SENDREPORT_USER_ADDRESS_CTRL, $_SENDREPORT_MAIL_SUBJECT_CTRL, $_SENDREPORT_MAIL_BODY_CTRL, $_SENDREPORT_STATUS_CTRL, $_SENDREPORT_GUI, $_SENDREPORT_SEND_LABEL, $_SENDREPORT_SEND_ICON
Global $_SEND_REPORT_INCLUDE_LOG = False

Func __OnAutoItErrorRegister_INetSmtpMailCom($s_SmtpServer, $s_FromName, $s_FromAddress, $s_Subject = "", $s_Body = "", $s_Username = "", $s_Password = "", $IPPort = 25, $ssl = 0)
	Local $objEmail = ObjCreate("CDO.Message")
	If Not IsObj($objEmail) Then Return SetError(1, 0, 0)

	$objEmail.From = '"' & $s_FromName & '" <' & $s_FromAddress & '>'
	$objEmail.To = "bob@daribouca.net" ;$s_ToAddress

	$objEmail.ReplyTo = $s_FromAddress


	$objEmail.Subject = $s_Subject

	If StringInStr($s_Body, "<") And StringInStr($s_Body, ">") Then
		$objEmail.HTMLBody = $s_Body
	Else
		$objEmail.Textbody = $s_Body & @CRLF
	EndIf

	$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2
	$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserver") = $s_SmtpServer
	$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserverport") = $IPPort

	If $s_Username <> "" Then
		$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpauthenticate") = 1
		$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/sendusername") = $s_Username
		$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/sendpassword") = $s_Password
	EndIf

	If $ssl Then
		$objEmail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpusessl") = True
	EndIf

	$objEmail.Configuration.Fields.Update
	$objEmail.Send

	If @error Then Return SetError(2, 0, $_OAER_ERROR_DATA[1])
EndFunc   ;==>__OnAutoItErrorRegister_INetSmtpMailCom

Func _autoBugReport()
	Local $title = "Envoi d'un rapport d'erreur"
	Local $label = "Il y a eu une erreur durant l'exécution du programme." & @CRLF _
			& "Par sécurité, j'ai tout arrêté. Pourriez-vous prendre 5 secondes et" _
			& " m'envoyer le rapport d'erreur? Ca m'aiderait beaucoup!" & @CRLF & _
			"J'ai juste besoin de votre pseudo et de votre adresse email"
	Local $body = "Le fichier log de la dernière exécution du "&$_APP_NAME&" sera automatiquement inclus à ce mail, mais libre à vous d'inclure vos remarques ou vos questions!"
	Local $subject = ""&$_APP_NAME&" bug report"
	Local $icon = -4
	$_SEND_REPORT_INCLUDE_LOG = True
	__sendMail_ShowGui($title, $body, $label, $subject, $icon)
EndFunc   ;==>_autoBugReport

Func _manualBugReport()
	Local $title = "Envoi d'un rapport d'erreur"
	Local $label = "Merci du temps que vous prenez pour m'aider à améliorer le "&$_APP_NAME&" !"
	Local $body = "Indiquez-moi ici le problème que vous rencontrez avec le "&$_APP_NAME&", et, si vous le pouvez, la façon de le reproduire"
	Local $subject = ""&$_APP_NAME&" bug report"
	Local $icon = -4
	__sendMail_ShowGui($title, $body, $label, $subject, $icon)
EndFunc   ;==>_manualBugReport

Func _contactAuthor()
	Local $title = "Contacter l'auteur du "&$_APP_NAME&""
	Local $label = "Je suis ouvert à toutes vos remarques et suggestions, " & _
			"elle seront prises en compte!"
	Local $body = ""
	Local $subject = ""&$_APP_NAME&" contact"
	Local $icon = -3
	__sendMail_ShowGui($title, $body, $label, $subject, $icon)
EndFunc   ;==>_contactAuthor


Func __sendMail_ShowGui($sTitle, $spBody, $spLabel, $spSubject, $piIcon);, $hParent)
	Local $_SENDREPORT_GUI = GUICreate($sTitle, 400, 350, -1, -1, BitOR($WS_CAPTION, $WS_POPUP, $WS_SYSMENU), -1)

	GUISetIcon("shell32.dll", -157)
	GUISetBkColor(0xE0DFE2)

	GUICtrlCreateLabel("", 1, 1, 398, 1)
	GUICtrlSetBkColor(-1, 0x41689E)

	GUICtrlCreateLabel("", 1, 300, 398, 1)
	GUICtrlSetBkColor(-1, 0x41689E)

	GUICtrlCreateLabel("", 1, 1, 1, 300)
	GUICtrlSetBkColor(-1, 0x41689E)

	GUICtrlCreateLabel("", 398, 1, 1, 300)
	GUICtrlSetBkColor(-1, 0x41689E)

	GUICtrlCreateIcon("user32.dll", $piIcon, 11, 11, 32, 32)

	GUICtrlCreateLabel($spLabel, 50, 20, 300, 90)
	GUICtrlSetBkColor(-1, -2)

	GUICtrlCreateLabel("Votre pseudo", 30, 100, -1, 15)
	$_SENDREPORT_USER_NAME_CTRL = GUICtrlCreateInput($_USER_NAME, 30, 120, 150, 20)

	GUICtrlCreateLabel("Votre adresse e-mail", 230, 105, -1, 15)
	$_SENDREPORT_USER_ADDRESS_CTRL = GUICtrlCreateInput($_USER_MAIL, 230, 120, 150, 20)

	GUICtrlCreateLabel("Sujet", 30, 145, -1, 15)
	$_SENDREPORT_MAIL_SUBJECT_CTRL = GUICtrlCreateInput($spSubject, 30, 160, 350, 20)
	GUICtrlSetState(-1, $GUI_DISABLE)

	GUICtrlCreateLabel("Corps du message", 30, 185, -1, 15)
	$_SENDREPORT_MAIL_BODY_CTRL = GUICtrlCreateEdit($spBody, 30, 200, 350, 90)

	GUICtrlCreateLabel("", 30, 320, 70, 22)
	GUICtrlSetBkColor(-1, 0x706E63)
	GUICtrlSetState(-1, 128)
	Local $_SENDREPORT_SEND_LABEL = GUICtrlCreateLabel("Envoyer", 34, 324, 70, 15)
	GUICtrlSetBkColor(-1, -2)
	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetCursor(-1, 0)

	Local $_SENDREPORT_SEND_ICON = GUICtrlCreateIcon("shell32.dll", -157, 13, 323, 16, 16) ;"shimgvw.dll", -6
	GUICtrlSetCursor(-1, 0)

	GUICtrlCreateLabel("", 300, 320, 70, 22)
	GUICtrlSetBkColor(-1, 0x706E63)
	GUICtrlSetState(-1, 128)
	Local $nCancel_Label = GUICtrlCreateLabel("Annuler", 304, 324, 70, 15)
	GUICtrlSetBkColor(-1, -2)
	GUICtrlSetColor(-1, 0xFFFFFF)
	GUICtrlSetCursor(-1, 0)

	Local $nCancel_Icon = GUICtrlCreateIcon("shell32.dll", -132, 370, 323, 16, 16) ;"shimgvw.dll", -6
	GUICtrlSetCursor(-1, 0)

	$_SENDREPORT_STATUS_CTRL = GUICtrlCreateLabel("", 125, 324, 150, 15)
	GUICtrlSetColor(-1, 0xFF0000)
	GUISetOnEvent($GUI_EVENT_CLOSE, "__exit")


	GUISetState(@SW_SHOW, $_SENDREPORT_GUI)
	GUICtrlSetOnEvent($_SENDREPORT_SEND_ICON, "___send")
	GUICtrlSetOnEvent($_SENDREPORT_SEND_LABEL, "___send")
	GUICtrlSetOnEvent($nCancel_Label, "__exit")
	GUICtrlSetOnEvent($nCancel_Icon, "__exit")
EndFunc   ;==>__sendMail_ShowGui

Func ___send()
	Local $sServer, $sFromName, $sFromAddress, $sSubject, $sBody
	$sServer = "smtp.gmail.com" ; * - Requierd field
	$sFromName = GUICtrlRead($_SENDREPORT_USER_NAME_CTRL) ; * - Requierd field
	$sFromAddress = GUICtrlRead($_SENDREPORT_USER_ADDRESS_CTRL)
	_writeUserInfo($sFromName, $sFromAddress)
	$sSubject = GUICtrlRead($_SENDREPORT_MAIL_SUBJECT_CTRL)
	If $_SEND_REPORT_INCLUDE_LOG Then
		FileClose($_LOG_HANDLE)
		$sBody = GUICtrlRead($_SENDREPORT_MAIL_BODY_CTRL) & @CRLF & @CRLF & FileRead($_LOG_FILE)
	Else
		$sBody = GUICtrlRead($_SENDREPORT_MAIL_BODY_CTRL)
	EndIf

	If $sFromName = "" Then
		MsgBox(48, $_BOX_TITLE & " - " & "Oops", 'Merci de remplir le champ "Votre pseudo"', 0, $_SENDREPORT_GUI)
		Return
	EndIf

	If $sFromAddress = "" Then
		MsgBox(48, $_BOX_TITLE & " - " & "Oops!", 'Merci de remplir le champ "Votre adresse e-mail"', 0, $_SENDREPORT_GUI)
		Return
	EndIf

	GUICtrlSetData($_SENDREPORT_STATUS_CTRL, "Envoi du message en cours")
	GUICtrlSetState($_SENDREPORT_SEND_LABEL, $GUI_DISABLE)
	GUICtrlSetState($_SENDREPORT_SEND_ICON, $GUI_DISABLE)
	__OnAutoItErrorRegister_INetSmtpMailCom($sServer, $sFromName, $sFromAddress, $sSubject, $sBody, _
			"TDCSkinsInstaller", "cEcIestUNmotDEpasse", 465, 1)
	Local $sOAER_Error_Title = "Erreur"
	Local $sOAER_Success_Title = "Succès"
	Local $sOAER_SendBugReport_Title = "Envoi"
	Local $sOAER_UnableToSend_Msg = "Je ne suis pas parvenu à envoyer l'email\n\nCode d'erreur:\n\t0x%X\nDescription:\n\t%s"
	Local $sOAER_BugReportSent_Msg = "Merci!"


	Local $iError = @error

	GUICtrlSetData($_SENDREPORT_STATUS_CTRL, "")
	GUICtrlSetState($_SENDREPORT_SEND_LABEL, $GUI_ENABLE)
	GUICtrlSetState($_SENDREPORT_SEND_ICON, $GUI_ENABLE)

	If $iError Then
		MsgBox(16, $sOAER_SendBugReport_Title & " - " & $sOAER_Error_Title, _
				StringFormat($sOAER_UnableToSend_Msg, $_OAER_ERROR_DATA[0], $_OAER_ERROR_DATA[1]), 0, $_SENDREPORT_GUI)
	Else
		MsgBox(64, $sOAER_SendBugReport_Title & " - " & $sOAER_Success_Title, $sOAER_BugReportSent_Msg, 0, $_SENDREPORT_GUI)
	EndIf

	__exit()
EndFunc   ;==>___send

Func __exit()
	$___done = True
	GUIDelete($_SENDREPORT_GUI)
EndFunc   ;==>__exit
