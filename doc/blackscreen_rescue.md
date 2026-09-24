# BlackScreen Rescue MVP

BlackScreen Rescue is an experimental recovery workflow built on top of scrcpy
for Android devices whose display or touch layer is broken.

## Goal

The MVP combines two existing scrcpy modes:

1. `scrcpy --otg` for keyboard/mouse control without ADB.
2. Normal `scrcpy` mirroring after USB debugging is enabled and the computer
   is authorized.

It does **not** bypass a PIN, pattern, password, Factory Reset Protection (FRP),
device encryption, or any account protection.

## Intended use

Use this only on a device you own or a device you are explicitly authorized to
service.

Typical recovery case:

- phone powers on;
- screen is black, cracked, or touch is unusable;
- USB debugging is currently disabled;
- the owner knows the device credentials.

## Linux MVP

Requirements:

- Python 3.9+
- `scrcpy`
- `adb`
- USB cable

Run:

```bash
python3 tools/blackscreen_rescue.py
```

If several devices are connected:

```bash
python3 tools/blackscreen_rescue.py --serial DEVICE_SERIAL
```

Extra arguments after `--` are passed to normal scrcpy once ADB becomes ready:

```bash
python3 tools/blackscreen_rescue.py -- --no-audio
```

## Workflow

```text
USB device connected
        |
        v
scrcpy --otg
(AOA keyboard + mouse, no ADB required)
        |
        v
Owner navigates the phone
Optionally uses TalkBack/accessibility feedback
        |
        v
USB debugging enabled
        |
        v
ADB appears as unauthorized
        |
        v
Owner approves RSA prompt
        |
        v
ADB state = device
        |
        v
OTG process is stopped
        |
        v
normal scrcpy starts
(screen mirroring + control)
```

## Current limitations

- No framebuffer/video can be read without ADB or native video-output support.
- TalkBack activation is not automated in this MVP.
- OEM-specific navigation profiles are not implemented yet.
- AOA/ADB behavior varies by Android version and vendor USB configuration.
- Devices that are locked still require the legitimate owner to unlock them.

## Planned work

- device/USB diagnostics;
- guided TalkBack rescue mode;
- Samsung/Xiaomi/Pixel profiles;
- optional AOA HID consumer-control experiments;
- automatic state machine and better UI;
- Windows/macOS support after the Linux workflow is proven.

## Why this is separate from HDMI

AOA HID can make the computer behave like a USB keyboard/mouse. It cannot make
a phone output video if the phone hardware/firmware does not support a video
transport such as DisplayPort Alt Mode. BlackScreen Rescue therefore uses
accessibility feedback and OTG input only as a bridge until ADB-based mirroring
becomes legitimately available.
