import socket
import threading

class TCPClient:
    def __init__(self, server_host, server_port, message_received_callback=None, verbose=False):
        self.server_host = server_host
        self.server_port = server_port
        self.message_received_callback = message_received_callback
        self.verbose = verbose
        self.client_socket = None
        self.connected = False
        self.receive_thread = None

    def __print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def __receive_messages(self):
        try:
            while self.connected:
                response = self.client_socket.recv(4096)  # Buffer size of 4096 bytes
                if response:
                    # Call the callback function if any message is received
                    if self.message_received_callback:
                        self.__print("App → Client: ", response)
                        self.message_received_callback(response.decode())
                else:
                    # No response indicates the server has closed the connection
                    break
        except Exception as e:
            if self.connected:
                self.__print(f"An error occurred in TCP: {e}")
        finally:
            self.connected = False
            self.client_socket.close()
            self.__print(f"Closed TCP connection with app.")

    def send_message(self, message):
        self.__print("Client → App: ", message)
        
        if self.connected:
            try:
                self.client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                self.__print(f"\t sending failed: {e}.")
        else:
            self.__print("\t sending failed: client is not connected.")

    def start(self, initial_message=None):
        if not self.connected:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect((self.server_host, self.server_port))
                self.connected = True
                self.__print(f"Connected to {self.server_host} on port {self.server_port}")

                # Start listening for messages from the server
                self.receive_thread = threading.Thread(target=self.__receive_messages)
                self.receive_thread.start()

                # Send the initial message after connecting
                if initial_message:
                    self.send_message(initial_message)

            except Exception as e:
                self.connected = False
                self.__print(f"An error occurred while connecting: {e}")
        else:
            self.__print("Client is already connected.")
    
    def stop(self):
        if self.connected:
            try:
                self.connected = False
                self.client_socket.close()
            except OSError as e:
                self.__print(f"Error closing TCP socket: {e}")
                return
            
            if threading.current_thread() != self.receive_thread:
                try:
                    if self.receive_thread:
                        self.receive_thread.join()
                        self.receive_thread = None
                except Exception as e:
                    self.__print(f"Error joining TCP thread: {e}")
                return

    def is_connected(self):
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
    if client.is_connected():
        print("Client is connected.")
    else:
        print("Client is not connected.")

    # The client will now listen for messages and invoke the callback when messages are received
    try:
        # Keep the main thread alive while the client is running.
        while client.is_connected():
            pass
    except KeyboardInterrupt:
        print("Stopping the client...")
        client.stop()
