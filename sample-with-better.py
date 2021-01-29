from time import sleep
from bhaptics import better_haptic_player as player
import keyboard

player.initialize()

# tact file can be exported from bhaptics designer
print("register CenterX")
player.register("CenterX", "CenterX.tact")
print("register Circle")
player.register("Circle", "Circle.tact")

interval = 0.5
durationMillis = 100



for i in range(20):
    print(i, "back")
    player.submit_dot("backFrame", "VestBack", [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

    print(i, "front")
    player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)


def play(index):
    if index == 1:
        print("submit CenterX")
        player.submit_registered("CenterX")
    elif index == 2:
        print("submit Circle")
        player.submit_registered_with_option("Circle", "alt",
                                             scale_option={"intensity": 1, "duration": 1},
                                             rotation_option={"offsetAngleX": 180, "offsetY": 0})
    elif index == 3:
        print("submit Circle With Diff AltKey")
        player.submit_registered_with_option("Circle", "alt2",
                                             scale_option={"intensity": 1, "duration": 1},
                                             rotation_option={"offsetAngleX": 0, "offsetY": 0})


def run():
    # sleep(0.5)
    # play(1)
    # sleep(0.5)

    print("Press Q to quit")
    while True:
        key = keyboard.read_key()
        if key == "q" or key == "Q":
            break
        elif key == "1":
            play(1)
        elif key == "2":
            play(3)
        elif key == "3":
            play(3)


        print('=================================================')
        print('is_playing', player.is_playing())
        print('is_playing_key(CenterX)', player.is_playing_key('CenterX'))
        print('is_device_connected(Vest)', player.is_device_connected('Vest'))
        print('is_device_connected(ForearmL)', player.is_device_connected('ForearmL'))
        print('=================================================')


if __name__ == "__main__":
    run()
