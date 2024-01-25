import socket
import threading


class UDPServer:
    def __init__(self, host="0.0.0.0", port=15884, callback=None):
        self.host = host
        self.port = port
        self.callback = callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        self.thread = None

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.running = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()
        print(f"UDP server listening on {self.host}:{self.port}")

    def listen(self):
        try:
            while self.running:
                data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
                message = data.decode()
                print(f"Received message: {message} from {addr}")
                if self.callback:
                    self.callback(message, addr)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.sock.close()

    def stop_server(self):
        self.running = False
        # We send a dummy message to the server to unblock the recvfrom call
        self.sock.sendto(b'', (self.host, self.port))
        self.sock.close()
        if self.thread is not None:
            self.thread.join()
        print("UDP server stopped.")


# Global server instance
udp_server = None


# Exportable functions
def listen(host="0.0.0.0", port=15884, callback=None):
    global udp_server
    udp_server = UDPServer(host, port, callback)
    udp_server.start_server()


def stop():
    global udp_server
    if udp_server:
        udp_server.stop_server()
