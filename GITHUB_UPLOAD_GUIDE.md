# GitHub Upload Guide

Complete guide for uploading HRaJi Screen Recorder to GitHub.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Preparing Your Repository](#preparing-your-repository)
4. [Uploading to GitHub](#uploading-to-github)
5. [Post-Upload Configuration](#post-upload-configuration)
6. [Creating Your First Release](#creating-your-first-release)
7. [Repository Settings](#repository-settings)
8. [Best Practices](#best-practices)

---

## Prerequisites

### Required Tools

1. **Git**: Version control system
   ```bash
   # Check if installed
   git --version
   
   # Install on Ubuntu/Debian
   sudo apt install git
   
   # Install on macOS
   brew install git
   
   # Install on Windows
   # Download from https://git-scm.com/
   ```

2. **GitHub Account**: Free account at [github.com](https://github.com)

3. **Git Configuration**:
   ```bash
   # Set your name
   git config --global user.name "Your Name"
   
   # Set your email (use GitHub email)
   git config --global user.email "your.email@example.com"
   
   # Verify settings
   git config --list
   ```

---

## Initial Setup

### 1. Initialize Git Repository

Navigate to your project directory:

```bash
cd /home/r/Python/screen_recorder

# Initialize git repository
git init

# Check status
git status
```

### 2. Review Files

Ensure all necessary files are present:

```bash
ls -la
```

Expected files:
- ✅ screen_recorder.py
- ✅ requirements.txt
- ✅ sc_icon.png
- ✅ README.md
- ✅ LICENSE
- ✅ .gitignore
- ✅ CONTRIBUTING.md
- ✅ CHANGELOG.md
- ✅ INSTALL.md
- ✅ SECURITY.md
- ✅ CODE_OF_CONDUCT.md
- ✅ .github/ directory with templates

### 3. Verify .gitignore

Check that `.gitignore` exists and contains:

```bash
cat .gitignore
```

This prevents uploading unnecessary files like:
- Virtual environments (venv/)
- Python cache (__pycache__)
- Recorded videos (*.mp4)
- OS-specific files (.DS_Store)

---

## Preparing Your Repository

### 1. Stage All Files

```bash
# Add all files to staging
git add .

# Check what's staged
git status
```

You should see files in green, ready to commit.

### 2. Verify No Unwanted Files

```bash
# List staged files
git ls-files

# If you see unwanted files, remove them:
git rm --cached <filename>
git rm -r --cached <directory>
```

### 3. Make Initial Commit

```bash
# Commit with descriptive message
git commit -m "Initial commit: HRaJi Screen Recorder v1.0.0

- Core screen recording functionality
- Advanced features (cursor, clicks, stats)
- Comprehensive documentation
- GitHub templates and guidelines"

# Verify commit
git log
```

---

## Uploading to GitHub

### Method 1: Create Repository on GitHub First (Recommended)

#### Step 1: Create Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click the **+** icon → **New repository**
3. Fill in details:
   - **Repository name**: `screen-recorder` or `hraji-screen-recorder`
   - **Description**: "A powerful, feature-rich screen recording application built with Python"
   - **Visibility**: Public (or Private)
   - **Do NOT initialize with**:
     - ❌ README (you already have one)
     - ❌ .gitignore (you already have one)
     - ❌ License (you already have one)
4. Click **Create repository**

#### Step 2: Connect Local to GitHub

GitHub will show you commands. Use the "push an existing repository" section:

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/screen-recorder.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Method 2: Using GitHub CLI (gh)

```bash
# Install GitHub CLI
# Ubuntu/Debian:
sudo apt install gh

# macOS:
brew install gh

# Authenticate
gh auth login

# Create repository and push
gh repo create screen-recorder --public --source=. --push

# Set description
gh repo edit --description "A powerful, feature-rich screen recording application built with Python"
```

### Authentication Methods

#### HTTPS with Token (Recommended)

1. Create Personal Access Token:
   - GitHub → Settings → Developer settings
   - Personal access tokens → Tokens (classic)
   - Generate new token (classic)
   - Select scopes: `repo` (full control)
   - Generate and copy token

2. Use token when pushing:
   ```bash
   # GitHub will ask for password
   # Paste your token instead
   git push -u origin main
   ```

#### SSH Key (Alternative)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key

# Test connection
ssh -T git@github.com

# Use SSH remote
git remote set-url origin git@github.com:YOUR_USERNAME/screen-recorder.git
```

---

## Post-Upload Configuration

### 1. Verify Upload

Visit your repository: `https://github.com/YOUR_USERNAME/screen-recorder`

Check that all files are visible:
- ✅ Source code files
- ✅ Documentation files
- ✅ GitHub templates in .github/
- ✅ README.md displays on homepage

### 2. Add Repository Topics

On GitHub repository page:
1. Click ⚙️ (Settings gear) next to "About"
2. Add topics (tags):
   - `screen-recorder`
   - `screen-capture`
   - `python`
   - `tkinter`
   - `opencv`
   - `video-recording`
   - `cross-platform`
   - `linux`
   - `windows`
   - `macos`

### 3. Add Repository Description

Edit the "About" section:
- **Description**: "A powerful, feature-rich screen recording application built with Python"
- **Website**: (optional, if you have one)
- **Topics**: (added above)

### 4. Enable Features

In repository Settings:
- ✅ **Issues**: Enable
- ✅ **Projects**: Optional
- ✅ **Discussions**: Enable (for Q&A)
- ✅ **Wiki**: Optional
- ❌ **Sponsorships**: Optional

---

## Creating Your First Release

### Step 1: Tag Your Version

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0

Initial release with core features:
- Screen recording at 30 FPS
- Pause/resume capability
- Custom area selection
- Cursor and click visualization
- Performance statistics overlay
- Global hotkeys support
- Cross-platform compatibility"

# Push tag to GitHub
git push origin v1.0.0
```

### Step 2: Create Release on GitHub

1. Go to repository → **Releases** → **Create a new release**
2. Choose tag: `v1.0.0`
3. Release title: `HRaJi Screen Recorder v1.0.0`
4. Description (copy from CHANGELOG.md):

```markdown
# HRaJi Screen Recorder v1.0.0

First stable release! 🎉

## 🌟 Highlights

- **High-quality screen recording** at 30 FPS
- **Pause and resume** without creating separate files
- **Custom area selection** with visual interface
- **Cursor and click visualization** for tutorials
- **Real-time performance statistics**
- **Global hotkeys** for convenient control
- **Cross-platform** support (Linux, Windows, macOS)

## 📦 Installation

```bash
pip install -r requirements.txt
python screen_recorder.py
```

See [INSTALL.md](INSTALL.md) for detailed instructions.

## 📖 Documentation

- [User Guide](README.md)
- [Installation Guide](INSTALL.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🐛 Known Issues

None reported yet. Please report issues on the [Issues page](https://github.com/YOUR_USERNAME/screen-recorder/issues).

## 🙏 Acknowledgments

Built with ❤️ using:
- [MSS](https://github.com/BoboTiG/python-mss) - Screen capture
- [OpenCV](https://opencv.org/) - Video processing
- [NumPy](https://numpy.org/) - Numerical computing
- [pynput](https://github.com/moses-palmer/pynput) - Input monitoring

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.
```

5. Optional: Attach executable (if you built one with PyInstaller)
6. Click **Publish release**

---

## Repository Settings

### 1. Branch Protection (Recommended)

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews
- ✅ Require status checks
- ✅ Include administrators

### 2. Security Settings

Settings → Security:
- ✅ **Dependency graph**: Enabled
- ✅ **Dependabot alerts**: Enabled
- ✅ **Dependabot security updates**: Enabled
- ✅ **Code scanning**: Optional

### 3. Issue Labels

Settings → Issues → Labels:

Create custom labels:
- `priority: high` (red)
- `priority: medium` (orange)
- `priority: low` (yellow)
- `status: in-progress` (blue)
- `status: needs-info` (purple)
- `type: bug` (red) - already exists
- `type: feature` (green) - already exists
- `good first issue` (green) - already exists
- `help wanted` (green) - already exists

### 4. Social Preview Image

1. Create an image (1280x640 pixels)
2. Settings → Options → Social preview
3. Upload image

---

## Best Practices

### Commit Message Guidelines

```bash
# Good commit messages
git commit -m "fix(recording): Resolve memory leak in frame capture"
git commit -m "feat(ui): Add dark mode support"
git commit -m "docs(readme): Update installation instructions"

# Bad commit messages (avoid)
git commit -m "fix"
git commit -m "update"
git commit -m "changes"
```

### Regular Updates

```bash
# After making changes
git status
git add .
git commit -m "descriptive message"
git push origin main
```

### Branch Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: Add new feature"

# Push branch
git push origin feature/new-feature

# Create pull request on GitHub
# After merge, delete branch
git checkout main
git pull origin main
git branch -d feature/new-feature
```

---

## Updating Your Repository

### Making Changes

```bash
# 1. Make your changes to files

# 2. Check what changed
git status
git diff

# 3. Stage changes
git add file1.py file2.py
# or add all
git add .

# 4. Commit with message
git commit -m "type(scope): description"

# 5. Push to GitHub
git push origin main
```

### Pulling Updates

```bash
# If working with collaborators
git pull origin main

# Resolve conflicts if any
# Then commit and push
```

---

## Troubleshooting

### Authentication Failed

```bash
# Check remote URL
git remote -v

# Use HTTPS with token
git remote set-url origin https://github.com/USERNAME/REPO.git

# Or use SSH
git remote set-url origin git@github.com:USERNAME/REPO.git
```

### Files Too Large

```bash
# GitHub has 100MB file limit
# If you accidentally added large files:

git rm --cached large_file.mp4
echo "*.mp4" >> .gitignore
git add .gitignore
git commit -m "Remove large files and update gitignore"
```

### Undo Last Commit

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes
git reset --hard HEAD~1

# If already pushed (use with caution)
git push -f origin main
```

### Remove Sensitive Data

```bash
# If you committed passwords/keys
# Use BFG Repo-Cleaner or git-filter-repo
# Contact GitHub support for help

# Prevention: Always use .gitignore
echo ".env" >> .gitignore
```

---

## Next Steps After Upload

1. **Announce your project**:
   - Share on social media
   - Post on Reddit (r/Python, r/opensource)
   - Submit to awesome-python lists

2. **Monitor activity**:
   - Watch for issues
   - Respond to questions
   - Review pull requests

3. **Maintain momentum**:
   - Regular updates
   - Fix reported bugs
   - Add requested features
   - Keep documentation current

4. **Engage community**:
   - Thank contributors
   - Welcome new users
   - Guide first-time contributors
   - Share project milestones

---

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Markdown Guide](https://guides.github.com/features/mastering-markdown/)

---

## Quick Reference

```bash
# Essential commands
git init                          # Initialize repository
git add .                         # Stage all changes
git commit -m "message"           # Commit changes
git push origin main              # Push to GitHub
git pull origin main              # Pull from GitHub
git status                        # Check status
git log                           # View history
git tag -a v1.0.0 -m "message"   # Create tag
git push origin v1.0.0            # Push tag
```

---

**Congratulations! Your project is now on GitHub! 🎉**
