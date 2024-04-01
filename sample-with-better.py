from time import sleep
from bhaptics import better_haptic_player as player
from bhaptics.better_haptic_player import BhapticsPosition
import keyboard

player.initialize()

# tact file can be exported from bhaptics designer
print("register CenterX")
player.register("CenterX", "CenterX.tact")
print("register Circle")
player.register("Circle", "Circle.tact")

interval = 0.5
durationMillis = 100



x = [0.738,0.723,0.709,0.696,0.682,0.667,0.653,0.639,0.624,0.611,0.597,0.584,0.57,0.557,0.542,0.528,0.515,0.501,0.487,0.474,0.46,0.447,0.432,0.419,0.406,0.393,0.378,0.365,0.352,0.338,0.324,0.311,0.297]
y = [0.68,0.715,0.749,0.782,0.816,0.852,0.885,0.921,0.956,0.952,0.918,0.885,0.848,0.816,0.779,0.743,0.71,0.673,0.639,0.606,0.571,0.537,0.5,0.467,0.434,0.4,0.363,0.329,0.296,0.261,0.226,0.192,0.157]


player.submit_path("backFramePath", BhapticsPosition.VestBack.value, [
    {"x": x[0], "y": y[0], "intensity": 100},
    {"x": x[1], "y": y[1], "intensity": 100},
    {"x": x[2], "y": y[2], "intensity": 100},
    {"x": x[3], "y": y[3], "intensity": 100},
    {"x": x[4], "y": y[4], "intensity": 100},
    {"x": x[5], "y": y[5], "intensity": 100},
    ], durationMillis)
sleep(interval)

player.submit_path("frontFramePath", BhapticsPosition.VestFront.value, [
    {"x": x[0], "y": y[0], "intensity": 100},
    {"x": x[1], "y": y[1], "intensity": 100},
    {"x": x[2], "y": y[2], "intensity": 100},
    ], durationMillis)
sleep(interval)


for i in range(len(x)):
    print(i, "back")
    player.submit_path("backFramePath", BhapticsPosition.VestBack.value, [{"x": x[i], "y": y[i], "intensity": 100}], durationMillis)
    sleep(interval)

    print(i, "front")
    player.submit_path("frontFramePath", BhapticsPosition.VestFront.value, [{"x": x[i], "y": y[i], "intensity": 100}], durationMillis)
    sleep(interval)
sleep(3)


for i in range(20):
    print(i, "back")
    player.submit_dot("backFrame", BhapticsPosition.VestBack.value, [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

    print(i, "front")
    player.submit_dot("frontFrame", BhapticsPosition.VestFront.value, [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

for i in range(6):
    print(i, "Glove Left")
    player.submit_dot("gloveLFrame", BhapticsPosition.GloveL.value, [{"index": i, "intensity": 100}], durationMillis)
    sleep(interval)

    print(i, "Glove Right")
    player.submit_dot("gloveRFrame", BhapticsPosition.GloveR.value, [{"index": i, "intensity": 100}], durationMillis)
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
        print('is_device_connected(Vest)', player.is_device_connected(BhapticsPosition.Vest.value))
        print('is_device_connected(ForearmL)', player.is_device_connected(BhapticsPosition.ForearmL.value))
        print('=================================================')


if __name__ == "__main__":
    run()
