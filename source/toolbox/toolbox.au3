#NoTrayIcon
Func Singleton($semaphore)
	Local $_TOOLBOX_ERROROR_ALREADY_EXISTS = 183
	DllCall("kernel32.dll", "int", "CreateSemaphore", "int", 0, "long", 1, "long", 1, "str", $semaphore)
	Local $lastError = DllCall("kernel32.dll", "int", "GetLastError")
	If $lastError[0] = $_TOOLBOX_ERROROR_ALREADY_EXISTS Then
		MsgBox(4096, $_BOX_TITLE, "Le " & $_APP_NAME & " est déjà lancé; il n'est pas possible de lancer plusieurs instances de ce programme")
		$_DONE = True
		Exit 1
	EndIf
EndFunc   ;==>Singleton

Global $_TOOLBOX_ERROR
Global $_TOOLBOX_CALL

Func _try($funcName, $params, $desc = "", $_ERROR_IS_FATAL = True)
	If $_ERROR_IS_FATAL Then
		$_TOOLBOX_ERROR = $_ERROR
	Else
		$_TOOLBOX_ERROR = $_DEBUG
	EndIf
	$_TOOLBOX_CALL = "_try: " & $funcName & "(" & $params & "): " & $desc & ": "
	_out($_DEBUG, $_TOOLBOX_CALL & "lancement") ; On s'annonce dans le log
	$params = StringSplit($params, ',') ; Split des paramètres reçus
	For $_i = 0 To $params[0] 	; Nettoyage d'éventuels espaces dans les paramètres reçus
		$params[$_i] = StringStripWS($params[$_i], 3)
	Next
	Local $i_Flag, $i_Recurse, $i_TimeOut, $return, $f_Root, $f_InitialDir, $i_Background, $iniFile, $section, $key, $default
	Switch $funcName
		;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		; Fonctions  HTTP
		Case "InetGetSource"
			Switch $params[0]
				Case 1
					$i_Flag = True ; default reads data to a string
				Case 2
					$i_Flag = $params[2]
				Case Else
					_wrongNumberOfParams()
			EndSwitch
			$return = _INetGetSource($params[1], $i_Flag)
			If @error Then return _fail("impossible de lire les données distantes à l'adresse: " & $params[1])
			_ok("retour: " & $return)
			Return $return
		Case "InetGet"
			Switch $params[0]
				Case 2
					$i_Flag = 19 ; defaults ignore SSL errors and force a reload (no cache download)
					$i_Background = 0 ; wait before download is complete
				Case 3
					$i_Flag = Int($params[3])
					$i_Background = 0 ; wait before download is complete
				Case 4
					$i_Flag = Int($params[3])
					$i_Background = Int($params[4])
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			If FileExists($params[2]) Then _try("FileDelete", $params[2])
			InetGet($params[1], $params[2], $i_Flag, $i_Background)
			If @error Then return _fail("échec du téléchargement")
			return _ok("téléchargement réussi")
		Case "InetGetSize"
			Switch $params[0]
				Case 1
					$i_Flag = 1 ; default forces reload from remote site
				Case 2
					$i_Flag = $params[2]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			$return = InetGetSize($params[1], $i_Flag)
			If @error Then return _fail()
			_ok("taille  du fichier distant: " & $return)
			Return $return
		Case "Ping"
			Switch $params[0]
				Case 1
					$i_TimeOut = 2500
				Case 2
					$i_TimeOut = $params[2]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			$return = Ping($params[1], $i_TimeOut)
			If @error Then
				Local $error
				Switch @error
					Case 1
						$error = "hôte hors-ligne"
					Case 2
						$error = "hôte injoignable"
					Case 3
						$error = "mauvaise destination"
					Case 4
						$error = "erreur non gérée"
				EndSwitch
				return _fail($error)
			EndIf
			_ok("l'hôte a répondu après " & $return & " millisecondes")
			Return $return
			;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			; Fonctions de BDR
		Case "RegWrite"
			If $params[0] <> 4 Then _wrongNumberOfParams()
			$return = RegWrite($params[1], $params[2], $params[3], $params[4])
			If @error Then
				Switch @error
					Case 1
						return _fail("impossible d'ouvrir la clef demandée")
					Case 2
						return _fail("impossible d'ouvrir la clef maitresse demandée")
					Case 3
						return _fail("impossible de se connecter au registre")
					Case -1
						return _fail("impossible d'acéder à la valeur demandée")
					Case -2
						return _fail("type de valeur non supporté")
				EndSwitch
			EndIf
			_ok("écriture de la clef réussie")
			Return $return
		Case "RegRead"
			If $params[0] <> 2 Then Return _wrongNumberOfParams()
			$return = RegRead($params[1], $params[2])
			If @error Then
				Switch @error
					Case -2
						return _fail("type de valeur non supporté")
					Case -1
						return _fail("impossible de lire la valeur de la clef")
					Case 1
						return _fail("impossible d'ouvrir la sous clef demandée")
					Case 2
						return _fail("impossible d'ouvrir la clef demandée")
					Case 3
						return _fail("impossible de se connecter au registre distant")
				EndSwitch
			EndIf
			_ok('retour: "' & $return & '"')
			Return $return
			;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			; Fonctions de Fichiers et Dossiers
		Case "FileGetSize"
			If $params[0] <> 1 Then Return _wrongNumberOfParams()
			$return = FileGetSize($params[1])
			If @error Then return _fail("échec")
			_ok("taille du fichier: " & $return)
			Return $return
		Case "FileSelectFolder"
			Switch $params[0]
				Case 1
					$f_Root = ""
					$i_Flag = 2 ; 1: show "create folder" 2: new dialog style 4: show edit control to type a folder name
					$f_InitialDir = ""
				Case 2
					$f_Root = $params[2]
					$i_Flag = 2 ; 1: show "create folder" 2: new dialog style 4: show edit control to type a folder name
					$f_InitialDir = ""
				Case 3
					$f_Root = $params[2]
					$i_Flag = $params[3]
					$f_InitialDir = ""
				Case 4
					$f_Root = $params[2]
					$i_Flag = $params[3]
					$f_InitialDir = $params[4]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			$return = FileSelectFolder($params[1], $f_Root, Int($i_Flag), $f_InitialDir)
			If @error = 1 Then return _fail("opération annulée par l'utilisateur")
			_ok("choix de l'utilisateur: " & $return)
			Return $return
		Case "FileClose"
			If $params[0] <> 1 Then Return _wrongNumberOfParams()
			If FileClose(Int($params[1])) = 0 Then return _fail("échec lors de la fermeture du fichier")
			return _ok("fichier fermé avec succès")
		Case "FileWrite"
			If $params[0] <> 2 Then Return _wrongNumberOfParams()
			If FileWrite(Int($params[1]), $params[2]) = 0 Then return _fail('le fichier "' & $params[1] & '" ne peut être ouvert en écriture, est déjà utilisé par un autre programme, ou est en lecture seule.')
			return _ok('écriture réussie')
		Case "FileOpen"
			Switch $params[0]
				Case 1
					$i_Flag = 0 ; open file in read-mode as default behaviour
				Case 2
					$i_Flag = Int($params[2])
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			$return = FileOpen($params[1], $i_Flag)
			If $return = -1 Then return _fail("erreur lors de l'ouverture du fichier " & '"' & $params[1] & '" (mode: ' & $i_Flag & ')')
			_ok('fichier ouvert')
			Return $return
		Case "FileGetVersion"
			If $params[0] <> 2 Then Return _wrongNumberOfParams()
			$return = FileGetVersion($params[1], $params[2])
			If @error Then return _fail("échec lors de la récupération de l'information " & '"' & $params[2] & '"'& " du fichier: " & '"' &  $params[1] & '"')
			_ok('lecture réussie; retour: ' & $return)
			Return $return
		Case "FileExists"
			If $params[0] <> 1 Then Return _wrongNumberOfParams()
			If FileExists($params[1]) = 0 Then return _fail('le fichier "' & $params[1] & '"' & " n'existe pas")
			return _ok('le fichier existe')
		Case "FileMove"
			Switch $params[0]
				Case 2
					$i_Flag = 9 ; overwrite and autocreate structure by default
				Case 3
					$i_Flag = $params[3]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			If FileMove($params[1], $params[2], $i_Flag) = 0 Then return _fail('échec du déplacement')
			return _ok("fichier déplacé")
		Case "FileCopy"
			Switch $params[0]
				Case 2
					$i_Flag = 8 ; do not overwrite by default, but create directory structure (1: overwrite, 0: do not create structure)
				Case 3
					$i_Flag = $params[3]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			If FileCopy($params[1], $params[2], Int($i_Flag)) = 0 Then return _fail('échec de la copie du fichier "' & $params[1] & '" vers "' & $params[2] & '"')
			_ok('copie du fichier réussie')
		Case "FileDelete"
			If $params[0] <> 1 Then Return _wrongNumberOfParams()
			If FileExists($params[1]) = 0 Then
				_ok("le fichier n'existait pas")
				Return True
			EndIf
			If FileDelete($params[1]) = 0 Then
				_out(BitOR($_OUT_MSG, $_OUT_EXT), "Impossible de supprimer le fichier " & @CRLF & @CRLF & $params[1] & @CRLF & @CRLF & "Vérifiez qu'il n'est pas ouvert quelque part et relancez le TDCSKI")
;~ 				_out($_TOOLBOX_ERROR, "_try: " & $funcName & ': Impossible de supprimer le fichier  "' & $params[1])
				_fail()
			EndIf
			return _ok('fichier supprimé')
			Return True
		Case "DirCopy"
			Switch $params[0]
				Case 2
					$i_Flag = 0 ;do not overwrite destination
				Case 3
					$i_Flag = $params[3]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			If DirCopy($params[1], $params[2], Int($i_Flag)) = 0 Then return _fail('échec de la copie du répertoire "' & $params[1] & '" vers "' & $params[2] & '"')
			return _ok('répertoire copié')
		Case "DirCreate"
			If $params[0] <> 1 Then Return _wrongNumberOfParams()
			If FileExists($params[1]) = 1 Then Return _ok("le répertoire existe déjà")
			If DirCreate($params[1]) = 0 Then Return _fail("échec")
			Return _ok("répertoire créé")
		Case "DirRemove"
			Switch $params[0]
				Case 1
					$i_Recurse = 1 ; delete subidrs by defaults (0 to override)
				Case 2
					$i_Recurse = $params[2]
				Case Else
					Return _wrongNumberOfParams()
			EndSwitch
			If Not _try("FileExists", $params[1], "", False) Then Return _ok("le répertoire n'existe pas")
			If DirRemove($params[1], $i_Recurse) = 0 Then Return _fail("échec de la suppression du répertoire")
			Return _ok("répertoire supprimé")
		Case "IniRead"
			Switch $params[0]
				Case 3
					$iniFile 	= $params[1]
					$section 	= $params[2]
					$key		= $params[3]
					$default	= ""
				Case 4
					$iniFile 	= $params[1]
					$section 	= $params[2]
					$key		= $params[3]
					$default	= $params[4]
				Case Else
					_wrongNumberOfParams()
			EndSwitch
			$return = IniRead($iniFile, $section, $key, $default)
			If $return = $default Then
				_ok("la valeur lue est égale à la valeur par défaut: la clef demandée n'existe peut-être pas. Valeur lue: " & $return)
			Else
				_ok("valeur lue: " & $return)
			EndIf
			Return $return
		Case "IniWrite"
			If $params[0] <> 4 Then _wrongNumberOfParams()
			If IniWrite($params[1], $params[2], $params[3], $params[4]) = 0 Then Return _fail("écriture impossible")
			Return _ok("écriture réussie")
		Case Else
			Return _out($_ERROR, "_try: fonction inconnue: " & $funcName)
	EndSwitch
EndFunc   ;==>_try

;-------------------------------------------------------------------------------------------------------------------------------
Func _tryByRef($funcName, ByRef $param1, $param2 = False, $param3 = False, $param4 = False, $desc = "", $_ERROR_IS_FATAL = True)
	If $_ERROR_IS_FATAL Then
		$_TOOLBOX_ERROR = $_ERROR
	Else
		$_TOOLBOX_ERROR = $_WARNING
	EndIf
	$_TOOLBOX_CALL = "_tryByRef: " & $funcName & "(" & $param1 & "," & $param2 & "," & $param3 & "," & $param4 & "): " & $desc & ": "
	If Not IsArray($param1) Then _out($_ERROR, "_tryByRef: " &$funcName & ": la première valeur passée n'est pas un tableau valide")
	Switch $funcName
		Case "ArrayInsert"
			If IsBool($param2) And Not $param2 Then _wrongNumberOfParams()
			If IsBool($param3) And Not $param3 Then _wrongNumberOfParams()
			_ArrayInsert($param1, $param2, $param3)
			If @error Then
				Switch @error
					Case 1
						_fail("la valeur passée n'est pas un tableau")
					Case 2
						_fail("le tableau passé en paramètre n'est pas un tableau à 1 dimension")
				EndSwitch
				Return False
			EndIf
			_ok()
			Return True
		Case "FileWriteFromArray"
			; call as follow: _tryStatic("FileWriteFromArray", ByRef $array, $file, [ $base, [ $bound ] ] )
			If IsBool($param2) And Not $param2 Then _wrongNumberOfParams()
			If Not $param3 Then $param3 = 0 ; "base" defaults to element 0
			If Not $param4 Then $param4 = 0 ; "bound" defaults to all elements (whole array)
			_FileWriteFromArray($param2, $param1, $param3, $param4)
			If @error Then
				Switch @error
					Case 1
						_fail("erreur lors de l'ouverture du fichier " &  '"' & $param2 & '"')
					Case 2
						_fail("la variable passée en référence n'est pas un tableau")
					Case 3
						_fail("erreur lors de l'écriture dans le fichier")
				EndSwitch
				Return False
			EndIf
			_ok()
			Return True
		Case "FileReadToArray"
			If IsBool($param2) And Not $param2 Then _wrongNumberOfParams()
			_FileReadToArray($param2, $param1)
			If @error Then
				Switch @error
					Case 1
						_fail("erreur à l'ouverture du fichier")
					Case 2
						_fail("erreur lors de l'éclatage du fichier vers un tableau")
				EndSwitch
				Return False
			EndIf
			_ok()
			Return True
		Case "ArrayAdd"
			If IsBool($param2) And Not $param2 Then Return _wrongNumberOfParams()
			If Not IsArray($param1) Then _out($_ERROR, "_tryByRef: " &$funcName & ": la valeur passée n'est pas un tableau valide")
			_ArrayAdd($param1, $param2)
			If @error Then
				Switch @error
					Case 1
						_fail("la valeur passée n'est pas un tableau")
					Case 2
						_fail("la valeur passée n'est pas un tableau à une Localension")
				EndSwitch
				Return False
			EndIf
			_ok()
			Return True
		Case "ArrayDelete"
			If IsBool($param2) And Not $param2 Then Return _wrongNumberOfParams()
			_ArrayDelete($param1, $param2)
			If @error Then
				Switch @error
					Case 1
						_fail("la valeur passée n'est pas un tableau")
					Case 3
						_fail("la valeur passée n'est pas un tableau à une Localension")
				EndSwitch
				Return False
			EndIf
			_ok()
			Return True
		Case Else
			_out($_ERROR, "_tryByRef: unknown function: " & $funcName)
			Return False
	EndSwitch
EndFunc   ;==>_tryByRef

Func _wrongNumberOfParams()
	_out($_ERROR, $_TOOLBOX_CALL & "fonction appelée avec un nombre incorrect de paramètres")
	Return False
EndFunc   ;==>_wrongNumberOfParams


Func _fail($msg = "erreur")
	_out($_TOOLBOX_ERROR, $_TOOLBOX_CALL & $msg)
	Return False
EndFunc   ;==>_fail

Func _ok($msg = "succès")
	_out($_DEBUG, $_TOOLBOX_CALL & $msg)
	Return True
EndFunc   ;==>_ok


