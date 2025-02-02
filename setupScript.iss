; Steven's Script to Create Installer for Gregg's Flow Sheet Generator
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; Basic setup information
AppName=Gregg's Flow Sheet Generator
AppVersion=0.2.0
DefaultDirName={userappdata}\GFS Gen
DefaultGroupName=GFS Gen
DisableProgramGroupPage=yes
OutputDir=C:\Users\Olsens\Downloads\GFS-Gen-main\GFS-Gen-main\dist
OutputBaseFilename=Setup_GFS_Gen
SetupIconFile=C:\Users\Olsens\Downloads\GFS-Gen-main\GFS-Gen-main\dist\icon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
; Files to install
Source: "C:\Users\Olsens\Downloads\GFS-Gen-main\GFS-Gen-main\dist\Greggs Flow Sheet Generator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Olsens\Downloads\GFS-Gen-main\GFS-Gen-main\dist\13template.xlsx"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Olsens\Downloads\GFS-Gen-main\GFS-Gen-main\dist\24template.xlsx"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Olsens\Downloads\GFS-Gen-main\GFS-Gen-main\dist\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create desktop shortcut
Name: "{userdesktop}\GFS Gen"; Filename: "{app}\Greggs Flow Sheet Generator.exe"; IconFilename: "{app}\icon.ico"

[Run]
; Run application after installation (optional, can be removed if not needed)
Filename: "{app}\Greggs Flow Sheet Generator.exe"; Description: "Launch Gregg's Flow Sheet Generator"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
