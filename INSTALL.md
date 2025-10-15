# Installation Guide

Detailed installation instructions for HRaJi Screen Recorder on different platforms.

## Table of Contents

- [Linux Installation](#linux-installation)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Docker Installation](#docker-installation)
- [Troubleshooting](#troubleshooting)

---

## Linux Installation

### Ubuntu/Debian

#### 1. Install Python and Dependencies

```bash
# Update package list
sudo apt update

# Install Python 3.8 or higher
sudo apt install python3 python3-pip python3-venv

# Install system dependencies for OpenCV
sudo apt install python3-dev libgl1-mesa-glx libglib2.0-0

# Install X11 utilities (for fullscreen tracking)
sudo apt install x11-utils

# Install tkinter (if not already included)
sudo apt install python3-tk
```

#### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/screen-recorder.git
cd screen-recorder

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python screen_recorder.py
```

### Fedora/RHEL/CentOS

```bash
# Install Python
sudo dnf install python3 python3-pip python3-tkinter

# Install system dependencies
sudo dnf install mesa-libGL glib2

# Install X11 utilities
sudo dnf install xorg-x11-utils

# Follow steps 2 from Ubuntu section above
```

### Arch Linux

```bash
# Install Python and dependencies
sudo pacman -S python python-pip tk

# Install system dependencies
sudo pacman -S mesa glib2 xorg-xprop xorg-xwininfo

# Follow steps 2 from Ubuntu section above
```

### Permission Issues

If you encounter permission errors:

```bash
# Grant accessibility permissions
# Add your user to video group (if needed)
sudo usermod -aG video $USER

# Log out and log back in for changes to take effect
```

---

## Windows Installation

### Prerequisites

1. **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Check "Install pip"

### Installation Steps

#### Using PowerShell

```powershell
# Check Python installation
python --version

# Clone repository (requires Git)
git clone https://github.com/yourusername/screen-recorder.git
cd screen-recorder

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If execution policy error occurs:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Run application
python screen_recorder.py
```

#### Using Command Prompt (cmd)

```cmd
# Check Python installation
python --version

# Clone repository
git clone https://github.com/yourusername/screen-recorder.git
cd screen-recorder

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run application
python screen_recorder.py
```

### Without Git

1. Download ZIP from GitHub
2. Extract to desired location
3. Open PowerShell/CMD in that folder
4. Follow steps from "Create virtual environment" onward

### Common Issues

#### Global Hotkeys Not Working
- Run as Administrator
- Grant accessibility permissions in Windows Security

#### OpenCV Import Errors
```powershell
# Uninstall and reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python-headless
```

---

## macOS Installation

### Prerequisites

1. **Homebrew**: Install from [brew.sh](https://brew.sh/)
2. **Python 3.8+**: Usually pre-installed, or install via Homebrew

### Installation Steps

```bash
# Install Python if needed
brew install python@3.11

# Verify installation
python3 --version

# Clone repository
git clone https://github.com/yourusername/screen-recorder.git
cd screen-recorder

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python screen_recorder.py
```

### Grant Permissions

On first run, macOS will request permissions:

1. **Screen Recording Permission**:
   - System Preferences → Security & Privacy → Privacy
   - Select "Screen Recording"
   - Enable for Terminal or your Python IDE

2. **Accessibility Permission** (for hotkeys):
   - System Preferences → Security & Privacy → Privacy
   - Select "Accessibility"
   - Add Terminal or Python

### Apple Silicon (M1/M2) Notes

```bash
# If you encounter architecture issues:
# Install Rosetta 2 if not already installed
softwareupdate --install-rosetta

# Use x86_64 Python
arch -x86_64 /usr/bin/python3 -m venv venv
```

---

## Docker Installation

### Using Docker

```bash
# Note: GUI applications in Docker require X11 forwarding
# This is more complex and primarily for development/testing

# Build Docker image
docker build -t screen-recorder .

# Run with X11 forwarding (Linux)
xhost +local:docker
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/recordings:/recordings \
    screen-recorder
```

### Dockerfile Example

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY screen_recorder.py .
COPY sc_icon.png .

# Run application
CMD ["python", "screen_recorder.py"]
```

---

## Virtual Environment Setup

### Why Use Virtual Environment?

- Isolates project dependencies
- Prevents version conflicts
- Easy to remove (just delete folder)
- Reproducible environment

### Creating Virtual Environment

```bash
# Using venv (built-in)
python -m venv venv

# Using virtualenv (more features)
pip install virtualenv
virtualenv venv

# Using conda
conda create -n screen-recorder python=3.11
conda activate screen-recorder
```

### Activating Virtual Environment

| Platform | Command |
|----------|---------|
| Linux/macOS | `source venv/bin/activate` |
| Windows (cmd) | `venv\Scripts\activate.bat` |
| Windows (PowerShell) | `.\venv\Scripts\Activate.ps1` |
| Fish shell | `source venv/bin/activate.fish` |

### Deactivating

```bash
deactivate
```

---

## Troubleshooting

### Import Errors

```bash
# Problem: ModuleNotFoundError
pip list  # Check installed packages
pip install -r requirements.txt  # Reinstall

# Problem: Wrong Python version
python --version  # Check version
python3 --version  # Try python3 command
```

### Permission Denied

```bash
# Linux: Screen capture permissions
# Add user to video group
sudo usermod -aG video $USER

# Windows: Run as Administrator
# Right-click → Run as administrator

# macOS: Grant screen recording permission
# System Preferences → Security & Privacy
```

### Display Issues

```bash
# Linux: X11 not found
echo $DISPLAY  # Should show :0 or similar
export DISPLAY=:0  # Set if empty

# Linux: Wayland issues
# Switch to X11 session (at login screen)
echo $XDG_SESSION_TYPE  # Check current session
```

### Performance Issues

```bash
# Reduce capture area size
# Disable cursor tracking
# Disable click visualization
# Close background applications
# Use SSD for output location
```

### Dependencies Won't Install

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -v opencv-python

# Try alternative packages
pip install opencv-python-headless

# Check for system libraries
ldconfig -p | grep libGL  # Linux
```

---

## Verifying Installation

Test your installation:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Check Python version
python --version

# Check installed packages
pip list | grep mss
pip list | grep opencv
pip list | grep numpy
pip list | grep pynput

# Import test
python -c "import mss, cv2, numpy, pynput; print('All imports successful!')"

# Run application
python screen_recorder.py
```

---

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
rm -rf screen-recorder

# Remove any recordings (if needed)
rm -rf ~/recordings/*.mp4
```

---

## Updating

```bash
# Navigate to project directory
cd screen-recorder

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run application
python screen_recorder.py
```

---

## Getting Help

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/yourusername/screen-recorder/issues)
2. Read [Troubleshooting Section](README.md#troubleshooting) in README
3. Search [GitHub Discussions](https://github.com/yourusername/screen-recorder/discussions)
4. Create a new issue with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

---

## Next Steps

After successful installation:

1. Read the [Usage Guide](README.md#usage)
2. Try [Basic Recording](README.md#basic-recording)
3. Explore [Advanced Features](README.md#advanced-features)
4. Customize [Configuration](README.md#configuration)
