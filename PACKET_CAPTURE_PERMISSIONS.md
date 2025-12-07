# Packet Capture Permissions Guide

## Overview

Network packet capture requires elevated privileges to access the network interfaces at a low level. This guide explains how to grant the necessary permissions to the Network Monitoring application on different operating systems.

## Why Are Permissions Needed?

Packet capture operations require raw socket access, which is a privileged operation on most operating systems. This is a security feature to prevent unauthorized programs from intercepting network traffic.

## Permission Setup by Operating System

### Linux (Recommended Method)

The recommended approach on Linux is to grant specific capabilities to the Python executable without running the entire application as root:

```bash
# Find the actual Python binary (not symlink)
which python3
readlink -f $(which python3)

# Grant capabilities to the Python binary
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3.12

# Verify capabilities were set
getcap /usr/bin/python3.12
```

**Advantages:**
- More secure than running as root
- Only grants network capture capabilities
- Application runs with normal user privileges

**Alternative (Not Recommended for Production):**
```bash
# Run the entire application as root
sudo python3 app.py
```

### macOS

On macOS, you need to run the application with root privileges:

```bash
sudo python3 app.py
```

### Windows

On Windows, you need to run the Command Prompt as Administrator:

1. Right-click on Command Prompt or PowerShell
2. Select "Run as Administrator"
3. Navigate to the backend directory
4. Run: `python app.py`

## Checking Permissions

The application includes a built-in permission checking endpoint:

```bash
# After logging in, call the check-permissions endpoint
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:5000/api/analysis/check-permissions
```

Response when permissions are available:
```json
{
  "has_permission": true,
  "message": "Packet capture permissions are available"
}
```

Response when permissions are missing:
```json
{
  "has_permission": false,
  "message": "Insufficient permissions for packet capture",
  "instructions": {
    "os": "Linux",
    "methods": [
      {
        "method": "Grant capabilities to Python binary (recommended)",
        "command": "sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3",
        "description": "This allows Python to capture packets without running as root"
      },
      {
        "method": "Run application as root (not recommended for production)",
        "command": "sudo python3 app.py",
        "description": "Run the entire application with root privileges"
      }
    ]
  }
}
```

## Security Considerations

### Production Deployments

For production deployments, we recommend:

1. **Use capabilities on Linux** instead of running as root
2. **Limit network access** to only the interfaces that need monitoring
3. **Run the application** in a restricted environment (container, VM, etc.)
4. **Regular security audits** of captured data and access logs
5. **Encrypted storage** for captured packet data

### Development Environments

For development:
- Using `sudo` is acceptable for quick testing
- Consider setting up capabilities once rather than using `sudo` repeatedly
- Be aware that packet capture can see sensitive data on your network

## Troubleshooting

### "Operation not permitted" Error

If you see this error, it means the application doesn't have the necessary permissions:

```
PermissionError: Insufficient permissions for packet capture.
```

**Solution:** Follow the permission setup steps for your operating system above.

### Capabilities Not Working on Linux

If you granted capabilities but still get permission errors:

1. Ensure you granted capabilities to the actual binary, not a symlink:
   ```bash
   file /usr/bin/python3
   readlink -f /usr/bin/python3
   ```

2. Verify capabilities are set:
   ```bash
   getcap /usr/bin/python3.12
   ```

3. Check if AppArmor or SELinux is blocking the operation

### Windows Administrator Mode Not Working

1. Ensure you're running Command Prompt/PowerShell "as Administrator"
2. Check Windows Firewall settings
3. Verify that WinPcap or Npcap is installed (required for Scapy on Windows)

## API Endpoints Requiring Permissions

The following endpoints require packet capture permissions:

- `POST /api/analysis/capture` - Start packet capture
- `GET /api/analysis/packets` - Retrieve captured packets (requires previous capture with permissions)

Other endpoints (monitoring, system stats, etc.) do NOT require special permissions and will work normally.

## No Mock Data

**Important:** This application does NOT use mock or simulated data. All network monitoring data comes from real system and network activity. If packet capture permissions are not available, the capture endpoint will return a clear error message with instructions on how to grant permissions.

## Additional Resources

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [setcap Command](https://man7.org/linux/man-pages/man8/setcap.8.html)
