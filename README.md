# CCIC1410-LAW Camera IO Integration for Home Assistant

A custom Home Assistant integration for CCIC1410-LAW IP cameras that enables control and monitoring of digital I/O ports. This integration provides real-time status updates and control capabilities for the camera's digital input and output ports.

## Features

- 📡 Digital input monitoring (high/low state)
- 🔌 Digital output control (grounded/open state)
- 🔄 Automatic state updates
- 🔒 Secure authentication
- 🎯 Easy configuration through Home Assistant UI

## Installation

1. Copy the `custom_components/ccic1410_law` folder to your Home Assistant configuration directory.
2. Restart Home Assistant
3. Go to Configuration > Integrations
4. Click the "+ ADD INTEGRATION" button
5. Search for "CCIC1410-LAW Camera IO"
6. Enter your camera's IP address, username, and password

## Requirements

- Home Assistant 2023.3.0 or newer
- CCIC1410-LAW IP camera with accessible I/O ports
- Network connectivity to the camera
- Python packages: `requests`, `beautifulsoup4`

## Entities Created

### Sensors
- Input State (high/low/unknown)
- Output State (grounded/open/unknown)

### Switch
- Output Control

## Configuration

The integration can be configured entirely through the Home Assistant UI. Required configuration parameters:

```yaml
host: IP address of your camera
username: Camera login username
password: Camera login password
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
