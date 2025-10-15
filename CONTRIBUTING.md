# Contributing to HRaJi Screen Recorder

Thank you for your interest in contributing to HRaJi Screen Recorder! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/screen-recorder.git
   cd screen-recorder
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/screen-recorder.git
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title**: Summarize the problem
- **Description**: Detailed explanation of the bug
- **Steps to reproduce**: List exact steps to trigger the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, library versions
- **Screenshots**: If applicable

**Example**:
```markdown
**Title**: Recording fails with large capture areas

**Description**: Application crashes when recording areas larger than 3840x2160

**Steps to reproduce**:
1. Select Full Screen mode on 4K monitor
2. Click Start button
3. Application crashes after 2-3 seconds

**Expected**: Recording should work on any resolution
**Actual**: Application crashes with "Memory Error"

**Environment**:
- OS: Ubuntu 22.04
- Python: 3.10.6
- OpenCV: 4.8.0
- RAM: 8GB
```

### Suggesting Features

Feature requests are welcome! Please include:

- **Use case**: Why this feature is needed
- **Proposed solution**: How it should work
- **Alternatives**: Other approaches you've considered
- **Examples**: Similar features in other applications

### Submitting Changes

1. Ensure your code follows the [coding standards](#coding-standards)
2. Write clear commit messages (see [commit guidelines](#commit-guidelines))
3. Update documentation if needed
4. Add tests if applicable
5. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv or virtualenv)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/your-username/screen-recorder.git
cd screen-recorder

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt  # Optional

# Run the application
python screen_recorder.py
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these specifics:

#### Indentation
- Use 4 spaces (no tabs)
- Continuation lines should align wrapped elements

#### Line Length
- Maximum 88 characters (Black formatter standard)
- Maximum 120 for comments and docstrings

#### Naming Conventions
```python
# Classes: PascalCase
class ScreenRecorder:
    pass

# Functions and variables: snake_case
def capture_screen():
    frame_count = 0

# Constants: UPPER_SNAKE_CASE
MAX_FPS = 60
DEFAULT_CODEC = "mp4v"

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

#### Type Hints
Use type hints for function signatures:
```python
def process_frame(frame: np.ndarray, bbox: BBox) -> np.ndarray:
    """Process a captured frame."""
    # Implementation
    return frame
```

#### Docstrings
Use Google-style docstrings:
```python
def calculate_region(width: int, height: int, ratio: Optional[Tuple[int, int]]) -> BBox:
    """Calculate capture region based on aspect ratio.
    
    Args:
        width: Screen width in pixels
        height: Screen height in pixels
        ratio: Optional aspect ratio as (width, height) tuple
    
    Returns:
        BBox object representing the capture region
    
    Raises:
        ValueError: If width or height is negative
    """
    # Implementation
```

### Code Organization

#### Imports
Group imports in this order:
```python
# Standard library
import os
import sys
import time

# Third-party
import cv2
import numpy as np
import mss

# Local
from .utils import helper_function
```

#### Class Structure
Organize class methods by category:
```python
class ScreenRecorder:
    def __init__(self):
        """Initialization"""
        pass
    
    # Public methods
    def start_recording(self):
        """Start recording"""
        pass
    
    # Private methods
    def _capture_frame(self):
        """Capture a single frame"""
        pass
    
    # Event handlers
    def on_close(self):
        """Handle window close"""
        pass
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies

### Examples

```
feat(recording): Add support for 60 FPS recording

- Added FPS selector in GUI
- Updated recording loop to handle variable FPS
- Modified frame scheduler for accurate timing

Closes #45
```

```
fix(cursor): Cursor not visible on high-DPI displays

Fixed cursor scaling issue on displays with DPI > 150.
Cursor now scales proportionally to screen resolution.

Fixes #78
```

```
docs(readme): Update installation instructions

Added platform-specific notes for Linux, Windows, and macOS.
Included troubleshooting section for common issues.
```

### Commit Best Practices

- Keep commits atomic (one logical change)
- Write in present tense ("Add feature" not "Added feature")
- Keep subject line under 50 characters
- Wrap body at 72 characters
- Reference issues/PRs in footer

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**:
   - Run the application
   - Test all affected features
   - Check for errors or warnings

3. **Update documentation**:
   - README.md if user-facing changes
   - Code comments for complex logic
   - Docstrings for new functions/classes

### Creating Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**:
   - Navigate to original repository
   - Click "New Pull Request"
   - Select your fork and branch

3. **Fill PR template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   
   ## Testing
   How were these changes tested?
   
   ## Screenshots
   If applicable, add screenshots
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-reviewed code
   - [ ] Commented complex code
   - [ ] Updated documentation
   - [ ] No new warnings
   - [ ] Added tests if applicable
   ```

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, PR will be merged
- Delete your feature branch after merge

## Testing

### Manual Testing

Test these scenarios before submitting:

1. **Basic Recording**:
   - Start, pause, resume, stop
   - Different aspect ratios
   - Custom area selection

2. **Visual Features**:
   - Cursor tracking
   - Click visualization
   - Border overlay
   - Stats overlay

3. **Edge Cases**:
   - Very small capture areas
   - Very large capture areas
   - Rapid start/stop cycles
   - Long recordings (>10 minutes)

4. **Keyboard Shortcuts**:
   - All hotkey combinations
   - Hotkeys during different states

### Automated Testing (Future)

```python
# Example test structure
import unittest

class TestScreenRecorder(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.recorder = ScreenRecorderApp()
    
    def test_aspect_ratio_calculation(self):
        """Test aspect ratio calculations"""
        bbox = self.recorder._calc_centered_bbox((16, 9))
        self.assertEqual(bbox.width / bbox.height, 16/9)
    
    def tearDown(self):
        """Clean up after tests"""
        self.recorder.on_close()
```

## Documentation

### Code Comments

```python
# Good: Explains WHY, not WHAT
# Calculate next frame time accounting for pause duration
self._next_frame_time += frame_interval

# Bad: Explains obvious code
# Add frame_interval to _next_frame_time
self._next_frame_time += frame_interval
```

### README Updates

When adding features, update:
- Feature list
- Usage instructions
- Configuration options
- Troubleshooting section

### Inline Documentation

Document complex algorithms:
```python
def _calc_centered_bbox(self, ratio: Optional[Tuple[int, int]]) -> BBox:
    """Calculate centered bounding box.
    
    Algorithm:
    1. Get monitor dimensions
    2. If ratio is None, return full screen
    3. Calculate largest fitting rectangle:
       - Try width-constrained: h = W * (rh/rw)
       - If h > H, use height-constrained: w = H * (rw/rh)
    4. Center within monitor
    5. Ensure even dimensions for video codec
    """
    # Implementation
```

## Questions?

If you have questions:

1. Check existing issues and discussions
2. Read the documentation thoroughly
3. Ask in GitHub Discussions
4. Create an issue with "question" label

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in documentation

Thank you for contributing to HRaJi Screen Recorder! 🎉
