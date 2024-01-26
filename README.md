### Sample code for python

### Prerequisite
* bHaptics Beta App is installed.
* To get access, please contact developer@bhaptics.com.
* Setup your project at the bHaptics Developer Portal: [Create haptic events using bHaptics Developer Portal](https://bhaptics.notion.site/Create-haptic-events-using-bHaptics-Developer-Portal-b056c5a56e514afeb0ed436873dd87c6).

### Conditions
* Tested under Python 3.9

### Dependencies
* requests


### Example Code
Here's a sample code snippet demonstrating how to use the bHaptics SDK with Python:

```python
import keyboard
import time
from bhaptics.haptic_player import BhapticsSDK2

def on_space_pressed():
    sdk_instance.play_event("interaction-open-box")

def on_2_pressed():
    print("stop_by_event")
    sdk_instance.stop_by_event("interaction-open-box")

def on_1_pressed():
    print("play_event")
    sdk_instance.play_event("hit-rush", offset_angle_x=180)

if __name__ == '__main__':
    appId = "yourAppIdfromDeveloperPortal"
    apiKey = "yourApiKeyfromDeveloperPortal"
    sdk_instance = BhapticsSDK2(appId, apiKey)
    try:
        keyboard.add_hotkey('space', on_space_pressed)
        keyboard.add_hotkey('1', on_1_pressed)
        keyboard.add_hotkey('2', on_2_pressed)
        print("Press space to play")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the client...")
        sdk_instance.stop()
    finally:
        keyboard.remove_hotkey('space')
        keyboard.remove_hotkey('1')
        keyboard.remove_hotkey('2')
    print("Client stopped.")

```

### Usage Instructions
* Install the required dependencies.

```
pip install -r requirements.txt
```

* Update the appId and apiKey in the code with your credentials.

Visit developer.bhaptics.com to create your own project.

* Execute the script, and it will periodically play haptic patterns every 5 seconds.