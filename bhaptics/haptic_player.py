import json
import time
import requests
import bhaptics.udp_server
import bhaptics.tcp_client
import keyboard
import random

# Constants and Configuration
API_URL = "https://sdk-apis.bhaptics.com/api/v1/tacthub-api/verify"


# Helper Functions
def send_request(url, params):
    """Send a GET request and return the response."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


def generate_message(message_type, message):
    """Generate a JSON message."""
    msg = {"message": json.dumps(message), "type": message_type}
    return json.dumps(msg) + '\n'


def generate_string_message(message_type, message):
    """Generate a JSON message."""
    msg = {"message": message, "type": message_type}
    return json.dumps(msg) + '\n'


def random_request_id():
    return random.randint(1, 99999)


# Main Functionalities
class BhapticsSDK2:
    def __init__(self, appId, apiKey):
        self.appId = appId
        self.apiKey = apiKey
        self.client = None
        self.start()

    def start(self):
        bhaptics.udp_server.listen(callback=self.udp_message_received)

    def stop(self):
        if self.client:
            self.client.stop()

    def udp_message_received(self, message, addr):
        """Handle UDP messages."""
        msg = json.loads(message)
        print(f"Received UDP message from {addr[0]}:{addr[1]} - {msg}")

        if self.client is None:
            self.client = bhaptics.tcp_client.TCPClient(addr[0], msg["port"],
                                                        message_received_callback=self.message_received)
            self.client.start()

        self.wait_for_client_connection()
        self.send_auth_request()
        bhaptics.udp_server.stop()

    def wait_for_client_connection(self):
        """Wait until the client is connected."""
        while not self.client.status():
            print("Waiting for client to connect...")
            time.sleep(1)

    def send_auth_request(self):
        """Send authentication request to the client."""
        config = {
            "applicationId": self.appId,
            "sdkApiKey": self.apiKey,
        }

        auth_message = generate_message("SdkRequestAuthInit", config)
        self.client.send_message(auth_message)

    def message_received(self, message):
        """Handle TCP messages."""
        msg = json.loads(message)
        print(f"Received TCP message: {msg}")
        message_type = msg["type"]
        print(f"Received TCP type: {message_type}")

        if message_type == "ServerTokenMessage":
            message_message = msg["message"]
            parsed_message = json.loads(message_message)
            token = parsed_message["token"]
            token_key = parsed_message["tokenKey"]
            self.verify_token(token, token_key)

    def verify_token(self, token, token_key):
        """Verify the token with the API."""
        params = {"token": token, "token-key": token_key}
        response = send_request(API_URL, params)
        if response is not None:
            print(f"API Response: {response}")
        else:
            print("Failed to verify token.")

    def play_event(self, event, intensity=1, duration=1, offset_angle_x=0, offset_y=0):
        """Play an event."""
        if self.client is None:
            return -1

        request_id = random_request_id()
        play_message = {
            "eventName": event,
            "requestId": request_id,
            "intensity ": intensity,
            "duration ": duration,
            "offsetAngleX ": offset_angle_x,
            "offsetY  ": offset_y,
        }

        message = generate_message("SdkPlay", play_message)
        self.client.send_message(message)

        return request_id

    def stop_by_event(self, event):
        """Play an event."""
        if self.client is None:
            return

        message = generate_message("SdkStopByEventId", event)
        self.client.send_message(message)


if __name__ == '__main__':
    bhaptics_client = BhapticsSDK2("dd", "dd")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # If a KeyboardInterrupt (Ctrl+C) is detected, the program will exit this loop
        print("Stopping the client...")
        bhaptics_client.stop()
    finally:
        # Remove the hotkey hook
        keyboard.remove_hotkey('space')
    print("Client stopped.")
