# Security Policy

## Supported Versions

Currently supported versions of HRaJi Screen Recorder:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in HRaJi Screen Recorder, please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please email security details to:
- **Email**: your.email@example.com
- **Subject**: [SECURITY] HRaJi Screen Recorder - Brief Description

### What to Include

Please include the following information:

1. **Description**: Clear description of the vulnerability
2. **Impact**: Potential impact and severity
3. **Reproduction**: Step-by-step instructions to reproduce
4. **Environment**: OS, Python version, affected versions
5. **Proof of Concept**: Code or screenshots (if applicable)
6. **Suggested Fix**: If you have ideas for fixing

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Development**: Depends on severity
- **Disclosure**: After fix is released

### Security Best Practices

When using HRaJi Screen Recorder:

#### For Users

1. **Download from Official Sources**
   - Only download from official GitHub repository
   - Verify checksums if provided
   - Be cautious of third-party distributions

2. **Keep Software Updated**
   - Regularly check for updates
   - Review changelog for security fixes
   - Update dependencies periodically

3. **Permissions**
   - Grant only necessary permissions
   - Review screen recording permissions
   - Be cautious with global hotkeys

4. **Output Security**
   - Store recordings in secure locations
   - Be aware of sensitive content in recordings
   - Delete unnecessary recordings

5. **Network Security**
   - Application doesn't require internet
   - Firewall rules not needed
   - No data transmission (local only)

#### For Developers

1. **Code Review**
   - Review all pull requests
   - Check for injection vulnerabilities
   - Validate user inputs

2. **Dependencies**
   - Keep dependencies updated
   - Monitor security advisories
   - Use `pip-audit` for vulnerability scanning

3. **Input Validation**
   - Validate file paths
   - Sanitize filename templates
   - Check coordinate bounds

4. **File Operations**
   - Use safe file operations
   - Avoid path traversal vulnerabilities
   - Set appropriate file permissions

## Known Security Considerations

### Screen Capture Permissions

This application requires screen capture permissions, which grants access to:
- All visible screen content
- Application windows
- Desktop environment

**Mitigation**: 
- Only grant permissions if you trust the application
- Review source code before running
- Use virtual machines for testing

### Global Hotkeys

Global hotkeys can potentially:
- Intercept keyboard input
- Work across all applications
- Trigger actions system-wide

**Mitigation**:
- Hotkeys are optional (pynput library)
- Limited to specific key combinations
- Can be disabled by not installing pynput

### Mouse Tracking

Mouse position tracking could theoretically:
- Track cursor movements
- Monitor user activity
- Capture interaction patterns

**Mitigation**:
- Only active during recording
- Used solely for cursor overlay
- No data storage or transmission

### File System Access

The application:
- Writes video files to user-specified locations
- Reads configuration from local storage
- No automatic file uploads or sharing

**Mitigation**:
- User controls output directory
- No hidden file operations
- All file operations are explicit

## Security Updates

Security updates will be:
- Released as soon as possible
- Clearly marked in changelog
- Announced via GitHub releases
- Recommended for immediate installation

### Update Notification

Subscribe to notifications:
1. Watch the GitHub repository
2. Enable release notifications
3. Star the repository for updates

## Vulnerability Disclosure Policy

### Coordinated Disclosure

We follow coordinated disclosure:
1. Reporter notifies us privately
2. We acknowledge and investigate
3. We develop and test fix
4. We release patched version
5. Public disclosure after fix

### Public Disclosure Timeline

- **Critical vulnerabilities**: 30 days after fix
- **High severity**: 60 days after fix
- **Medium/Low severity**: 90 days after fix

### Credit

Security researchers who report vulnerabilities will be:
- Credited in security advisory
- Listed in acknowledgments
- Thanked in release notes

## Security Checklist

Before each release:

- [ ] Dependencies updated to latest secure versions
- [ ] No known vulnerabilities in dependencies
- [ ] Code reviewed for security issues
- [ ] Input validation implemented
- [ ] File operations secured
- [ ] Permissions minimized
- [ ] Security documentation updated
- [ ] Test with security scanning tools

## Common Vulnerabilities (CVE)

None reported as of latest version.

## Security Tools

Recommended tools for security analysis:

### Dependency Scanning
```bash
# Install pip-audit
pip install pip-audit

# Scan dependencies
pip-audit -r requirements.txt
```

### Code Analysis
```bash
# Install bandit
pip install bandit

# Run security checks
bandit -r screen_recorder.py
```

### Safety Check
```bash
# Install safety
pip install safety

# Check for known vulnerabilities
safety check -r requirements.txt
```

## Additional Resources

- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [CWE Database](https://cwe.mitre.org/)
- [CVE Database](https://cve.mitre.org/)

## Questions?

For security questions that are not vulnerabilities:
- Open a GitHub Discussion
- Tag with "security" label
- Email for sensitive matters

Thank you for helping keep HRaJi Screen Recorder secure!
