import time
from bhaptics.haptic_player import BhapticsSDK2

sdk_instance = None


def on_play():
    sdk_instance.play_event("shoot_test")


if __name__ == '__main__':
    # Replace 'yourAppId' and 'yourApiKey' with your actual appId and apiKey
    appId = "mWK8BbDgpx9LdZVR22ij"
    apiKey = "m9ef4q9oQRXbPeJY9z4J"
    sdk_instance = BhapticsSDK2(appId, apiKey)
    try:
        while True:
            time.sleep(5)
            sdk_instance.play_event("shoot_test")
    except KeyboardInterrupt:
        print("Stopping the client...")
        sdk_instance.stop()
