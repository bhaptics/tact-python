# Sample code for python

## Prerequisite
- One or more TactSuits (X40, X16, and so on)
- bHaptics Hub App ([android](https://bit.ly/bhaptics-hub-android)) is installed.
- Setup your project at the bHaptics Developer Portal: [Create haptic events using bHaptics Developer Portal](https://bhaptics.notion.site/Create-haptic-events-using-bHaptics-Developer-Portal-b056c5a56e514afeb0ed436873dd87c6).

### Conditions
- Tested under Python 3.9

### Dependencies
- requests

## Getting started with sample code
1. Install bHaptics Hub App - [android](https://bit.ly/bhaptics-hub-android)
2. Setup bHaptics Hub App with your TactSuit - [bHaptics Hub Guide](https://bit.ly/bHaptics-Hub-Guide)
3. Go source directory and install the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
4. Run sample code
    ```bash
    python sample.py
    ```

## Example Code
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

## Next
- Visit [developer.bhaptics.com](https://developer.bhaptics.com/) to create your own project.
- Update the appId and apiKey in the code with your credentials.

