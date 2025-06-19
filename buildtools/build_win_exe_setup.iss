; Inno Setup Script for m3.exe
; Created for user-specific installation with PATH update

#define AppName "m3-cli"
#define AppVersion "0.0.0"
#ifdef Version
  #define AppVersion Version
#endif

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={userappdata}\Programs\m3-cli
DisableProgramGroupPage=yes
OutputBaseFilename={#AppName}-{#AppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "..\dist\m3.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; Add to user PATH if not already present
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; \
    ValueData: "{code:GetUpdatedPath}"; Check: NeedsPathUpdate

[Code]
function GetUserPath(): string;
begin
  RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', Result);
end;

function PathContainsM3(Path: string): boolean;
begin
  Result := Pos(ExpandConstant('{app}'), Path) > 0;
end;

function GetUpdatedPath(Param: string): string;
var
  CurrentPath: string;
begin
  CurrentPath := GetUserPath();
  if not PathContainsM3(CurrentPath) then
    Result := CurrentPath + ';' + ExpandConstant('{app}')
  else
    Result := CurrentPath;
end;

function NeedsPathUpdate(): boolean;
begin
  Result := not PathContainsM3(GetUserPath());
end;
