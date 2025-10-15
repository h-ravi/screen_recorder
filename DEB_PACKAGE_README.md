# HRaJi Screen Recorder - Debian Package Guide

यह गाइड आपको HRaJi Screen Recorder को .deb package में convert करने और install/uninstall करने की पूरी जानकारी देती है।

## 📦 Package Features (पैकेज की विशेषताएं)

### Installation के दौरान:
1. ✅ **System Dependencies Check**: Installation से पहले सभी जरूरी system-level packages की जांच करता है
2. ✅ **User Notification**: अगर कोई dependency missing है (जैसे python3-tk), तो user को install करने के लिए clear instruction देता है
3. ✅ **Python Virtual Environment**: Automatically एक isolated Python environment create करता है
4. ✅ **Package Installation**: सभी Python packages (mss, opencv-python, numpy, pynput) virtual environment में install करता है
5. ✅ **Desktop Entry**: Application menu में shortcut बनाता है
6. ✅ **Command-line Access**: Terminal से `hraji-screen-recorder` command से run कर सकते हैं

### Uninstallation के दौरान:
1. ✅ **Complete Cleanup**: Application और उसके सभी files को remove करता है
2. ✅ **Virtual Environment Removal**: अपने द्वारा बनाया गया Python environment पूरी तरह delete कर देता है
3. ✅ **No Leftovers**: कोई भी leftover files नहीं छोड़ता

## 🚀 .deb Package बनाने के Steps

### Step 1: Prerequisites Install करें

```bash
# dpkg-deb tool के लिए
sudo apt-get update
sudo apt-get install dpkg-dev
```

### Step 2: Build Script को Executable बनाएं

```bash
chmod +x build-deb.sh
chmod +x debian_scripts/postinst
chmod +x debian_scripts/prerm
chmod +x debian_scripts/postrm
```

### Step 3: .deb Package Build करें

```bash
./build-deb.sh
```

यह command एक `.deb` file create करेगी: `hraji-screen-recorder_1.0.0_amd64.deb`

## 📥 Package Install करना

### Method 1: dpkg का उपयोग करें

```bash
sudo dpkg -i hraji-screen-recorder_1.0.0_amd64.deb
```

अगर dependencies missing हैं, तो आपको error मिलेगी:

```
❌ ERROR: Missing required system dependencies!

Please install the following packages first:
  sudo apt-get install python3-tk ffmpeg
```

Dependencies install करें:

```bash
sudo apt-get install python3-tk python3-venv python3-pip ffmpeg
```

फिर package को reconfigure करें:

```bash
sudo dpkg --configure hraji-screen-recorder
```

### Method 2: apt का उपयोग करें (Automatic Dependency Resolution)

```bash
sudo apt-get install ./hraji-screen-recorder_1.0.0_amd64.deb
```

यह automatically सभी dependencies को install कर देगा।

## 🎯 Application को Run करना

### Terminal से:

```bash
hraji-screen-recorder
```

### Application Menu से:

"HRaJi Screen Recorder" को search करें और click करें।

## 🗑️ Uninstallation

### पूर्ण रूप से Remove करने के लिए (Recommended):

```bash
sudo apt-get purge hraji-screen-recorder
```

यह command:
- Application को uninstall करेगी
- Virtual environment को delete करेगी
- सभी configuration files को remove करेगी
- Desktop entries को साफ करेगी

### केवल Application Remove करने के लिए:

```bash
sudo apt-get remove hraji-screen-recorder
```

## 📋 Package Details देखना

### Package में क्या है देखें:

```bash
dpkg -c hraji-screen-recorder_1.0.0_amd64.deb
```

### Package Information देखें:

```bash
dpkg -I hraji-screen-recorder_1.0.0_amd64.deb
```

### Installed Package की Status देखें:

```bash
dpkg -s hraji-screen-recorder
```

## 🔍 Package Structure

```
debian/
├── DEBIAN/
│   ├── control          # Package metadata
│   ├── postinst         # Installation script
│   ├── prerm            # Pre-removal script
│   └── postrm           # Post-removal script
├── opt/
│   └── hraji-screen-recorder/
│       ├── screen_recorder.py
│       ├── requirements.txt
│       └── icon.png
└── usr/
    └── share/
        ├── applications/
        │   └── hraji-screen-recorder.desktop
        └── doc/
            └── hraji-screen-recorder/
                ├── README.md
                ├── LICENSE
                └── copyright
```

## 🛠️ Installation Process Details

### 1. System Dependencies Check (postinst script):
```bash
- python3 (>= 3.8)
- python3-venv
- python3-pip
- python3-tk
- ffmpeg
```

### 2. Virtual Environment Creation:
```bash
Location: /opt/hraji-screen-recorder/venv
Python version: Same as system Python3
Isolated: Yes (packages केवल इस environment में install होते हैं)
```

### 3. Python Packages Installation:
```bash
- mss>=9.0.1
- numpy>=1.24.0
- opencv-python>=4.8.0
- pynput>=1.7.6
```

### 4. Shortcuts Creation:
```bash
Command-line: /usr/local/bin/hraji-screen-recorder
Desktop Entry: /usr/share/applications/hraji-screen-recorder.desktop
```

## 🐛 Troubleshooting

### Problem: "Missing required system dependencies" Error

**Solution:**
```bash
sudo apt-get install python3-tk python3-venv python3-pip ffmpeg
sudo dpkg --configure hraji-screen-recorder
```

### Problem: Package Installation Fails

**Solution:**
```bash
# पुराना package पूरी तरह remove करें
sudo apt-get purge hraji-screen-recorder

# Dependencies install करें
sudo apt-get install -f

# फिर से install करें
sudo apt-get install ./hraji-screen-recorder_1.0.0_amd64.deb
```

### Problem: Application Run नहीं हो रहा

**Solution:**
```bash
# Launcher script check करें
ls -la /opt/hraji-screen-recorder/launcher.sh

# Manually run करें
/opt/hraji-screen-recorder/launcher.sh

# Logs check करें
journalctl -xe | grep hraji
```

### Problem: Virtual Environment Corrupt हो गया

**Solution:**
```bash
# Package को reinstall करें
sudo apt-get install --reinstall hraji-screen-recorder
```

## 📝 Customization

### Package Metadata बदलना:

`build-deb.sh` में control section को edit करें:

```bash
Package: hraji-screen-recorder
Version: 1.0.0
Maintainer: Your Name <your-email@example.com>
Description: Your custom description
```

### Icon बदलना:

`icon.png` file को project root में add करें, build script automatically उसे include कर देगी।

## 🎉 Success Messages

Installation के बाद आपको यह message दिखेगा:

```
======================================
 Installation completed successfully! 
======================================

You can now run the application by:
  1. Typing 'hraji-screen-recorder' in terminal
  2. Searching 'HRaJi Screen Recorder' in your application menu

Virtual environment location: /opt/hraji-screen-recorder/venv
```

Uninstallation के बाद:

```
======================================
 Uninstallation completed!            
======================================

Thank you for using HRaJi Screen Recorder!
```

## 📚 Additional Commands

### Package को upgrade करना:

```bash
sudo apt-get install --only-upgrade hraji-screen-recorder
```

### Package को hold करना (updates से protect):

```bash
sudo apt-mark hold hraji-screen-recorder
```

### Hold को remove करना:

```bash
sudo apt-mark unhold hraji-screen-recorder
```

---

## 🤝 Support

अगर कोई problem आए या question हो, तो:
1. DEB_PACKAGE_README.md को ध्यान से पढ़ें
2. Troubleshooting section देखें
3. GitHub issues में report करें

---

**Happy Recording! 🎥**
