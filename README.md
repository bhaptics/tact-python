### Sample code for python

### Prerequisite
* [bHaptics Hub App](https://play.google.com/store/apps/details?id=com.bhaptics.hub) is installed.
* Setup your project at the bHaptics Developer Portal: [Create haptic events using bHaptics Developer Portal](https://bhaptics.notion.site/Create-haptic-events-using-bHaptics-Developer-Portal-b056c5a56e514afeb0ed436873dd87c6).

### Conditions
* Tested under Python 3.9

### Dependencies
* requests


### Example Code
Here's a sample code snippet demonstrating how to use the bHaptics SDK with Python:

```python
import time
from bhaptics.haptic_player import BhapticsSDK2

sdk_instance = None


def on_play():
    sdk_instance.play_event("shoot_test")


if __name__ == '__main__':
    # Replace 'yourAppId' and 'yourApiKey' with your actual appId and apiKey
    appId = "yourAppId"
    apiKey = "yourApiKey"
    sdk_instance = BhapticsSDK2(appId, apiKey)
    try:
        while True:
            time.sleep(5)
            sdk_instance.play_event("shoot_test")
    except KeyboardInterrupt:
        print("Stopping the client...")
        sdk_instance.stop()

```

### Usage Instructions
* Install the required dependencies.

```
pip install -r requirements.txt
```

* Update the appId and apiKey in the code with your credentials.

Visit developer.bhaptics.com to create your own project.

* Execute the script, and it will periodically play haptic patterns every 5 seconds.
