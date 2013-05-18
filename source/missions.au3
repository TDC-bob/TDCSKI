#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)



Func _sync_missions()
	_out($_INFO, "Synchronisation des missions avec le serveur TDC", 1)
	_out($_INFO, "D�tection du r�pertoire des fichiers missions ... ")
	If _try("FileExists", $_A10_MISSIONS_FOLDER, "", false) Then
		_out($_RESULT, "r�pertoire trouv� via le chemin " & '"' & $_A10_MISSIONS_FOLDER & '"')
		_out($_INFO, "Cr�ation, si n�cessaire, des sous-dossiers TDC, TDC/SOLO et TDC/MULTI", 1)
		_out($_INFO, "Sous-dossier TDC: ")
		_try("DirCreate", $_A10_MISSIONS_FOLDER_TDC)
		_out($_RESULT, "ok")
		_out($_INFO, "Sous-dossier TDC: ")
		_try("DirCreate", $_A10_MISSIONS_FOLDER_SOLO)
		_out($_RESULT, "ok")
		_out($_INFO, "Sous-dossier TDC: ")
		_try("DirCreate", $_A10_MISSIONS_FOLDER_MULTI)
		_out($_RESULT, "ok", -1)
		_try("FTPSwitchDir", $_FTP_TDC_SESSION_ID & ',' & $_FTP_TDC_RFOLDER_MISSIONS_SOLO)
		_out($_INFO, "Traitement des missions SOLO", 1)
		Local $missionSolo = _try("FTPListFiles", $_FTP_TDC_SESSION_ID)
		if not IsArray($missionSolo) then _out($_ERROR, "_sync_missions: �chec lors de la r�cup�ration de la liste des fichiers pour les missions SOLO")
		_tryByRef("ArrayDelete", $missionSolo, 0)
		For $file In $missionSolo
			_out($_INFO, "Traitement de la mission " & '"' & $file & '"', 1)
			Local $remoteFile = $_FTP_TDC_RFOLDER_MISSIONS_SOLO & "/" & $file
			_out($_INFO, "Fichier distant: " & $remoteFile)
			Local $localFile = $_A10_MISSIONS_FOLDER_SOLO & "\" & $file
			_out($_INFO, "Fichier local: " & $localFile)
			_out($_INFO, "V�rification de l'existence du fichier local ... ")
			If Not _try("FileExists", $localFile, "", False) Then
				_out($_RESULT, "le fichier local n'existe pas, t�l�chargement ... ")
				_try("FTPDownload", $_FTP_TDC_SESSION_ID & "," & $remoteFile & "," & $localFile, False, $INTERNET_FLAG_RELOAD + $INTERNET_FLAG_RESYNCHRONIZE + $FTP_TRANSFER_TYPE_BINARY)
				_out($_RESULT, "fichier t�l�charg�", -1)
			ElseIf Not _try("FTPCompareSize", $_FTP_TDC_SESSION_ID & ',' & $remoteFile & "," & $localFile) Then
				_out($_RESULT, "le fichier local existe, mais sa taille est diff�rente de celle du fichier distant; t�l�chargement ... ")
				_try("FileDelete", $localFile)
				_try("FTPDownload", $_FTP_TDC_SESSION_ID & "," & $remoteFile & "," & $localFile, False, $INTERNET_FLAG_RELOAD + $INTERNET_FLAG_RESYNCHRONIZE + $FTP_TRANSFER_TYPE_BINARY)
				_out($_RESULT, "fichier t�l�charg�", -1)
			Else
				_out($_RESULT, "les fichiers locaux et distants sont de m�me taille, passage au fichier suivant", -1)
			EndIf
		Next
		_out($_INFO, "Toutes les missions SOLO ont �t� trait�es", -1)
		_out($_INFO, "Traitement des missions MULTI", 1)
		_try("FTPSwitchDir", $_FTP_TDC_SESSION_ID & ',' & $_FTP_TDC_RFOLDER_MISSIONS_MULTI)
		Local $missionMulti = _try("FTPListFiles", $_FTP_TDC_SESSION_ID)
		if not IsArray($missionMulti) then _out($_ERROR, "_sync_missions: �chec lors de la r�cup�ration de la liste des fichiers pour les missions MULTI")
		_tryByRef("ArrayDelete", $missionMulti, 0)
		For $file In $missionMulti
			_out($_INFO, "Traitement de la mission " & '"' & $file & '"', 1)
			Local $remoteFile = $_FTP_TDC_RFOLDER_MISSIONS_MULTI & "/" & $file
			_out($_INFO, "Fichier distant: " & $remoteFile)
			Local $localFile = $_A10_MISSIONS_FOLDER_MULTI & "\" & $file
			_out($_INFO, "Fichier local: " & $localFile)
			If Not _try("FileExists", $localFile, "", False) Then
				_out($_RESULT, "le fichier local n'existe pas, t�l�chargement ... ")
				_try("FTPDownload", $_FTP_TDC_SESSION_ID & "," & $remoteFile & "," & $localFile, False, $INTERNET_FLAG_RELOAD + $INTERNET_FLAG_RESYNCHRONIZE + $FTP_TRANSFER_TYPE_BINARY)
				_out($_RESULT, "fichier t�l�charg�", -1)
			ElseIf Not _try("FTPCompareSize", $_FTP_TDC_SESSION_ID & ',' & $remoteFile & "," & $localFile) Then
				_out($_RESULT, "le fichier local existe, mais sa taille est diff�rente de celle du fichier distant; t�l�chargement ... ")
				_try("FileDelete", $localFile)
				_try("FTPDownload", $_FTP_TDC_SESSION_ID & "," & $remoteFile & "," & $localFile, False, $INTERNET_FLAG_RELOAD + $INTERNET_FLAG_RESYNCHRONIZE + $FTP_TRANSFER_TYPE_BINARY)
				_out($_RESULT, "fichier t�l�charg�", -1)
			Else
				_out($_RESULT, "les fichiers locaux et distants sont de m�me taille, passage au fichier suivant", -1)
			EndIf
		Next
		_out($_INFO, "Toutes les missions MULTI ont �t� trait�es", -1)
	Else
		_out($_WARNING, "Synchronisation des missions impossible, je n'ai pas pu d�tecter le r�pertoire dans lequel vos missions sont install�es." & _
		" Il est possible que ce soit parce que vous n'avez pas encore lanc� le jeu sur cet ordinateur." & @CRLF & @CRLF & _
		" Si le probl�me persiste, n'h�sitez pas � prendre contact avec moi !" & @CRLF & "(fermez le TDCSKI pour faire dispara�tre cette fen�tre)", -1)
	EndIf
	_out($_INFO, "Fin de la synchronisation des missions", -1)
EndFunc   ;==>_sync_missions
