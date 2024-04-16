import socket
import threading

class UDPServer:
    def __init__(self, host="0.0.0.0", port=15884, callback=None, verbose=False):
        self.host = host
        self.port = port
        self.callback = callback
        self.verbose = verbose
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.thread = None

    def __print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def __listen(self):
        try:
            while self.running:
                data, addr = self.sock.recvfrom(1024)  # Buffer size of 1024 bytes
                message = data.decode()
                self.__print(f"Received message: {message} from {addr}")
                if self.callback:
                    self.callback(message, addr)
        except Exception as e:
            if self.running:
                self.__print(f"An error occurred in UDP: {e}")
        finally:
            self.running = False
            self.sock.close()
            self.__print("Closed UDP server.")

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.running = True
        self.thread = threading.Thread(target=self.__listen)
        self.thread.start()
        self.__print(f"UDP server listening on {self.host}:{self.port}")

    def stop_server(self):
        if self.running:
            try:
                self.running = False
                self.sock.close()
            except OSError as e:
                self.__print(f"Error closing UDP socket: {e}")
                return
            
            if threading.current_thread() != self.thread:
                try:
                    if self.thread:
                        self.thread.join()
                        self.thread = None
                except Exception as e:
                    self.__print(f"Error joining UDP thread: {e}")
                    return

# Global server instance
udp_server = None

# Exportable functions
def listen(host="0.0.0.0", port=15884, callback=None, verbose=False):
    global udp_server
    udp_server = UDPServer(host, port, callback, verbose=verbose)
    udp_server.start_server()

def stop():
    global udp_server
    if udp_server:
        udp_server.stop_server()
