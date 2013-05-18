#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)


Global Const $_GOOGLE_DNS_IP = "8.8.8.8"
Global Const $_PING_DEFAULT_TIMEOUT = 2500

Func _checkConnection()
	local $respond_time
	_out($_INFO, "V�rification de la connexion � internet", 1)
	_out($_INFO, "Ping du serveur DNS de Google ... ")
	$respond_time = _try("Ping", $_GOOGLE_DNS_IP, "Ping du serveur DNS de Google", False)
	if not $respond_time then _out(BitOR($_OUT_EXT, $_OUT_MSG), "Je ne suis pas parvenu � pinger le serveur DNS de Google. V�rifiez votre connexion internet et recommencez")
	_out($_RESULT, "le serveur � r�pondu apr�s " & $respond_time & " millisecondes")
	_out($_INFO, "Ping du serveur Dropbox ... ")
	$respond_time = _try("Ping", $_HTTP_DROPBOX, "Ping du serveur Dropbox", False)
	if not $respond_time then _out(BitOR($_OUT_EXT, $_OUT_MSG), "Je ne suis pas parvenu � pinger le serveur HTTP de DropBox. DropBox est peut-�tre injoignable actuellement ? R�essayez plus tard ...")
	_out($_RESULT, "le serveur � r�pondu apr�s " & $respond_time & " millisecondes")
	_out($_INFO, "Connexion internet v�rifi�e", -1)
EndFunc   ;==>_checkConnection
