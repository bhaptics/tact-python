import json
from time import sleep
from websocket import create_connection

class HapticPlayer:
    def __init__(self):
        try:
            self.ws = create_connection("ws://localhost:15881/v2/feedbacks")
        except:
            print("Couldn't connect")
            return

    def register(self, file_directory):
        json_data = open(file_directory).read()

        data = json.loads(json_data)
        project = data["project"]

        layout = project["layout"]
        tracks = project["tracks"]

        request = {
            "Register": [{
                "Key": "BowShoot",
                "Project": {
                    "Tracks": tracks,
                    "Layout": layout
                }
            }]
        }

        json_str = json.dumps(request)
        self.ws.send(json_str)

    def submit_registered(self, key):
        submit = {
            "Submit": [{
                "Type": "key",
                "Key": "BowShoot"
            }]
        }

        json_str = json.dumps(submit);

        self.ws.send(json_str)

    def submit(self, key, frame):
        submit = {
            "Submit": [{
                "Type": "frame",
                "Key": key,
                "Frame": frame
            }]
        }

        json_str = json.dumps(submit);

        self.ws.send(json_str)

    def __del__(self):
        self.ws.close()


player = HapticPlayer()
sleep(0.1)

player.register("BowShoot.tact")

sleep(0.1)
player.submit_registered("BowShoot")
sleep(2)


# send individual point for 1 seconds
dotFrame = {
    "Position": "Left",
    "DotPoints": [{
        "Index": 0,
        "Intensity": 100
    }, {
        "Index": 3,
        "Intensity": 50
    }],
    "DurationMillis": 1000
}
player.submit("dotPoint", dotFrame)
sleep(2)

pathFrame = {
    "Position": "VestFront",
    "PathPoints": [{
        "X": "0.5",
        "Y": "0.5",
        "Intensity": 100
    }, {
        "X": "0.3",
        "Y": "0.3",
        "Intensity": 50
    }],
    "DurationMillis": 1000
}
player.submit("pathPoint", pathFrame)
sleep(2)


print('Press Ctrl-C to Stop')
try:
    while True:
        a = 1
except KeyboardInterrupt:
    pass
