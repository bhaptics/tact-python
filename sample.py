from time import sleep
from bhaptics import haptic_player


player = haptic_player.HapticPlayer()
sleep(0.4)

# tact file can be exported from bhaptics designer
print("register CenterX")
player.register("CenterX", "CenterX.tact")
print("register Circle")
player.register("Circle", "Circle.tact")

sleep(0.3)
print("submit CenterX")
player.submit_registered("CenterX")
sleep(4)
print("submit Circle")
player.submit_registered_with_option("Circle", "alt",
                                     scale_option={"intensity": 1, "duration": 1},
                                     rotation_option={"offsetAngleX": 180, "offsetY": 0})
print("submit Circle With Diff AltKey")
player.submit_registered_with_option("Circle", "alt2",
                                     scale_option={"intensity": 1, "duration": 1},
                                     rotation_option={"offsetAngleX": 0, "offsetY": 0})
sleep(3)

interval = 0.5
durationMillis = 100

for i in range(20):
    print(i, "back")
    player.submit_dot("backFrame", "VestBack", [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

    print(i, "front")
    player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

