# import keyboard
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
        print("Play 'shoot_test' event")
        time.sleep(3)

        while True:
            # sdk_instance.play_dot_mode(
            #     [
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,

            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #         30, 30, 30, 30,
            #     ]
            # )
            # time.sleep(5)

            # sdk_instance.play_dot_mode(
            #     [
            #         0, 0, 0, 0,
            #         0, 0, 0, 0,
            #         50, 50, 50, 50,
            #         0, 0, 0, 0,
            #         0, 0, 0, 0,

            #         0, 0, 0, 0,
            #         0, 0, 0, 0,
            #         0, 0, 0, 0,
            #         0, 0, 0, 0,
            #         0, 0, 0, 0,
            #     ],
            #     duration=3
            # )
            # time.sleep(5)

            sdk_instance.play_path_mode(
                x_list=[0.0, 1.0, 0.5],
                y_list=[0.0, 1.0, 0.5],
                intensity_list=[20, 100, 20],
                duration=2
            )
            time.sleep(5)


            # sdk_instance.play_event("shoot_test")
            # time.sleep(5)

            # sdk_instance.play_event("shoot_test", duration=2)
            # time.sleep(5)

            # sdk_instance.play_event("shoot_test", duration=2)
            # time.sleep(0.2)
            # sdk_instance.stop_all()
            # time.sleep(5)
    
    except KeyboardInterrupt:
        print("Stopping the client...")
        sdk_instance.stop()

    finally:
        print("Finally...")

    print("Client stopped.")
