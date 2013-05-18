#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)


Func _backupFile($fileToBackup)
	_out($_INFO, "Backup du fichier " & '"' & $fileToBackup & '"', 1)
	$fileToBackup = _PathFull($fileToBackup)
	_out($_INFO, "Chemin complet vers le fichier � sauvegarder: " & '"' & $fileToBackup & '"')
	Local $backup = $_TDCSKI_BACKUP_FOLDER & StringReplace($fileToBackup, $_A10_MAIN_FOLDER & "\", "")
	_out($_INFO, "Chemin complet vers le fichier de backup: " & '"' & $backup & '"')
	If _try("FileExists", $backup, "V�rification de l'existence d'un pr�c�dent backup", False) Then
		_out($_INFO, "Le fichier de backup existe d�j�, aucune modification n'a �t� apport�e au syst�me de fichiers", -1)
	Else
		_try("FileCopy", $fileToBackup & ',' & $backup & ",9", "Copie du fichier vers l'emplacement: " & '"' & $backup & '"')
		_out($_INFO, "Le backup a �t� cr�� avec succ�s", -1)
	EndIf
EndFunc   ;==>_backupFile
