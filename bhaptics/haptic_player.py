import random
import requests
from enum import Enum

import json
import time
import threading

if __name__ == '__main__':
    import udp_server as udp_server
    import tcp_client as tcp_client
else:
    import bhaptics.udp_server as udp_server
    import bhaptics.tcp_client as tcp_client

__client: tcp_client.TCPClient = None
__is_client_connected = False
__is_client_api_verified = False

__is_verbose = False

__ping_thread = None
__ping_thread_active = False

__conf = {
    "applicationId": "",
    "sdkApiKey": "",
}

def __print(*args, **kwargs):
    if __is_verbose:
        print(*args, **kwargs)

def __message_received(message):
    msg = json.loads(message)

    message_type = msg["type"]
    __print(f"\nreceived: ({message_type}) {message}")

    if message_type == "ServerTokenMessage":
        parsed_msg = json.loads(msg["message"])
        __check_api(parsed_msg["token"], parsed_msg["tokenKey"])

def __check_api(token, token_key):
    global __is_client_api_verified

    # Make the GET request
    host = "https://sdk-apis.bhaptics.com"
    url = f"{host}/api/v1/tacthub-api/verify?token={token}&token-key={token_key}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        __is_client_api_verified = True
        __print("Client api is verified!")
    else:
        __is_client_api_verified = False
        __print(f"Client api failed verification: {response.status_code}.")

def __udp_message_received(message, addr):
    sender_ip = addr[0]
    sender_port = addr[1]

    msg = json.loads(message)
    # __print(message, sender_ip, sender_port, msg["userId"])
    
    global __client, __is_client_connected, __is_verbose
    
    if __client is None:
        __client = tcp_client.TCPClient(
            sender_ip, 
            msg["port"], 
            message_received_callback=__message_received,
            verbose=__is_verbose
        )
        __client.start()
    
    while __client.is_connected() is False:
        __print("Waiting for client ...")
        __is_client_connected = False
        time.sleep(0.5)

    if __client.is_connected():
        __print("Client is connected!")
        __is_client_connected = True
        __client.send_message(__generate_message("SdkRequestAuthInit", __conf))
        time.sleep(0.5)
    
    udp_server.stop()

def __generate_message(message_type, message = None):
    if isinstance(message, str):
        msg = {
            "message": message,
            "type": message_type
        }
    else:
        msg = {
            "message": json.dumps(message),
            "type": message_type
        }
    return json.dumps(msg) + '\n'

def is_client_connected():
    global __is_client_connected
    return __is_client_connected

def is_client_api_verified():
    global __is_client_api_verified
    return __is_client_api_verified

def initialize(appId: str, apiKey: str, verbose: bool = False):
    global __conf, __is_verbose

    __is_verbose = verbose
    
    __conf = {
        "applicationId": appId,
        "sdkApiKey": apiKey,
    }
    
    udp_server.listen(callback=__udp_message_received, verbose=__is_verbose)

def destroy():
    global __client, __is_client_connected, __is_client_api_verified

    # For iOS Hub App, let server prepare for the disconnection
    if __client is not None:
        __ping_to_server()
    
    udp_server.stop()
    __client.stop()
    __is_client_connected = False
    __is_client_api_verified = False

def play_event(
        name,
        requestId:int|None = None,
        intensity:float = 1, 
        duration:float = 1, 
        offsetAngleX:float = 0, 
        offsetY:float = 0, 
    ):
    global __client

    if __client is None:
        return
    
    if requestId is None:
        requestId = random.randint(0, 999999)

    play_message = {
        "eventName": name,
        "requestId": requestId,
        "intensity": intensity,
        "duration": duration,
        "offsetAngleX": offsetAngleX,
        "offsetY": offsetY,
    }

    __client.send_message(__generate_message("SdkPlay", play_message))
    __ping_while_waiting()
    return requestId

class Position(Enum):
    VEST = 0
    FOREARM_L = 1
    FOREARM_R = 2
    HEAD = 3
    HAND_L = 4
    HAND_R = 5
    FOOT_L = 6
    FOOT_R = 7
    GLOVE_L = 8
    GLOVE_R = 9

def play_dot(
        position:Position,
        motorValues:list[int], # 40 motor values ranging from 0 to 100
        requestId:int|None = None,
        duration:int = 1000,
    ):
    global __client

    if __client is None:
        return
    
    if requestId is None:
        requestId = random.randint(0, 999999)

    play_message = {
        "requestId": requestId,
        "pos": position.value,
        "motors": motorValues,
        "durationMillis": duration,
    }

    __client.send_message(__generate_message("SdkPlayDotMode", play_message))
    __ping_while_waiting()
    return requestId

class GloveMode:
    def __init__(self, intensity: int = 0, playTime: int = 0, shape: int = 0):
        self.intensity = intensity
        self.playTime = playTime
        self.shape = shape
    
    def to_dict(self):
        # Convert to dictionary for JSON serialization
        return {
            "intensity": self.intensity,
            "playTime": self.playTime,
            "shape": self.shape,
        }

def play_glove(
        position:Position,
        gloveModes:list[GloveMode],
        requestId:int|None = None,
    ):
    global __client

    if __client is None:
        return
    
    if requestId is None:
        requestId = random.randint(0, 999999)

    motorValues = []
    playTimeValues = []
    shapeValues = []
    for mode in gloveModes:
        motorValues.append(mode.intensity)
        playTimeValues.append(mode.playTime)
        shapeValues.append(mode.shape)
    
    play_message = {
        "requestId": requestId,
        "pos": position.value,
        "motorValues": motorValues,
        "playTimeValues": playTimeValues,
        "shapeValues": shapeValues,
    }

    __client.send_message(__generate_message("SdkPlayWaveformMode", play_message))
    __ping_while_waiting()
    return requestId

class PathPoint:
    def __init__(self, x: float, y: float, intensity: int, motorCount: int = 3):
        self.x = max(0, min(x, 1))  # Ensure x is within [0, 1]
        self.y = max(0, min(y, 1))  # Ensure y is within [0, 1]
        self.intensity = max(0, min(intensity, 100))  # Ensure intensity is within [0, 100]
        self.motorCount = max(0, min(motorCount, 3))  # Ensure motorCount is within [0, 3]

    def to_dict(self):
        # Convert to dictionary for JSON serialization
        return {
            "x": self.x,
            "y": self.y,
            "intensity": self.intensity,
            "motorCount": self.motorCount,
        }

def play_path(
        position:Position,
        pathPoints:list[PathPoint],
        requestId:int|None = None,
        duration:int = 1000,
    ):
    global __client

    if __client is None:
        return
    
    if requestId is None:
        requestId = random.randint(0, 999999)
    
    x = []
    y = []
    intensity = []
    for point in pathPoints:
        x.append(point.x)
        y.append(point.y)
        intensity.append(point.intensity)

    play_message = {
        "requestId": requestId,
        "pos": position.value,
        "x": x,
        "y": y,
        "intensity": intensity,
        "durationMillis": duration,
    }

    __client.send_message(__generate_message("SdkPlayPathMode", play_message))
    __ping_while_waiting()
    return requestId

def play_loop(
        name,
        requestId:int|None = None,
        intensity:float = 1,
        duration:float = 1,
        interval:int = 0,
        maxCount:int = 0,
        offsetAngleX:float = 0,
        offsetY:float = 0,
    ):
    global __client

    if __client is None:
        return
    
    if requestId is None:
        requestId = random.randint(0, 999999)

    play_message = {
        "eventName": name,
        "requestId": requestId,
        "intensity": intensity,
        "duration": duration,
        "interval": interval,
        "maxCount": maxCount,
        "offsetAngleX": offsetAngleX,
        "offsetY": offsetY,
    }

    __client.send_message(__generate_message("SdkPlayLoop", play_message))
    __ping_while_waiting()
    return requestId

def __ping_while_waiting():
    global __ping_thread, __ping_thread_active

    def __ping_loop():
        global __ping_thread, __ping_thread_active

        try:
            while __ping_thread_active:
                time.sleep(1)
                __ping_to_server()
        except Exception as e:
            pass
        finally:
            __ping_thread_active = False

    # Halt the ping loop if it is active
    if __ping_thread_active:
        __ping_thread_active = False
    
    if __ping_thread is not None:
        __ping_thread.join()
        __ping_thread = None

    # Ping for every second to keep the Hub app alive (especially for iOS)
    __ping_thread = threading.Thread(target=__ping_loop)
    __ping_thread.start()

def __ping_to_server():
    __client.send_message(__generate_message("SdkPingToServer"))

def ping_all():
    __client.send_message(__generate_message("SdkPingAll"))
    __ping_while_waiting()


def stop_by_event(name: str):
    __client.send_message(__generate_message("SdkStopByEventId", name))
    __ping_while_waiting()


def stop_by_request(id: int):
    __client.send_message(__generate_message("SdkStopByRequestId", id))
    __ping_while_waiting()


def stop_all():
    __client.send_message(__generate_message("SdkStopAll"))
    __ping_while_waiting()


if __name__ == '__main__':
    # TODO: Replace `appId` and `apiKey` with values of your app
    appId = "mWK8BbDgpx9LdZVR22ij"
    apiKey = "m9ef4q9oQRXbPeJY9z4J"

    # Load `HelloFps` game
    initialize(
        appId = appId,
        apiKey = apiKey,
        verbose = False
    )
    
    print("1. Open TactHub app and connect with TactSuit x40.")
    print("2. Press the play button to start the server.")
    print()

    # Wait until client is connected
    while not is_client_connected():
        time.sleep(0.3)

    print("Python SDK connected to bHaptics Hub! Now verifying client...")

    # Wait for max 5 seconds until api gets verified
    wait_time = 0
    while not is_client_api_verified() and wait_time < 5:
        time.sleep(0.3)
        wait_time += 0.3

    print(f"Client verification: {is_client_api_verified()}")
    print()

    print("Testing: play_dot")
    play_dot(
        Position.VEST,
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
    time.sleep(2)

    print("Testing: play_path")
    play_path(
        Position.VEST,
        [PathPoint(0.2, 0.2, 100, 3), PathPoint(0.8, 0.8, 100, 3)],
        duration = 500
    )
    time.sleep(2)

    print("Testing: play_loop")
    play_loop(
        "shoot_test",
        interval = 1,
        maxCount = 5,
    )
    time.sleep(2)

    print("Testing: play_glove(L)")
    play_glove(
        position=Position.GLOVE_L,
        gloveModes=[GloveMode(100, 100, 2), GloveMode(100, 100, 0), GloveMode(100, 100, 1)]
    )
    time.sleep(2)

    print("Testing: play_glove(R)")
    play_glove(
        position=Position.GLOVE_R,
        gloveModes=[GloveMode(100, 100, 2), GloveMode(100, 100, 0), GloveMode(100, 100, 1)]
    )
    time.sleep(2)

    print("Testing: play_event")
    play_event("shoot_test")
    time.sleep(2)

    print()
    print("Test Finished")
    destroy()
