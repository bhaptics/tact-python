# bHaptics Python SDK

Python SDK for bHaptics haptic feedback devices, enabling developers to integrate tactile sensations into their applications.

## Overview

The bHaptics Python SDK provides an asynchronous interface to control bHaptics haptic devices, including vests, gloves, and other tactile feedback hardware. This SDK allows you to create immersive experiences by sending haptic patterns, controlling individual motors, and managing device connections.

## 🔧 Requirements

### Required Software
- **bHaptics Player**: Download and install the PC player from the [official download page](https://www.bhaptics.com/support/downloads)
- **Python 3.8~3.12**: Currently supported Python version

### Developer Account Setup
- **bHaptics Portal**: Create a workspace on the [developer portal](https://developer.bhaptics.com/)
- For detailed setup instructions, refer to the [official documentation](https://docs.bhaptics.com/portal/)

## Installation

```bash
pip install bhaptics-python
```

## Requirements

- Python 3.9+
- bHaptics Player (must be installed and running)
- Compatible bHaptics hardware devices

## Quick Start

```python
import bhaptics_python
import asyncio

async def main():
    # Initialize the SDK
    app_id = "your_app_id"
    api_key = "your_api_key"
    app_version = 1
    
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
    print(f"Initialization result: {result}")
    
    # Check connection
    is_connected = await bhaptics_python.is_connected()
    print(f"Connected: {is_connected}")
    
    # Play a haptic event
    event_name = "your_event_name"
    request_id = await bhaptics_python.play_event(event_name)
    print(f"Playing event: {event_name}, Request ID: {request_id}")

asyncio.run(main())
```

## Core Features

### Device Index System

The bHaptics SDK supports controlling multiple devices simultaneously. You can target all devices or specific devices using the device index system:

- **All Devices**: Functions without `device_index` parameter affect all connected devices
- **Specific Device**: Functions with `device_index` parameter target a specific device (0-9)
- **Device Types**: Different device types have different index ranges
  - Vest devices: typically index 0-3
  - Glove devices: index 8 (left hand), 9 (right hand)
  - Other devices: index 4-7

```python
# Control all devices
request_id = await bhaptics_python.play_event("explosion")

# Control specific device (e.g., device index 1)
device_index = 1
request_id = await bhaptics_python.play_event("explosion", device_index)

# Check which devices are connected
for i in range(10):
    is_connected = await bhaptics_python.is_bhaptics_device_connected(i)
    print(f"Device {i} connected: {is_connected}")
```

### 1. Device Management

#### Initialize Connection
```python
result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
```

#### Check Connection Status
```python
is_connected = await bhaptics_python.is_connected()
is_running = await bhaptics_python.is_bhaptics_player_running()
is_installed = await bhaptics_python.is_bhaptics_player_installed()
```

#### Device Information
```python
device_info = await bhaptics_python.get_device_info_json()
haptic_mappings = await bhaptics_python.get_haptic_mappings_json()
```

### 2. Haptic Playback

#### Play Events
```python
# Play event on all devices
request_id = await bhaptics_python.play_event(event_name)

# Play event on specific device
device_index = 1
request_id = await bhaptics_python.play_event(event_name, device_index)
```

#### Play with Parameters
```python
# All devices
request_id = await bhaptics_python.play_param(
    event_name, 
    intensity=5.0,    # 0.0 - 10.0
    duration=1.0,     # seconds
    x_offset=0.0,     # -1.0 to 1.0
    y_offset=0.0      # -1.0 to 1.0
)

# Specific device
request_id = await bhaptics_python.play_param(
    event_name, 5.0, 1.0, 0.0, 0.0, device_index
)
```

#### Loop Playback
```python
# All devices
request_id = await bhaptics_python.play_loop(
    event_name,
    intensity=5.0,
    duration=1.0,
    x_offset=0.0,
    y_offset=0.0,
    interval=1000,    # milliseconds
    max_count=10      # number of repetitions
)

# Specific device
request_id = await bhaptics_python.play_loop(
    event_name, 5.0, 1.0, 0.0, 0.0, 1000, 10, device_index
)
```

#### Play Without Result (Fire and Forget)
```python
# All devices
await bhaptics_python.play_without_result(event_name, 5.0, 1.0, 0.0, 0.0)

# Specific device
await bhaptics_python.play_without_result(event_name, 5.0, 1.0, 0.0, 0.0, device_index)
```

### 3. Motor Control

#### Direct Motor Control (Dot Pattern)
```python
motor_len = 40
values = [40 if i == target_position else 0 for i in range(motor_len)]

# All devices
request_id = await bhaptics_python.play_dot(0, 1000, values)

# Specific device
request_id = await bhaptics_python.play_dot(0, 1000, values, device_index)
```

#### Path-based Haptics
```python
x_coordinates = [0.5, 0.6, 0.7]  # Normalized coordinates (0.0 - 1.0)
y_coordinates = [0.5, 0.6, 0.7]
intensities = [40, 50, 60]

# All devices
request_id = await bhaptics_python.play_path(0, 1000, x_coordinates, y_coordinates, intensities)

# Specific device
request_id = await bhaptics_python.play_path(0, 1000, x_coordinates, y_coordinates, intensities, device_index)
```

#### Glove Control
```python
glove_len = 8
motors = [100 for _ in range(glove_len)]      # Motor intensities
playtimes = [8 for _ in range(glove_len)]     # Duration for each motor
shapes = [2 for _ in range(glove_len)]        # Waveform shapes
repeat_count = 0

# Left hand (device index 8)
await bhaptics_python.play_glove(8, motors, playtimes, shapes, repeat_count)

# Right hand (device index 9)
await bhaptics_python.play_glove(9, motors, playtimes, shapes, repeat_count)

# Note: play_glove always requires a device_id (8 for left, 9 for right)
```

### 4. Playback Control

#### Stop Functions
```python
# Stop by request ID
await bhaptics_python.stop_by_request_id(request_id)

# Stop by event name
await bhaptics_python.stop_by_event_name(event_name)

# Stop all haptic feedback
await bhaptics_python.stop_all()
```

#### Playback Status
```python
is_playing_by_id = await bhaptics_python.is_playing_event_by_request_id(request_id)
is_playing_by_name = await bhaptics_python.is_playing_event_by_event_id(event_name)
is_any_playing = await bhaptics_python.is_playing_event()
```

### 5. Device-Specific Operations

#### Ping Devices
```python
await bhaptics_python.ping(device_address)  # Ping specific device
await bhaptics_python.ping_all()           # Ping all devices
```

#### Device Settings
```python
# Set vibration strength multiplier (VSM)
await bhaptics_python.set_device_vsm(device_address, 400)

# Swap device position
await bhaptics_python.swap_position(device_address)
```

#### Check Device Connections
```python
for i in range(10):
    is_connected = await bhaptics_python.is_bhaptics_device_connected(i)
    print(f"Device {i} connected: {is_connected}")
```

## Interactive Example

Here's a complete interactive example that demonstrates various SDK features:

```python
import bhaptics_python
import asyncio
import time

async def interactive_demo():
    # Initialize
    app_id = "your_app_id"
    api_key = "your_api_key"
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
    print(f"Initialization: {result}")
    
    device_index = 1  # Default device for device-specific commands
    
    while True:
        command = input("Enter command (help for options, q to quit): ").strip()
        
        if command == 'q':
            break
        elif command == 'help':
            print("""
Available commands:
- p: Play event (all devices)
- pd: Play event (specific device)
- d: Motor dot pattern (all devices)
- dd: Motor dot pattern (specific device)  
- path: Path-based haptics (all devices)
- pathd: Path-based haptics (specific device)
- g: Glove control
- ppp: Play with parameters (all devices)
- pppd: Play with parameters (specific device)
- loop: Loop playback (all devices)
- loopd: Loop playback (specific device)
- s: Stop by request ID
- a: Stop all
- i: Check playback status
- position: Check device connections
- help: Show this help
- q: Quit
            """)
        elif command == 'p':
            event_name = "your_event_name"
            request_id = await bhaptics_python.play_event(event_name)
            print(f"Playing event on all devices: {request_id}")
        elif command == 'pd':
            event_name = "your_event_name"
            request_id = await bhaptics_python.play_event(event_name, device_index)
            print(f"Playing event on device {device_index}: {request_id}")
        elif command == 'd':
            # Animate a moving dot on all devices
            motor_len = 40
            for i in range(motor_len):
                values = [40 if j == i else 0 for j in range(motor_len)]
                await bhaptics_python.play_dot(0, 100, values)
                time.sleep(0.1)
        elif command == 'dd':
            # Animate a moving dot on specific device
            motor_len = 40
            for i in range(motor_len):
                values = [40 if j == i else 0 for j in range(motor_len)]
                await bhaptics_python.play_dot(0, 100, values, device_index)
                time.sleep(0.1)
        elif command == 'g':
            # Control gloves
            glove_len = 8
            motors = [100 for _ in range(glove_len)]
            playtimes = [8 for _ in range(glove_len)]
            shapes = [2 for _ in range(glove_len)]
            repeat_count = 0
            
            # Left hand
            for _ in range(5):
                await bhaptics_python.play_glove(8, motors, playtimes, shapes, repeat_count)
                time.sleep(0.04)
            
            time.sleep(0.5)
            
            # Right hand
            for _ in range(5):
                await bhaptics_python.play_glove(9, motors, playtimes, shapes, repeat_count)
                time.sleep(0.04)
        elif command == 'position':
            # Check device connections
            for i in range(10):
                is_connected = await bhaptics_python.is_bhaptics_device_connected(i)
                print(f"Device {i} connected: {is_connected}")
        # Add more commands as needed...

asyncio.run(interactive_demo())
```

## Error Handling

Always wrap SDK calls in try-catch blocks for production applications:

```python
try:
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
    if not result:
        print("Failed to initialize bHaptics SDK")
except Exception as e:
    print(f"Error initializing SDK: {e}")
```

## Best Practices

1. **Always check connection status** before sending haptic commands
2. **Use appropriate intensities** (0-100) to avoid overwhelming users
3. **Limit concurrent haptic events** to prevent conflicts
4. **Properly close connections** when your application exits
5. **Test with actual hardware** as simulation may behave differently

## API Reference

### Core Functions (All Devices)

| Function | Description | Parameters |
|----------|-------------|------------|
| `registry_and_initialize(app_id, api_key, app_name)` | Initialize SDK connection | App credentials |
| `is_connected()` | Check connection status | None |
| `play_event(event_name)` | Play haptic event on all devices | Event name |
| `play_dot(start_time, duration, values)` | Control individual motors on all devices | Timing, motor values |
| `play_path(start_time, duration, x, y, intensity)` | Path-based haptics on all devices | Coordinates and intensity |
| `play_param(event_name, intensity, duration, x_offset, y_offset)` | Play with parameters on all devices | Event name, playback parameters |
| `play_loop(event_name, intensity, duration, x_offset, y_offset, interval, max_count)` | Loop playback on all devices | Event name, loop parameters |
| `play_without_result(event_name, intensity, duration, x_offset, y_offset)` | Play without waiting for result on all devices | Event name, parameters |
| `play_glove(device_id, motors, playtimes, shapes, repeat_count)` | Control glove devices (8=left, 9=right) | Device ID, motor parameters |
| `stop_all()` | Stop all haptic feedback | None |
| `close()` | Close SDK connection | None |

### Core Functions (Specific Device)

| Function | Description | Parameters |
|----------|-------------|------------|
| `play_event(event_name, device_index)` | Play haptic event on specific device | Event name, device index |
| `play_dot(start_time, duration, values, device_index)` | Control individual motors on specific device | Timing, motor values, device index |
| `play_path(start_time, duration, x, y, intensity, device_index)` | Path-based haptics on specific device | Coordinates, intensity, device index |
| `play_param(event_name, intensity, duration, x_offset, y_offset, device_index)` | Play with parameters on specific device | Event name, parameters, device index |
| `play_loop(event_name, intensity, duration, x_offset, y_offset, interval, max_count, device_index)` | Loop playback on specific device | Event name, loop parameters, device index |
| `play_without_result(event_name, intensity, duration, x_offset, y_offset, device_index)` | Play without waiting for result on specific device | Event name, parameters, device index |

### Playback Control

| Function | Description | Parameters |
|----------|-------------|------------|
| `stop_by_request_id(request_id)` | Stop haptic feedback by request ID | Request ID |
| `stop_by_event_name(event_name)` | Stop haptic feedback by event name | Event name |
| `is_playing_event_by_request_id(request_id)` | Check if specific request is playing | Request ID |
| `is_playing_event_by_event_id(event_name)` | Check if specific event is playing | Event name |
| `is_playing_event()` | Check if any haptic event is playing | None |
| `get_event_time(event_name)` | Get event duration | Event name |

### Device Management

| Function | Description | Parameters |
|----------|-------------|------------|
| `is_bhaptics_player_running()` | Check if bHaptics Player is running | None |
| `is_bhaptics_player_installed()` | Check if bHaptics Player is installed | None |
| `run_bhaptics_player(with_ui)` | Launch bHaptics Player | Boolean for UI display |
| `get_device_info_json()` | Get connected device information | None |
| `get_haptic_mappings_json()` | Get haptic mappings information | None |
| `get_haptic_messages(app_id, api_key, app_version)` | Get haptic messages from server | App credentials |
| `get_haptic_mappings(app_id, api_key, app_version)` | Get haptic mappings from server | App credentials |
| `is_bhaptics_device_connected(device_index)` | Check if specific device is connected | Device index (0-9) |
| `ping(device_address)` | Ping specific device | Device address |
| `ping_all()` | Ping all devices | None |
| `set_device_vsm(device_address, vsm_value)` | Set vibration strength multiplier | Device address, VSM value |
| `swap_position(device_address)` | Swap device position | Device address |
| `retry_initialize(app_id, api_key)` | Retry SDK initialization | App credentials |

## License

This SDK is provided by bHaptics Inc. Check the official documentation for licensing terms.

## Support

- [Official Documentation](https://docs.bhaptics.com)
- [Developer Portal](https://developer.bhaptics.com)

## Contributing

This is a proprietary SDK. For feature requests or bug reports, please contact bHaptics support.
