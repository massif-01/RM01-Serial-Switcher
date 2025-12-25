# RM-01 Serial Switcher Tool

## Introduction

A tool for switching between different modules on RM-01 device via serial console.

## Features

**Switch to Inference Module**
   - Automatically detect `/dev/ttyACM0`
   - Connect to serial console
   - Execute `usbmux agx` command
   - Save configuration

**Switch to Application Module**
   - Automatically detect `/dev/ttyACM0`
   - Connect to serial console
   - Execute `usbmux lpmu` command
   - Save configuration

## Prerequisites

- Linux operating system
- Python 3.6+
- `tio` serial terminal tool installed
- `pexpect` Python library

## Installation

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt install tio

# Arch Linux
sudo pacman -S tio
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 main.py
# or
./run.sh
```

## System Requirements

- Linux operating system
- Python 3.6+
- tio serial terminal
- Access to `/dev/ttyACM0` (may require sudo or user in dialout group)

## User Permission Setup

To access serial ports without sudo, add your user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

Then log out and log back in for the change to take effect.

## Notes

- The tool automatically waits for `/dev/ttyACM0` to be available
- If device is not detected after 10 seconds, the operation will fail
- Make sure the RM-01 device is properly connected via USB

