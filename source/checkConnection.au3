#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)


Global Const $_GOOGLE_DNS_IP = "8.8.8.8"
Global Const $_PING_DEFAULT_TIMEOUT = 2500

Func _checkConnection()
	local $respond_time
	_out($_INFO, "Vérification de la connexion à internet", 1)
	_out($_INFO, "Ping du serveur DNS de Google ... ")
	$respond_time = _try("Ping", $_GOOGLE_DNS_IP, "Ping du serveur DNS de Google", False)
	if not $respond_time then _out(BitOR($_OUT_EXT, $_OUT_MSG), "Je ne suis pas parvenu à pinger le serveur DNS de Google. Vérifiez votre connexion internet et recommencez")
	_out($_RESULT, "le serveur à répondu après " & $respond_time & " millisecondes")
	_out($_INFO, "Ping du serveur Dropbox ... ")
	$respond_time = _try("Ping", $_HTTP_DROPBOX, "Ping du serveur Dropbox", False)
	if not $respond_time then _out(BitOR($_OUT_EXT, $_OUT_MSG), "Je ne suis pas parvenu à pinger le serveur HTTP de DropBox. DropBox est peut-être injoignable actuellement ? Réessayez plus tard ...")
	_out($_RESULT, "le serveur à répondu après " & $respond_time & " millisecondes")
	_out($_INFO, "Connexion internet vérifiée", -1)
EndFunc   ;==>_checkConnection
