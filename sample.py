from time import sleep
from bhaptics import haptic_player


player = haptic_player.HapticPlayer()
sleep(0.1)

# tact file can be exported from bhaptics designer
player.register("BowShoot", "BowShoot.tact")

sleep(0.1)
player.submit_registered("BowShoot")
sleep(2)

interval = 0.5
durationMillis = 100

for i in range(20):
    print(i, "back")
    player.submit_dot("backFrame", "VestBack", [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

    print(i, "front")
    player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

