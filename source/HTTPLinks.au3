#NoTrayIcon
#include-once
AutoItSetOption("MustDeclareVars", 1)

Global $_HTTP_ROOT = "http://users.skynet.be/fd200121/"

Global Const $_HTTP_VERSION_FILE 			= $_HTTP_ROOT & $_APP_ONLINE_VERSION_FILE
Global Const $_HTTP_SETUP_FILE 				= $_HTTP_ROOT & $_APP_ONLINE_SETUP_FILE

Global Const $_HTTP_VERSION_FILE_ALPHA	 	= $_HTTP_ROOT & "ALPHA/" & $_APP_ONLINE_VERSION_FILE
Global Const $_HTTP_SETUP_FILE_ALPHA		= $_HTTP_ROOT & "ALPHA/" & $_APP_ONLINE_SETUP_FILE

Global Const $_HTTP_DROPBOX					= "www.dropbox.com"