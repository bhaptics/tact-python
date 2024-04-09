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
        time.sleep(3)

        while True:
            print("\nPlay haptic samples!!!")

            # Play Dot Mode - sample 1
            print("Play Dot Mode - sample 1")
            sdk_instance.play_dot_mode(
                [
                    # Front side
                    20, 20, 20, 20,
                    20, 20, 20, 20,
                    20, 20, 20, 20,
                    20, 20, 20, 20,
                    20, 20, 20, 20,

                    # Back side
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                ]
            )
            time.sleep(5)

            # Play Dot Mode - sample 2
            print("Play Dot Mode - sample 2")
            sdk_instance.play_dot_mode(
                [
                    # Front side
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,

                    # Back side
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    100, 100, 100, 100,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                ],
                duration=3
            )
            time.sleep(5)


            # Play Path Mode - sample
            print("Play Path Mode - sample")
            for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
                sdk_instance.play_path_mode(
                    x_list=[i],
                    y_list=[0.5],
                    intensity_list=[5],
                    duration=1
                )

                time.sleep(0.5)

            time.sleep(5)


            # Play an "shoot_test" event.
            print("Play an shoot_test event.")
            sdk_instance.play_event("shoot_test")
            time.sleep(5)

            # Play an "shoot_test" event with duration to double.
            print("Play an shoot_test event with duration to double.")
            sdk_instance.play_event("shoot_test", duration=2)
            time.sleep(5)

            # Play an "shoot_test" event, and stop all event.
            print("Play an shoot_test event, and stop all event.")
            sdk_instance.play_event("shoot_test", duration=2)
            time.sleep(0.2)
            sdk_instance.stop_all()
            time.sleep(5)


            # Repeat the event 3 times
            print("Repeat the event 3 times")
            sdk_instance.play_loop("shoot_test", interval=1, maxCount=3)
            time.sleep(5)


            print("Cooldown....")
            time.sleep(10)
    
    except KeyboardInterrupt:
        print("Stopping the client...")
        sdk_instance.stop()

    finally:
        print("Finally...")

    print("Client stopped.")
