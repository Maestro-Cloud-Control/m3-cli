# Linux
### Prepare environment
```
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pip install -r requirements.txt
pip install m3-cli
```

### Build artifact
Pyinstaller detects the operation system and builds binary file on linux for different architecture respectively where it has been built amd64 or arm

To start artifact build process run:(included in the build_deb.sh)
```
python3 build.py
```

#### Check what gets included(optional)
After building, you can inspect the binary’s contents:
```
pyi-archive_viewer dist/m3
```

#### Linux installer build
To build .deb package for ubuntu or debian run `build_deb.sh` script:
```
bash build_deb.sh
```
You can find `.deb` installer in the `dist` directory.
It extracts `m3` executable binary file to the `/usr/local/bin` that is already in the system `PATH`

To install:
```
sudo dpkg -i m3_x.x.x_arch.deb
```
To check:
```
m3 health-check
```

# Windows 
### Prepare environment
```
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install pyinstaller
pip install -r requirements.txt
pip install m3-cli
```

### Build artifact
This command works the same on linux and windows machine but for windows machine it requires additional software as:
- [Visual Studio C++](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022])
- Windows SDK
- [Visual Studio build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Microsoft .NET SDK

To start artifact build process run:
```
python build.py
```
#### Installer build
To build an executable installer that allows to choose destination directory to install m3.exe and add this directory to the system `PATH` without admin permissions run `build_win_exe_setup.iss` script:
It requires [Inno Setup](https://jrsoftware.org/isinfo.php) to be installed
Open file `build_win_exe_setup.iss` with Inno Setup Compiler press F9 on keyboard or button Run in the application navigation bar or run in the `cmd`:

```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DVersion=x.x.x build_win_exe_setup.iss
```

```ps
cmd /c '"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DVersion=x.x.x build_win_exe_setup.iss'
```

You can find `m3-cli-x.x.x.exe` installer in the `Output` directory.

#### To install:
Run `m3-cli-x.x.x.exe` and click through setup wizard 
To check:
```
m3 health-check
```

# macOS
### Prepare environment
```
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pip install -r requirements.txt
pip install m3-cli
```
### Build artifact
Prerequisites
- pyinstaller (already used to generate the m3 binary)
- hdiutil (built-in on macOS)
- Optional: create-dmg for nicer layout (via brew install create-dmg)

To start artifact build process run:(included in the build_deb.sh)
```
python3 build.py
```

### Create .dmg Installer
#### Option 1: Using create-dmg
Install create-dmg via Homebrew:
```
brew install create-dmg
```
Create the DMG:
```
create-dmg 'dist/m3' \
  --volname "m3_cli" \
  --window-pos 200 120 \
  --icon-size 100 \
  --icon "m3" 100 100 \
  --app-drop-link 400 100 \
  dist/
```
This will produce something like:
`dist/m3_cli.dmg`

#### Option 2: Using hdiutil (Manual)
```
mkdir -p dist/dmg-root
cp dist/m3 dist/dmg-root/
hdiutil create -volname "m3_cli" -srcfolder dist/dmg-root -ov -format UDZO dist/m3_cli.dmg
```
#### Testing and Installing
Mount the DMG:
open `dist/m3_cli.dmg`
You can then drag m3 to /usr/local/bin or anywhere else. To make it system-wide:
```
sudo cp /Volumes/m3_cli/m3 /usr/local/bin/
```
Test it:
```
m3 health-check
```


#### TODO
 - CICD build
