# bHaptics Python SDK2

A Python library for implementing haptic feedback using the bHaptics SDK2.

## 🔧 Requirements

### Required Software
- **bHaptics Player**: Download and install the PC player from the [official download page](https://www.bhaptics.com/support/downloads)
- **Python 3.9**: Currently supported Python version

### Developer Account Setup
- **bHaptics Portal**: Create a workspace on the [developer portal](https://developer.bhaptics.com/)
- For detailed setup instructions, refer to the [official documentation](https://docs.bhaptics.com/portal/)

## 📦 Installation

```bash
pip install bhaptics-python
```

## 🚀 Quick Start

### Basic Initialization

```python
import bhaptics_python
import asyncio

async def main():
    app_id = "your_app_id"        # App ID created in bHaptics Portal
    api_key = "your_api_key"      # API key created in bHaptics Portal
    
    # Initialize SDK
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
    print(f"Initialization result: {result}")
    
    # Check connection status
    is_connected = await bhaptics_python.is_connected()
    print(f"Connection status: {is_connected}")

asyncio.run(main())
```

## 📖 Function Reference

### 🔗 Connection and Initialization

#### `registry_and_initialize(app_id, api_key, app_name)`
Initializes the SDK and establishes connection with bHaptics Player.

**Parameters:**
- `app_id`: Application ID created in bHaptics Portal
- `api_key`: API key created in bHaptics Portal
- `app_name`: Application name (optional)

**Returns:** Initialization success status

#### `is_connected()`
Checks the connection status with bHaptics Player.

#### `retry_initialize(app_id, api_key)`
Attempts to reinitialize the connection if disconnected.

#### `close()`
Closes the SDK connection.

### 🎮 Haptic Playback Functions

#### `play_event(event_name)`
Plays a predefined haptic event.

**Parameters:**
- `event_name`: Event name created in bHaptics Portal

**Returns:** Request ID

```python
request_id = await bhaptics_python.play_event("HeartBeat")
print(f"Playback request ID: {request_id}")
```

#### `play_position(event_name, position)`
Plays a haptic event at a specific position.

**Parameters:**
- `event_name`: Event name
- `position`: Playback position (0-9, each number represents a body part)

#### `play_position_with_parameter(event_name, position, scale_option, intensity, duration, x_offset, y_offset)`
Plays a haptic event with custom parameters.

**Parameters:**
- `scale_option`: Scale option
- `intensity`: Intensity (0.0-1.0)
- `duration`: Playback duration (milliseconds)
- `x_offset`, `y_offset`: X, Y coordinate offsets

#### `play_dot(position, duration_millis, values)`
Plays dot patterns by directly controlling individual motors.

**Parameters:**
- `position`: Device position
- `duration_millis`: Playback duration (milliseconds)
- `values`: Array of motor intensities (0-100)

```python
# Sequentially activate 40 motors
motor_len = 40
values = [0 for _ in range(motor_len)]

for i in range(motor_len):
    values[i] = 40
    if i > 0:
        values[i - 1] = 0
    
    request_id = await bhaptics_python.play_dot(0, 1000, values)
    time.sleep(1)
```

#### `play_path(position, duration_millis, x, y, intensity)`
Plays haptic effects along a path.

**Parameters:**
- `x`, `y`: Path coordinate arrays (0.0-1.0)
- `intensity`: Intensity array for each point

#### `play_glove(position, motors, playtimes, shapes, repeat_count)`
Controls glove-type haptic devices.

**Parameters:**
- `position`: Device position (8: left hand, 9: right hand)
- `motors`: Array of motor intensities
- `playtimes`: Array of playback times for each motor
- `shapes`: Array of waveform shapes for each motor
- `repeat_count`: Number of repetitions

#### `play_loop(event_name, scale_option, intensity, duration, x_offset, y_offset, interval, max_count)`
Plays haptic events in a loop.

**Parameters:**
- `interval`: Repetition interval (milliseconds)
- `max_count`: Maximum number of repetitions

#### `play_without_result(event_name, position, scale_option, intensity, duration, x_offset, y_offset)`
Plays haptic events without waiting for results (fire-and-forget).

### ⏹️ Playback Control

#### `stop_by_request_id(request_id)`
Stops haptic playback for a specific request ID.

#### `stop_by_event_name(event_name)`
Stops all haptic playback for a specific event name.

#### `stop_all()`
Stops all haptic playback.

### 📊 Status Checking

#### `is_playing_event_by_request_id(request_id)`
Checks the playback status of a specific request ID.

#### `is_playing_event_by_event_id(event_name)`
Checks the playback status of a specific event.

#### `is_playing_event()`
Checks the overall haptic playback status.

#### `is_bhaptics_device_connected(position)`
Checks the connection status of a device at a specific position.

**Parameters:**
- `position`: Device position to check (0-9)

```python
# Check connection status for all positions
for i in range(10):
    is_connected = await bhaptics_python.is_bhaptics_device_connected(i)
    print(f"Position {i} device connection: {is_connected}")
```

### 🔧 Device Control

#### `ping(device_address)`
Sends a ping to a specific device.

#### `ping_all()`
Sends a ping to all connected devices.

#### `set_device_vsm(device_address, value)`
Sets the VSM (Vibration Strength Multiplier) value for a device.

#### `swap_position(device_address)`
Swaps the position of a device.

### 📱 Windows-Only Functions

The following functions are **only available on Windows**:

#### `is_bhaptics_player_running()`
Checks if bHaptics Player is currently running.

#### `is_bhaptics_player_installed()`
Checks if bHaptics Player is installed.

#### `run_bhaptics_player(show_ui)`
Launches bHaptics Player.

**Parameters:**
- `show_ui`: Whether to show the UI (True/False)

```python
# Only available on Windows
if platform.system() == "Windows":
    # Check if Player is installed
    is_installed = await bhaptics_python.is_bhaptics_player_installed()
    print(f"bHaptics Player installed: {is_installed}")
    
    # Check if Player is running
    is_running = await bhaptics_python.is_bhaptics_player_running()
    print(f"bHaptics Player running: {is_running}")
    
    # Launch Player (hide UI)
    if not is_running:
        await bhaptics_python.run_bhaptics_player(False)
```

### 📄 Information Retrieval

#### `get_event_time(event_name)`
Retrieves the playback time of an event.

#### `get_device_info_json()`
Returns connected device information in JSON format.

#### `get_haptic_mappings_json()`
Returns haptic mapping information in JSON format.

#### `get_haptic_messages(app_id, api_key, app_version)`
Retrieves haptic messages.

#### `get_haptic_mappings(app_id, api_key, app_version)`
Retrieves haptic mappings.

## 💡 Complete Example Code

```python
import bhaptics_python
import asyncio
import time
import platform

async def haptic_demo():
    # 1. Initialization
    app_id = "your_app_id"
    api_key = "your_api_key"
    
    print("🔧 Initializing bHaptics SDK...")
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
    print(f"Initialization result: {result}")
    
    # 2. Check connection status
    is_connected = await bhaptics_python.is_connected()
    if not is_connected:
        print("❌ Cannot connect to bHaptics Player.")
        return
    
    print("✅ Connected to bHaptics Player.")
    
    # 3. Check device information
    device_info = await bhaptics_python.get_device_info_json()
    print(f"📱 Connected device info: {device_info}")
    
    # 4. Test haptic effects
    print("\n🎮 Starting haptic effect tests...")
    
    # Play dot pattern
    print("• Playing dot pattern")
    values = [50] * 20 + [0] * 20  # Activate first 20 of 40 motors
    await bhaptics_python.play_dot(0, 2000, values)
    await asyncio.sleep(2.5)
    
    # Play path pattern
    print("• Playing path pattern")
    x = [0.2, 0.4, 0.6, 0.8]
    y = [0.2, 0.8, 0.2, 0.8]
    intensity = [80, 60, 80, 60]
    await bhaptics_python.play_path(0, 3000, x, y, intensity)
    await asyncio.sleep(3.5)
    
    # Test glove haptics (if available)
    print("• Testing glove haptics")
    glove_motors = [100] * 8
    glove_playtimes = [500] * 8
    glove_shapes = [2] * 8
    
    # Left hand
    await bhaptics_python.play_glove(8, glove_motors, glove_playtimes, glove_shapes, 0)
    await asyncio.sleep(1)
    
    # Right hand
    await bhaptics_python.play_glove(9, glove_motors, glove_playtimes, glove_shapes, 0)
    await asyncio.sleep(1)
    
    # 5. Cleanup
    await bhaptics_python.stop_all()
    await bhaptics_python.close()
    print("🔚 Demo completed")

# Run the demo
if __name__ == "__main__":
    asyncio.run(haptic_demo())
```

## 🎯 Interactive Example

Here's the complete interactive example from the original sample code with explanations:

```python
import bhaptics_python
import asyncio
import time

async def interactive_demo():
    print("bHaptics Python SDK2 Interactive Demo")
    
    # Initialize (replace with your credentials)
    app_id = ""
    api_key = ""
    
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "")
    print(f"Initialization: {result}")

    while True:
        print("\nAvailable commands:")
        print("p - Play event | s - Stop by request ID | o - Stop by event name")
        print("a - Stop all | d - Play dot pattern | path - Play path pattern")
        print("g - Play glove pattern | ping/pinga - Ping device(s)")
        print("i - Check playing status | json - Get device info")
        print("position - Check all device connections | loop - Play loop")
        print("running/install - Check Player status (Windows only)")
        print("q - Quit")
        
        user_input = input("\nEnter command: ").strip()
        
        if user_input == 'q':
            print("Exiting demo...")
            break
        elif user_input == 'p':
            # Play predefined event
            event_name = input("Enter event name: ")
            request_id = await bhaptics_python.play_event(event_name)
            print(f"Playing {event_name}, request ID: {request_id}")
            
        elif user_input == 's':
            # Stop by request ID
            request_id = int(input("Enter request ID to stop: "))
            await bhaptics_python.stop_by_request_id(request_id)
            print(f"Stopped request ID: {request_id}")
            
        elif user_input == 'a':
            # Stop all haptic effects
            await bhaptics_python.stop_all()
            print("All haptic effects stopped")
            
        elif user_input == 'd':
            # Play sequential dot pattern
            print("Playing sequential dot pattern...")
            motor_len = 40
            values = [0 for _ in range(motor_len)]
            
            for i in range(motor_len):
                values[i] = 40
                if i > 0:
                    values[i - 1] = 0
                await bhaptics_python.play_dot(0, 100, values)
                time.sleep(0.1)
                
        elif user_input == 'path':
            # Play predefined path pattern
            print("Playing path pattern...")
            x = [0.738, 0.723, 0.709, 0.696, 0.682, 0.667, 0.653]
            y = [0.68, 0.715, 0.749, 0.782, 0.816, 0.852, 0.885]
            intensity = [40] * len(x)
            
            for i in range(len(x)):
                await bhaptics_python.play_path(0, 200, [x[i]], [y[i]], [intensity[i]])
                time.sleep(0.2)
                
        elif user_input == 'g':
            # Play glove pattern
            print("Playing glove patterns...")
            motors = [100] * 8
            playtimes = [200] * 8
            shapes = [2] * 8
            
            # Left hand
            for _ in range(3):
                await bhaptics_python.play_glove(8, motors, playtimes, shapes, 0)
                time.sleep(0.3)
            
            # Right hand
            for _ in range(3):
                await bhaptics_python.play_glove(9, motors, playtimes, shapes, 0)
                time.sleep(0.3)
                
        elif user_input == 'i':
            # Check playing status
            playing = await bhaptics_python.is_playing_event()
            print(f"Any haptic effect playing: {playing}")
            
        elif user_input == 'json':
            # Get device information
            device_info = await bhaptics_python.get_device_info_json()
            mappings = await bhaptics_python.get_haptic_mappings_json()
            print(f"Device info: {device_info}")
            print(f"Haptic mappings: {mappings}")
            
        elif user_input == 'position':
            # Check all device positions
            print("Checking all device positions...")
            for i in range(10):
                connected = await bhaptics_python.is_bhaptics_device_connected(i)
                if connected:
                    print(f"✅ Position {i}: Connected")
                else:
                    print(f"❌ Position {i}: Not connected")
                    
        elif user_input == 'running':
            # Windows only - check if Player is running
            if platform.system() == "Windows":
                running = await bhaptics_python.is_bhaptics_player_running()
                print(f"bHaptics Player running: {running}")
            else:
                print("This command is only available on Windows")
                
        elif user_input == 'install':
            # Windows only - check if Player is installed
            if platform.system() == "Windows":
                installed = await bhaptics_python.is_bhaptics_player_installed()
                print(f"bHaptics Player installed: {installed}")
            else:
                print("This command is only available on Windows")
                
        else:
            print(f"Unknown command: {user_input}")
    
    # Cleanup
    await bhaptics_python.close()

# Run the interactive demo
if __name__ == "__main__":
    asyncio.run(interactive_demo())
```

## 🐛 Troubleshooting

### Connection Issues
- Ensure bHaptics Player is running
- Check firewall settings
- Use the `retry_initialize()` function
- Verify your app_id and api_key are correct

### Haptic Effects Not Playing
- Verify device is properly connected
- Use `is_bhaptics_device_connected()` to check device status
- Check device battery level
- Ensure the device is properly paired in bHaptics Player

### Windows-Only Function Errors
- These functions only work on Windows
- On other operating systems, manually launch bHaptics Player
- Use `platform.system()` to check the operating system before calling these functions

### Performance Issues
- Avoid calling haptic functions too frequently
- Use `play_without_result()` for fire-and-forget operations
- Consider using `play_loop()` instead of repeated `play_event()` calls

## 📚 Additional Resources

- [bHaptics Official Documentation](https://docs.bhaptics.com/)
- [bHaptics Portal](https://developer.bhaptics.com/)
- [bHaptics Community](https://www.bhaptics.com/support/)
- [Python SDK API Reference](https://docs.bhaptics.com/python/)

## 🤝 Contributing

When contributing to this project:
1. Test your changes with actual bHaptics hardware
2. Ensure compatibility with Python 3.9+
3. Follow the existing code style and documentation format
4. Test on both Windows and non-Windows platforms where applicable

## 📄 License

This library follows bHaptics' official licensing policy. Please refer to the bHaptics developer agreement for detailed licensing information.