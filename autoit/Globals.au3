#NoTrayIcon
#include-once

Global $first_start = false

Global Const $Python33_x86_download_link = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.msi"
Global Const $Python33_x64_download_link = "http://www.python.org/ftp/python/3.3.2/python-3.3.2.amd64.msi"
Global Const $PortableGit_download_link = "https://msysgit.googlecode.com/files/PortableGit-1.8.3-preview20130601.7z"

Global Const $repo = @ScriptDir & "\tdcski"
Global Const $repo_remote = "https://github.com/TDC-bob/TDCSKI.git"

Global Const $updater_path = $repo & "\updater.exe"
Global Const $new_version_path = $repo & "\tdcski.exe"

Global Const $log_dir = @ScriptDir & "\logs"
Global Const $log_file = $log_dir & "\" & @YEAR & @MON & @MDAY & " - " & @HOUR & "h" & @MIN & "m" & @SEC & " - Lanceur.log"
Global $iMemo, $python_path, $git_path, $gui_handle

Global Const $config_file = @ScriptDir & "\tdcski.cfg"

Global $portable_git_folder = @ScriptDir & "\portable-git"

#include "strings.au3"