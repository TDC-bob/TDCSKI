#define MyAppName "TDC Skins Installer"
#define AppShortNAme "TDCSKI"
#define MyAppVersion "0.8.23.0"
#define MyAppPublisher "Bob"
#define MyAppURL "http://tdcski.daribouca.net"
#define MyAppExeName "TDC_Skin_Installer.exe"
#define MyEmail "bob@daribouca.net"
#define UpdateUrl "http://www.daribouca.net/TDC_Skin_Installer.zip"
#define Copyright "Copyright (C) 2011-2012 Bob"
#define Comments "Installation automatique des livrées des TDCs"
#define OnlineChangelog "https://sites.google.com/a/daribouca.net/tdcski/changelog"
#define BaseDir "C:\Users\Bob\Desktop\Git\TDCSKI"

[Setup]
AppId={{7B1DB1E8-C6FC-4925-975E-F745BBBB6603}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\TDCSkinsInstaller
DefaultGroupName={#MyAppName}
LicenseFile={#BaseDir}\InnoPackage\License.txt
InfoBeforeFile={#BaseDir}\InnoPackage\changelog.txt
Compression=lzma
SolidCompression=yes
AppComments={#Comments}
AppReadmeFile={#OnlineChangelog}
VersionInfoVersion={#MyAppVersion}
ShowTasksTreeLines=yes
DisableProgramGroupPage=yes
OutputBaseFilename=Setup_TDCSKI_v{#MyAppVersion}
OutputDir={#BaseDir}\InnoBuild
AppCopyright={#Copyright}
;SignTool=kSign /d $qTDC Skins Installer$q /du $qhttp://tdcski.daribouca.net$q $f
AlwaysShowGroupOnReadyPage=yes
AlwaysShowDirOnReadyPage=yes
AllowUNCPath=no
AlwaysUsePersonalGroup=yes
AppContact={#MyEmail}
BackColor=clWhite
;BackColor2=clGrey
BackSolid=yes
ExtraDiskSpaceRequired=10485760
;ArchitecturesInstallIn64BitMode=x64


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Messages]
SetupAppTitle = Setup {#AppShortNAme}
SetupWindowTitle = Setup {#MyAppName} v{#MyAppVersion}
AboutSetupMessage = {#AppShortNAme} setup
french.SetupAppTitle = Installation de {#AppShortNAme}
french.SetupWindowTitle = Installation de {#MyAppName} v{#MyAppVersion}
french.AboutSetupMessage = Installation de {#AppShortNAme}


[CustomMessages]
CreateStartMenuIcon=Create a shortcut in the &start menu
french.CreateStartMenuIcon=Créer un raccourci dans le &menu démarrer

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce  
Name: "startmenuicon"; Description: "{cm:CreateStartMenuIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce; OnlyBelowVersion: 0,6.1

[Files]
Source: "{#BaseDir}\InnoPackage\TDC_Skin_Installer.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: not Is64BitInstallMode
Source: "{#BaseDir}\InnoPackage\changelog.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#BaseDir}\InnoPackage\License.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#BaseDir}\InnoPackage\Readme.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#BaseDir}\InnoPackage\Mettre en ligne une livrée ou une mission.url"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#BaseDir}\InnoPackage\source\*"; DestDir: "{app}\source"; Flags: ignoreversion
Source: "{#BaseDir}\ressources\7zip\*"; DestDir: "{app}\7zip"; Flags: ignoreversion
Source: "{#BaseDir}\ressources\logoTDC.jpg"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#BaseDir}\ressources\TDCSKI.ico"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Mettre en ligne une livrée ou une mission.url"; Filename: "{app}\Mettre en ligne une livrée ou une mission.url"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Registry]
Root: HKLM; Subkey: "SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{{7B1DB1E8-C6FC-4925-975E-F745BBBB6603}_is1"; Flags: uninsdeletekey createvalueifdoesntexist
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{7B1DB1E8-C6FC-4925-975E-F745BBBB6603}_is1"; Flags: uninsdeletekey createvalueifdoesntexist

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall

[UninstallDelete]
Type: files; Name: "{app}\log.log"           
Type: dirifempty; Name: "{app}"





                                                                      

