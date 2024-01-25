import keyboard
import time
from bhaptics.haptic_player import BhapticsSDK2

sdk_instance = None


def on_space_pressed():
    sdk_instance.play_event("interaction-open-box")


def on_2_pressed():
    print("stop_by_event")
    sdk_instance.stop_by_event("interaction-open-box")


def on_1_pressed():
    print("play_event")
    sdk_instance.play_event("hit-rush", offset_angle_x=180)


if __name__ == '__main__':
    # sdk_instance = BhapticsSDK2("yourAppId", "yourApiKey")
    appId = "appId"
    apiKey = "apiKey"
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
    print("Client stopped.")
