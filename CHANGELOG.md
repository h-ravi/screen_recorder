# Changelog

All notable changes to HRaJi Screen Recorder will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Variable FPS support (15-60 FPS)
- Audio recording (system audio and microphone)
- Multiple codec options (H.264, H.265, VP9)
- Webcam overlay support
- Multi-monitor selection
- Annotation tools

## [1.0.0] - 2025-10-15

### Added
- Initial release of HRaJi Screen Recorder
- Core screen recording functionality at 30 FPS
- Pause and resume recording capability
- Custom area selection with drag-to-select interface
- Aspect ratio presets (Full Screen, 16:9, 9:16, 4:3)
- Cursor tracking and visualization
- Mouse click visualization with animated ripples
- Real-time performance statistics overlay
- Visual border overlay for capture area
- Countdown timer before recording starts
- Floating mini controller window
- Global keyboard shortcuts (Alt+Shift+S/P/R)
- Follow fullscreen window mode (Linux X11)
- Customizable output directory and filename templates
- strftime support for timestamp-based filenames
- Safe close protection during active recording
- Constant frame rate (CFR) encoding
- Frame duplication for smooth playback
- Multi-threaded recording engine
- Comprehensive error handling
- Cross-platform support (Linux, Windows, macOS)

### Technical Features
- MSS-based screen capture for high performance
- OpenCV video encoding with MP4V codec
- NumPy-based frame processing
- pynput integration for global hotkeys and mouse tracking
- tkinter/ttk-based modern GUI
- Thread-safe recording with event synchronization
- Precise frame timing with monotonic clock
- Automatic dimension alignment (even pixel counts)
- Dynamic fullscreen window detection (X11)
- Overlay rendering system with multiple windows
- Configurable stats overlay with position options

### Documentation
- Comprehensive README.md with detailed feature descriptions
- Installation instructions for all platforms
- Usage guide with examples
- Troubleshooting section
- Technical architecture documentation
- Contributing guidelines
- MIT License

### Dependencies
- Python 3.8+
- mss >= 9.0.1
- numpy >= 1.24.0
- opencv-python >= 4.8.0
- pynput >= 1.7.6

## Version History Legend

### Types of Changes
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security vulnerability fixes

---

## Future Versions

### [1.1.0] - Planned
**Focus: Audio Support**

#### Planned Features
- System audio recording
- Microphone audio recording
- Audio/video synchronization
- Audio level meters
- Audio codec selection

### [1.2.0] - Planned
**Focus: Advanced Codecs**

#### Planned Features
- H.264 codec support
- H.265/HEVC codec support
- VP9 codec support
- Hardware acceleration (NVENC, QuickSync)
- Quality/bitrate settings
- Codec comparison presets

### [1.3.0] - Planned
**Focus: Multi-Monitor & Webcam**

#### Planned Features
- Multi-monitor selection
- Specific monitor recording
- Webcam overlay (PiP)
- Webcam position configuration
- Webcam recording without screen

### [1.4.0] - Planned
**Focus: Annotation Tools**

#### Planned Features
- Real-time drawing tools
- Text annotations
- Arrow/shape tools
- Annotation persistence
- Annotation export

### [1.5.0] - Planned
**Focus: Professional Features**

#### Planned Features
- Scheduled recording
- Recording profiles/presets
- Custom hotkey configuration
- Command-line interface
- Batch processing
- Video trimming/merging

---

## Development Notes

### Version Numbering

This project uses Semantic Versioning:
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

Example: `1.2.3`
- `1` = Major version
- `2` = Minor version
- `3` = Patch version

### Release Process

1. Update version in `screen_recorder.py`
2. Update CHANGELOG.md with release notes
3. Create git tag: `git tag -a v1.0.0 -m "Release version 1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with changelog
6. Build and test executable
7. Update documentation

### Compatibility Notes

- **Python**: Minimum 3.8, tested up to 3.12
- **Linux**: X11 required for advanced features, Wayland limited support
- **Windows**: Windows 10+ recommended
- **macOS**: macOS 10.14+ recommended

---

[Unreleased]: https://github.com/yourusername/screen-recorder/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/screen-recorder/releases/tag/v1.0.0
