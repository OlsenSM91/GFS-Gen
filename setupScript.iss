; Steven's Script to Create Installer for Gregg's Flow Sheet Generator
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; Basic setup information
AppName=Gregg's Flow Sheet Generator
AppVersion=0.1.0
DefaultDirName={userappdata}\GFS Gen
DefaultGroupName=GFS Gen
DisableProgramGroupPage=yes
OutputDir=C:\Users\Steven\Downloads\GreggApp\build\dist
OutputBaseFilename=Setup_GFS_Gen
SetupIconFile=C:\Users\Steven\Downloads\GreggApp\build\dist\icon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
; Files to install
Source: "C:\Users\Steven\Downloads\GreggApp\build\dist\Greggs Flow Sheet Generator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Steven\Downloads\GreggApp\build\dist\template.xlsx"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Steven\Downloads\GreggApp\build\dist\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

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
