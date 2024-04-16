import time

import bhaptics.haptic_player as player

if __name__ == '__main__':
    # TODO: Replace `appId` and `apiKey` with values of your app
    appId = "mWK8BbDgpx9LdZVR22ij"
    apiKey = "m9ef4q9oQRXbPeJY9z4J"

    # Load your app
    player.initialize(
        appId = appId,
        apiKey = apiKey,
        verbose = False
    )
    
    print("1. Open TactHub app and connect with TactSuit x40.")
    print("2. Press the play button to start the server.")
    print()

    # Wait until client is connected
    while not player.is_client_connected():
        time.sleep(0.3)

    print("Python SDK connected to bHaptics Hub! Now verifying client...")

    # Wait for max 5 seconds until api gets verified
    wait_time = 0
    while not player.is_client_api_verified() and wait_time < 5:
        time.sleep(0.3)
        wait_time += 0.3

    print(f"Client verification: {player.is_client_api_verified()}")
    print()

    print("\nPlay haptic samples!!!")

    # Play Dot Mode - sample 1
    print("Play Dot Mode - sample 1")
    player.play_dot(
        player.Position.VEST,
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
        ],
        duration = 3000
    )
    time.sleep(5)

    # Play Dot Mode - sample 2
    print("Play Dot Mode - sample 2")
    player.play_dot(
        player.Position.VEST,
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
        duration = 3000
    )
    time.sleep(5)

    # Play Path Mode - sample
    print("Play Path Mode - sample")
    for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        player.play_path(
            player.Position.VEST,
            [player.PathPoint(x=i, y=0.5, intensity=5)],
            duration = 500
        )
        time.sleep(0.5)
    time.sleep(5)

    # Play "shoot_test" event.
    print("Play `shoot_test` event.")
    player.play_event("shoot_test")
    time.sleep(5)

    # Play "shoot_test" event with its duration doubled.
    print("Play `shoot_test` event with its duration doubled.")
    player.play_event("shoot_test", duration=2)
    time.sleep(5)

    # Start playing "shoot_test" event and stop all events immediately.
    print("Start playing `shoot_test` event and stop all events immediately.")
    player.play_event("shoot_test", duration=2)
    time.sleep(0.2)
    player.stop_all()
    time.sleep(5)

    # Repeat "shoot_test" event 3 times.
    print("Repeat `shoot_test` event 3 times.")
    player.play_loop("shoot_test", interval=1, maxCount=3)
    time.sleep(5)

    print("Testing: play_glove(L)")
    player.play_glove(
        position=player.Position.GLOVE_L,
        gloveModes=[
            player.GloveMode(100, 100, 2),
            player.GloveMode(100, 100, 0),
            player.GloveMode(100, 100, 1)
        ]
    )
    time.sleep(2)

    print("Testing: play_glove(R)")
    player.play_glove(
        position=player.Position.GLOVE_R,
        gloveModes=[
            player.GloveMode(100, 100, 2),
            player.GloveMode(100, 100, 0),
            player.GloveMode(100, 100, 1)
        ]
    )
    time.sleep(2)

    player.destroy()
    print("Client stopped.")
