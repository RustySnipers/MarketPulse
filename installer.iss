[Setup]
AppName=Market Pulse
AppVersion={#MyAppVersion}
DefaultDirName={pf}\Market Pulse
DisableProgramGroupPage=yes
DisableDirPage=yes
OutputDir=dist-installer
OutputBaseFilename=MarketPulseSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\launcher.exe"; DestDir: "{app}"; DestName: "MarketPulse.exe"; Flags: ignoreversion
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\MarketPulse.exe"; Description: "Launch Market Pulse"; Flags: nowait postinstall skipifsilent
