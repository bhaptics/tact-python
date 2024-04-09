# Python SDK for bHaptics Hub

## Prerequisites
- One or more bHaptics TactSuit devices (e.g., X40, X16).
- A mobile device with bHaptics Hub App ([Android](https://bit.ly/bhaptics-hub-android)) installed.
- A haptic project deployed in [bHaptics Developer Portal](https://developer.bhaptics.com/).
  - [How to Create Projects](#how-to-create-projects)

### Conditions
- Tested under Python 3.9

### Dependencies
- requests

## Getting started
1. Connect a mobile device and a desktop to the network under the same Wi-Fi.
2. Clone this repository on your desktop and install the required dependencies inside the directory.
    ```bash
    pip3 install -r requirements.txt
    ```
3. Install bHaptics Hub App on your mobile device - [Android](https://bit.ly/bhaptics-hub-android).
4. Connect your TactSuit with bHaptics Hub App - [bHaptics Hub Guide](https://bit.ly/bHaptics-Hub-Guide).
5. Press the start button on the app.
6. Run the sample code inside your desktop.
    ```bash
    python3 sample.py
    ```

## Example
This example demonstrates how to use the bHaptics SDK with Python:

```python
import time
from bhaptics.haptic_player import BhapticsSDK2

sdk_instance = None

if __name__ == '__main__':
    # Replace `yourAppId` and `yourApiKey` with values of your own project
    appId = "yourAppId"
    apiKey = "yourApiKey"
    sdk_instance = BhapticsSDK2(appId, apiKey)
    try:
        while True:
            time.sleep(5)
            # Replace `shoot_test` with event name of your own project
            sdk_instance.play_event("shoot_test")
    except KeyboardInterrupt:
        print("Stopping the client...")
        sdk_instance.stop()

```

## How to Create Projects
- Visit [bHaptics Developer Portal](https://developer.bhaptics.com/).
- Create your own project with one or more haptic patterns: [refer to this guide for details](https://bhaptics.notion.site/Create-haptic-events-using-bHaptics-Developer-Portal-b056c5a56e514afeb0ed436873dd87c6).
- Save the haptic patterns and deploy the project.
- Go to Settings page and check the `appId` and `apiKey` of your project.
- Update the `appId` and `apiKey` in the code with your project.

