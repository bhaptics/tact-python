import socket
import threading


class TCPClient:
    def __init__(self, server_host, server_port, message_received_callback=None):
        self.server_host = server_host
        self.server_port = server_port
        self.message_received_callback = message_received_callback
        self.client_socket = None
        self.connected = False
        self.lock = threading.Lock()
        self.receive_thread = None

    def start(self, initial_message=None):
        with self.lock:
            if not self.connected:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.client_socket.connect((self.server_host, self.server_port))
                    self.connected = True
                    print(f"Connected to {self.server_host} on port {self.server_port}")

                    # Start listening for messages from the server
                    self.receive_thread = threading.Thread(target=self.receive_messages)
                    self.receive_thread.start()

                    # Send the initial message after connecting
                    if initial_message:
                        self.send_message(initial_message)

                except Exception as e:
                    self.connected = False
                    print(f"An error occurred while connecting: {e}")
            else:
                print("Client is already connected.")

    def receive_messages(self):
        while self.connected:
            try:
                response = self.client_socket.recv(4096)  # buffer size is 4096 bytes
                if response:
                    # Call the callback function if any message is received
                    if self.message_received_callback:
                        print("received", response)
                        self.message_received_callback(response.decode())
                else:
                    # No response indicates the server has closed the connection
                    print("The server has closed the connection.")
                    self.stop()
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                self.stop()
                break

    def send_message(self, message):
        if self.connected:
            try:
                print("sendMessage", message)
                self.client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"An error occurred while sending message: {e}")
        else:
            print("Cannot send message. The client is not connected.")

    def stop(self):
        with self.lock:
            if self.connected:
                self.connected = False
                self.client_socket.close()
                self.receive_thread.join()
                print("Connection closed.")
            else:
                print("Client is not connected.")

    def status(self):
        return self.connected


# Example callback function
def message_received(message):
    print(f"Received: {message}")


# Example of module usage
if __name__ == "__main__":
    client = TCPClient("127.0.0.1", 15884, message_received_callback=message_received)

    # Start client and send a message
    client.start("Hello, TCP Server!")

    # Send another message
    client.send_message("Another message")

    # Check connection status
    if client.status():
        print("Client is connected.")
    else:
        print("Client is not connected.")

    # The client will now listen for messages and invoke the callback when messages are received
    try:
        # Keep the main thread alive while the client is running.
        while client.status():
            pass
    except KeyboardInterrupt:
        print("Stopping the client...")
        client.stop()
