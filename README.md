# HRaJi Screen Recorder 🎥

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

A powerful, feature-rich screen recording application built with Python. Record your screen with advanced features like pause/resume, custom area selection, cursor tracking, click visualization, and real-time performance statistics.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Keyboard Shortcuts](#-keyboard-shortcuts) • [Advanced Features](#-advanced-features) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Quick Install](#quick-install)
  - [Manual Installation](#manual-installation)
- [Usage](#-usage)
  - [Basic Recording](#basic-recording)
  - [Recording Modes](#recording-modes)
  - [Output Configuration](#output-configuration)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Advanced Features](#-advanced-features)
  - [Custom Area Selection](#custom-area-selection)
  - [Cursor and Click Visualization](#cursor-and-click-visualization)
  - [Live Performance Statistics](#live-performance-statistics)
  - [Follow Fullscreen Window](#follow-fullscreen-window)
  - [Capture Border Overlay](#capture-border-overlay)
- [Configuration](#-configuration)
- [Technical Details](#-technical-details)
  - [Architecture](#architecture)
  - [Video Encoding](#video-encoding)
  - [Frame Rate Management](#frame-rate-management)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## ✨ Features

### Core Recording Features
- **🎬 High-Quality Screen Capture**: Records at 30 FPS with configurable resolution
- **⏸️ Pause & Resume**: Seamlessly pause and resume recordings without creating separate files
- **🎯 Custom Area Selection**: Draw to select specific screen regions for recording
- **📐 Aspect Ratio Presets**: Support for Full Screen, 16:9, 9:16, and 4:3 ratios
- **🖱️ Cursor Tracking**: Optional cursor overlay with visual feedback
- **👆 Click Visualization**: Animated ripple effects for mouse clicks (left/right differentiation)

### Advanced Capabilities
- **📊 Real-Time Statistics**: Live FPS monitoring, frame counting, and performance metrics
- **🖼️ Visual Border Overlay**: Configurable colored border around capture area
- **⏱️ Countdown Timer**: Configurable countdown before recording starts (0-10 seconds)
- **🪟 Floating Mini Controller**: Draggable mini window for recording controls
- **🔄 Follow Fullscreen Mode**: Automatically tracks fullscreen windows (Linux X11)
- **⌨️ Global Hotkeys**: Control recording from anywhere in your system

### User Experience
- **🎨 Modern GUI**: Clean, intuitive interface built with tkinter
- **💾 Flexible Output**: Customizable save location and filename templates
- **📁 Smart File Naming**: Support for timestamp-based filenames using strftime format
- **🔒 Safe Close Protection**: Warns before closing during active recording
- **🎯 Precise Frame Scheduling**: Constant frame rate (CFR) encoding for smooth playback

---

## 📸 Screenshots

### Main Application Window
The main control interface provides easy access to all recording features:
- Aspect ratio selection
- Output configuration
- Recording controls
- Live status display

### Mini Controller Window
A floating, draggable mini window that provides:
- Real-time elapsed timer
- Quick pause/resume/stop controls
- Stays on top of other windows
- Minimal screen footprint

### Recording with Visual Overlays
- Red border showing capture area
- Cursor visualization with yellow highlight
- Click ripple effects (red for right-click, blue for left-click)
- Real-time performance statistics overlay

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Linux, Windows, or macOS
- **Display Server** (Linux): X11 required for fullscreen window tracking

### Quick Install

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/screen-recorder.git
cd screen-recorder
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python screen_recorder.py
```

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install mss>=9.0.1
pip install numpy>=1.24.0
pip install opencv-python>=4.8.0
pip install pynput>=1.7.6
```

### Platform-Specific Notes

#### Linux
- For global hotkeys and mouse tracking, ensure X11 is running
- Some distributions may require additional permissions for screen capture
- Install `xprop` and `xwininfo` for fullscreen window tracking:
  ```bash
  sudo apt-get install x11-utils  # Debian/Ubuntu
  sudo dnf install xorg-x11-utils # Fedora
  ```

#### Windows
- Administrator privileges may be required for global hotkeys
- Windows Defender might flag the application; add it to exclusions if needed

#### macOS
- Grant accessibility permissions when prompted
- System Preferences → Security & Privacy → Accessibility

---

## 📖 Usage

### Basic Recording

1. **Launch the application**:
   ```bash
   python screen_recorder.py
   ```

2. **Configure your recording**:
   - Select aspect ratio (Full Screen, 16:9, 9:16, or 4:3)
   - Choose save location
   - Set filename template

3. **Start recording**:
   - Click the **Start** button
   - Wait for countdown (if enabled)
   - Recording begins automatically

4. **Control recording**:
   - **Pause**: Temporarily stop recording
   - **Resume**: Continue recording after pause
   - **Stop**: Finalize and save the recording

### Recording Modes

#### Full Screen Recording
```
1. Select "Full Screen" from Aspect Ratio dropdown
2. Click Start
3. Entire primary monitor is recorded
```

#### Custom Aspect Ratio
```
1. Select desired ratio (16:9, 9:16, or 4:3)
2. Recording area is centered on screen
3. Maintains aspect ratio at maximum size
```

#### Custom Area Selection
```
1. Click "Select Area..." button
2. Screen dims with selection overlay
3. Click and drag to select region
4. Release to confirm selection
```

### Output Configuration

#### Save Location
- Click **Browse...** to select output directory
- Defaults to current working directory
- Automatically creates directory if it doesn't exist

#### Filename Template
Supports Python's `strftime` format codes:
```python
# Examples:
"recording_%Y-%m-%d_%H-%M-%S.mp4"  # recording_2025-10-15_14-30-45.mp4
"HRaJi_%d-%b-%Y.mp4"                # HRaJi_15-Oct-2025.mp4
"video_%H%M%S.mp4"                  # video_143045.mp4
```

Common format codes:
- `%Y` - Year (2025)
- `%m` - Month (01-12)
- `%d` - Day (01-31)
- `%H` - Hour (00-23)
- `%M` - Minute (00-59)
- `%S` - Second (00-59)
- `%b` - Month name (Oct)

---

## ⌨️ Keyboard Shortcuts

Global hotkeys work even when the application is not in focus:

| Shortcut | Action |
|----------|--------|
| `Alt + Shift + S` | **Start/Stop** recording |
| `Alt + Shift + P` | **Pause** recording |
| `Alt + Shift + R` | **Resume** recording |

> **Note**: Global hotkeys require the `pynput` library. If not available, use on-screen buttons.

---

## 🔧 Advanced Features

### Custom Area Selection

Select any rectangular region of your screen:

1. Click **"Select Area..."** button
2. Screen darkens with transparent overlay
3. Click and drag to create selection rectangle
4. Red outline shows selected area in real-time
5. Release mouse to confirm

**Features**:
- Real-time preview of selection
- Automatic dimension alignment (even pixel counts)
- Minimum size: 4x4 pixels
- Works across entire primary monitor

### Cursor and Click Visualization

#### Cursor Overlay
- **Yellow dot**: Current cursor position
- **Yellow circle**: Outer ring for visibility
- Tracks mouse movement in real-time
- Toggle with "Show cursor" checkbox

#### Click Visualization
- **Blue ripples**: Left mouse clicks
- **Red ripples**: Right mouse clicks
- **Animated expansion**: 0.6-second fade effect
- **Radius growth**: 10px → 70px
- Toggle with "Show clicks" checkbox

**Use Cases**:
- Tutorial videos
- Software demonstrations
- UI/UX testing recordings
- Bug reproduction videos

### Live Performance Statistics

Monitor recording performance in real-time:

#### Statistics Displayed
- **Capture FPS**: Frames captured per second
- **Written FPS**: Frames written to video file
- **Duplicate frames/s**: Frame duplication rate

#### Configuration Options
- **Opacity**: 0.2 to 1.0 (controls transparency)
- **Font Size**: 8 to 24 pixels
- **Window Size**: Custom width (140-600px) and height (40-400px)
- **Position**: Top-Left, Top-Right, Bottom-Left, Bottom-Right

#### Position Reference
```
┌─────────────────────┐
│ TL          TR      │
│                     │
│                     │
│ BL          BR      │
└─────────────────────┘
```

### Follow Fullscreen Window

Automatically tracks fullscreen applications (Linux X11 only):

**How it works**:
1. Enable "Follow Full Screen" checkbox
2. Start recording
3. System detects active fullscreen window
4. Capture area updates automatically
5. Handles resolution changes dynamically

**Requirements**:
- Linux with X11 display server
- `xprop` utility installed
- `xwininfo` utility installed

**Supported Scenarios**:
- Fullscreen games
- Video players
- Presentation software
- Browser fullscreen mode

### Capture Border Overlay

Visual indicator of recording area:

**Features**:
- **Color**: Red (#ff3b30)
- **Thickness**: 3 pixels
- **Opacity**: 90%
- **Always on top**: Visible over all windows
- **Toggle**: "Show Capture Border" checkbox

**Border Components**:
- Top edge overlay
- Bottom edge overlay
- Left edge overlay
- Right edge overlay

---

## ⚙️ Configuration

### Recording Settings

| Setting | Default | Range/Options | Description |
|---------|---------|---------------|-------------|
| Frame Rate | 30 FPS | Fixed | Target frames per second |
| Countdown | 3 seconds | 0-10 seconds | Delay before recording starts |
| Codec | MP4V | Fixed | Video codec (MPEG-4) |
| Aspect Ratio | Full Screen | Full/16:9/9:16/4:3 | Screen capture dimensions |

### Visual Overlays

| Setting | Default | Options | Description |
|---------|---------|---------|-------------|
| Show Cursor | Enabled | On/Off | Display cursor in recording |
| Show Clicks | Enabled | On/Off | Visualize mouse clicks |
| Show Border | Enabled | On/Off | Capture area border |
| Show Stats | Disabled | On/Off | Performance statistics |

### Output Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Save Directory | Current Dir | Output folder for recordings |
| Filename Template | HRaJi.mp4 | Filename pattern with strftime support |

---

## 🔬 Technical Details

### Architecture

The application follows a modular architecture:

```
┌──────────────────────────────────────────┐
│         Main Application (Tk)            │
├──────────────────────────────────────────┤
│  GUI Layer (tkinter + ttk)               │
│  - Control Interface                     │
│  - Settings Management                   │
│  - Status Display                        │
├──────────────────────────────────────────┤
│  Recording Engine (Threading)            │
│  - Screen Capture (MSS)                  │
│  - Frame Processing (NumPy)              │
│  - Video Writing (OpenCV)                │
├──────────────────────────────────────────┤
│  Input Handlers                          │
│  - Global Hotkeys (pynput.keyboard)      │
│  - Mouse Tracking (pynput.mouse)         │
├──────────────────────────────────────────┤
│  Overlay System                          │
│  - Border Windows (tkinter Toplevel)     │
│  - Stats Display (tkinter Toplevel)      │
│  - Mini Controller (tkinter Toplevel)    │
└──────────────────────────────────────────┘
```

### Video Encoding

**Codec Details**:
- **Codec**: MPEG-4 Part 2 (FourCC: MP4V)
- **Container**: MP4
- **Frame Rate**: Constant 30 FPS
- **Color Space**: BGR (24-bit)
- **Compression**: Lossy (quality depends on codec implementation)

**Frame Flow**:
```
Screen Capture (BGRA)
    ↓
Color Conversion (BGR)
    ↓
Overlay Rendering (Cursor/Clicks)
    ↓
Frame Resize (if needed)
    ↓
Video Writer (MP4V)
    ↓
Output File (.mp4)
```

### Frame Rate Management

The application uses sophisticated frame scheduling to maintain constant frame rate:

#### CFR (Constant Frame Rate) Implementation
```python
target_fps = 30.0
frame_interval = 1.0 / 30.0  # 0.0333 seconds

1. Calculate next frame time
2. Capture screen when due
3. Write frame to video
4. Duplicate frames if capture is slow
5. Skip frames if capture is fast
```

#### Pause/Resume Handling
- Timer pauses: Accumulates elapsed time
- Frame schedule: Shifts by pause duration
- Video timeline: Remains contiguous
- No frame loss: Last frame duplicated during pause

#### Performance Optimization
- **Capture Rate**: Adaptive based on system load
- **Write Rate**: Matches target FPS via duplication
- **Frame Duplication**: Maintains smooth playback
- **Sleep Timing**: 0.02s intervals to reduce CPU usage

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Failed to create video writer" Error

**Causes**:
- Missing OpenCV codecs
- Invalid output path
- Permission denied

**Solutions**:
```bash
# Reinstall OpenCV with full codec support
pip uninstall opencv-python
pip install opencv-python-headless

# Check output directory permissions
chmod 755 /path/to/output/directory

# Try different filename (avoid special characters)
```

#### 2. Global Hotkeys Not Working

**Causes**:
- `pynput` not installed
- Insufficient permissions
- Wayland display server (Linux)

**Solutions**:
```bash
# Install pynput
pip install pynput

# Linux: Use X11 instead of Wayland
# Check display server:
echo $XDG_SESSION_TYPE

# Grant accessibility permissions (macOS)
# System Preferences → Security → Accessibility
```

#### 3. Low Frame Rate / Choppy Recording

**Causes**:
- High resolution capture area
- CPU/GPU overload
- Insufficient system resources

**Solutions**:
- Reduce capture area size
- Close unnecessary applications
- Use aspect ratio presets instead of full screen
- Disable cursor/click visualization
- Disable stats overlay

#### 4. Cursor Not Appearing in Recording

**Checks**:
- ✅ "Show cursor" checkbox enabled
- ✅ `pynput` library installed
- ✅ Cursor within capture area
- ✅ Not using Wayland (Linux)

#### 5. Fullscreen Following Not Working (Linux)

**Requirements**:
```bash
# Install required utilities
sudo apt-get install x11-utils

# Verify installation
which xprop
which xwininfo

# Check display server (must be X11)
echo $XDG_SESSION_TYPE
```

### Performance Tips

#### For Best Quality:
- Use wired connection (if streaming)
- Close resource-heavy applications
- Disable background processes
- Use SSD for output location

#### For Lower Resource Usage:
- Use smaller capture areas
- Disable cursor tracking
- Disable click visualization
- Disable stats overlay
- Use 16:9 aspect ratio (smallest area)

### System Requirements

#### Minimum:
- CPU: Dual-core 2.0 GHz
- RAM: 2 GB
- Disk: 100 MB free space + recording storage
- Display: 1024x768

#### Recommended:
- CPU: Quad-core 2.5 GHz or better
- RAM: 4 GB or more
- Disk: SSD with ample free space
- Display: 1920x1080 or higher

---

## 👨‍💻 Development

### Project Structure

```
screen-recorder/
├── screen_recorder.py      # Main application file
├── requirements.txt        # Python dependencies
├── sc_icon.png            # Application icon
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore             # Git ignore rules
└── examples/              # Example recordings (optional)
```

### Code Overview

#### Key Classes
- **`ScreenRecorderApp`**: Main application class
  - GUI management
  - Recording state control
  - Event handling

#### Key Methods
- **`_record_loop()`**: Background recording thread
- **`_draw_cursor_and_clicks()`**: Overlay rendering
- **`_maybe_update_bbox_follow()`**: Fullscreen tracking
- **`_refresh_region()`**: Capture area calculation

### Adding New Features

#### Example: Adding a New Aspect Ratio

```python
# In _build_ui() method:
ratios = ["Full Screen", "16:9", "9:16", "4:3", "21:9"]  # Add 21:9

# In _ratio_tuple() method:
def _ratio_tuple(self) -> Optional[Tuple[int, int]]:
    val = self.ratio_var.get()
    if val == "21:9":
        return (21, 9)  # Add new ratio
    # ... rest of the code
```

### Running Tests

Currently, the project doesn't have automated tests. Consider adding:
- Unit tests for frame processing
- Integration tests for recording workflow
- Performance benchmarks

### Building Executable

Create standalone executable with PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=sc_icon.png screen_recorder.py

# Output in dist/ directory
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Report Bugs**: Open an issue with detailed reproduction steps
2. **Suggest Features**: Propose new features via issues
3. **Submit Pull Requests**: Fix bugs or implement features
4. **Improve Documentation**: Enhance README or add code comments
5. **Share Examples**: Provide example use cases or recordings

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to new functions/classes
- Keep functions focused and modular
- Comment complex logic

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat(recording): Add support for 60 FPS recording

Implemented adjustable frame rate selection in GUI.
Added FPS spinbox in settings panel.
Updated recording loop to handle variable FPS.

Closes #123
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 HRaJi Screen Recorder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Libraries Used

- **[MSS](https://github.com/BoboTiG/python-mss)** - Ultra-fast screen capture
- **[OpenCV](https://opencv.org/)** - Computer vision and video processing
- **[NumPy](https://numpy.org/)** - Numerical computing
- **[pynput](https://github.com/moses-palmer/pynput)** - Input monitoring and control
- **[tkinter](https://docs.python.org/3/library/tkinter.html)** - GUI framework

### Inspiration

- Built for content creators, developers, and educators
- Designed with user experience and performance in mind
- Open source contribution to the Python community

### Special Thanks

- Python community for excellent libraries
- Contributors and users for feedback
- Open source community for inspiration

---

## 📞 Contact & Support

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/screen-recorder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/screen-recorder/discussions)
- **Email**: your.email@example.com

### Links

- **Homepage**: [Project Website](https://github.com/yourusername/screen-recorder)
- **Documentation**: [Full Docs](https://github.com/yourusername/screen-recorder/wiki)
- **Changelog**: [Release Notes](https://github.com/yourusername/screen-recorder/releases)

---

## 🗺️ Roadmap

### Planned Features

- [ ] **Variable FPS**: Adjustable frame rate (15-60 FPS)
- [ ] **Audio Recording**: System audio and microphone support
- [ ] **Multiple Codecs**: H.264, H.265, VP9 support
- [ ] **Webcam Overlay**: Picture-in-picture webcam recording
- [ ] **Annotation Tools**: Draw, text, arrows during recording
- [ ] **Scheduled Recording**: Start/stop at specific times
- [ ] **Multi-Monitor**: Select specific monitor for recording
- [ ] **Streaming**: Live streaming to platforms (YouTube, Twitch)
- [ ] **GIF Export**: Convert recordings to animated GIFs
- [ ] **Video Editing**: Basic trim and merge functionality

### Future Enhancements

- Cloud upload integration
- Hardware acceleration (NVENC, QuickSync)
- Custom hotkey configuration
- Recording profiles/presets
- Command-line interface
- Plugin system

---

## 📊 Project Statistics

- **Lines of Code**: ~1,200
- **Dependencies**: 4 core libraries
- **Supported Platforms**: 3 (Linux, Windows, macOS)
- **License**: MIT (permissive)

---

<div align="center">

### ⭐ Star this project if you find it helpful!

**Made with ❤️ using Python**

[Report Bug](https://github.com/yourusername/screen-recorder/issues) • [Request Feature](https://github.com/yourusername/screen-recorder/issues) • [Contribute](https://github.com/yourusername/screen-recorder/pulls)

</div>
