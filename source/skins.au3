#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)






Func _downloadAndInstallSkins()
	_out($_INFO, "Téléchargement des livrées manquantes ou mises à jour", 1)
	_try("FTPSwitchDir", $_FTP_TDC_SESSION_ID & ',' & $_FTP_TDC_RFOLDER_SKINS)
	Dim $skinFolders = _try("FTPListFolders", $_FTP_TDC_SESSION_ID, "Récupération de la liste des livrées présentes sur le FTP")
	If Not IsArray($skinFolders) Then _out($_ERROR, "_downloadAndInstallSkins: échec lors de la récupération de la liste des livrées sur le serveur")
	_tryByRef("ArrayDelete", $skinFolders, 0)
	For $skin In $skinFolders
		_out($_INFO, "Traitement de la livrée" & ' "' & $skin & '"', 1)
		Local $zipdone = False, $luadone = False, $txtdone = False
		_tryByRef("ArrayAdd", $_LIST_OF_PACKS_TO_INJECT_IN_GRAPHICS_CFG_FILE, $skin, False, False)
		_try("FTPSwitchDir", $_FTP_TDC_SESSION_ID & ',' & $_FTP_TDC_RFOLDER_SKINS & $skin)
		Local $listOfFilesInSkinFolder = _try("FTPListFiles", $_FTP_TDC_SESSION_ID)
		If Not IsArray($listOfFilesInSkinFolder) Then _out($_ERROR, "_downloadAndInstallSkins: échec lors de la récupération de la liste des fichiers pour la livrée " & '"' & $skin & '"')
		_tryByRef("ArrayDelete", $listOfFilesInSkinFolder, 0)
		Local $localFile = "", $remoteFile = "", $liveryFolder = ""
		For $file In $listOfFilesInSkinFolder
			_out($_INFO, "Traitement du fichier " & '"' & $file & '"', 1)
			Local $updated = False
			$remoteFile = $_FTP_TDC_RFOLDER_SKINS & $skin & "/" & $file
			Switch StringRight($file, 4)
				Case ".lua"
					_out($_INFO, "Fichier identifié comme un fichier .lua")
					If $luadone Then
						_out($_INFO, "Un fichier .lua a déjà été traité pour cette livée; je laisse tomber celui-ci", -1)
						ContinueLoop
					EndIf
					_out($_INFO, "Dossier Livery propre à cette livrée: ")
					$liveryFolder = $_A10_LIVERIES_FOLDER & _Iif(StringCompare(StringLeft($skin, 6), "TDC - ") <> 0, "TDC - ", "") & $skin
					_out($_RESULT, $liveryFolder)
					_out($_INFO, "Vérification de l'existence du dossier Livery ... ")
					If Not _try("FileExists", $liveryFolder, "", False) Then
						_out($_RESULT, "le dossier n'existe pas encore, création ... ")
						_try("DirCreate", $liveryFolder)
						_out($_RESULT, "dossier créé")
					Else
						_out($_RESULT, "le dossier existe déjà")
					EndIf
					$localFile = $liveryFolder & "\description.lua"
					_out($_INFO, "Le fichier de destination pour ce fichier .lua sera " & $localFile)
					$luadone = True
				Case ".txt"
					_out($_INFO, "Fichier identifié comme un fichier .txt")
					If $txtdone Then
						_out($_INFO, "Un fichier .txt a déjà été traité pour cette livée; je laisse tomber celui-ci", -1)
						ContinueLoop
					EndIf
					$localFile = $_TDCSKI_SKINS_FOLDER & $skin & ".txt"
					_out($_INFO, "Le fichier de destination pour ce fichier .txt sera " & $localFile)
					$txtdone = True
				Case ".zip"
					If $zipdone Then
						_out($_INFO, "Un fichier .zip a déjà été traité pour cette livée; je laisse tomber celui-ci", -1)
						ContinueLoop
					EndIf
					$localFile = $_TDCSKI_SKINS_FOLDER & $skin & ".zip"
					_out($_INFO, "Le fichier de destination pour ce fichier .zip sera " & $localFile)
					$zipdone = True
			EndSwitch
			_out($_INFO, "Vérification de l'existence du fichier sur le disque dur local ... ")
			If Not _try("FileExists", $localFile, "", False) Then
				_out($_RESULT, "le fichier n'existe pas, téléchargement ... ")
				_try("FTPDownloadWrapper", $_FTP_TDC_SESSION_ID & "," & $remoteFile & "," & $localFile)
				_out($_RESULT, "fichier téléchargé")
				$updated = True
			Else
				_out($_RESULT, "le fichier existe déjà, comparaison de sa taille avec celle du fichier sur le FTP ... ")
				If not _try("FTPCompareSize", $_FTP_TDC_SESSION_ID & ',' & $remoteFile & "," & $localFile) Then
					_out($_RESULT, "les tailles sont différentes, mise à jour ... ")
					_try("FTPDownloadWrapper", $_FTP_TDC_SESSION_ID & "," & $remoteFile & "," & $localFile)
					_out($_RESULT, "fichier téléchargé")
					$updated = True
				Else
					_out($_RESULT, "les tailles sont identiques, votre fichier est à jour")
				EndIf
			EndIf
			_out($_INFO, "Traitement du fichier terminé", -1)
		Next
		_out($_INFO, "Traitement de la livrée " & '"' & $skin & '"' & " terminé", -1)
	Next
	_out($_INFO, "Toutes vos livrées sont à jour !", -1)
EndFunc   ;==>_downloadAndInstallSkins
