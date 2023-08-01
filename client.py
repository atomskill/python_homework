import socket

class Client():
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def put(self, key, value, timestamp):
        connect = socket.create_connection((self.host, self.port), self.timeout)
        connect.sendall( f"put {key} {value} {timestamp}\n".encode('utf-8'))
        return connect.recv(1024)
    
    def get(self, key):
        connect = socket.create_connection((self.host, self.port), self.timeout)
        connect.sendall(f"get {key}\n".encode('utf-8'))
        return connect.recv(1024)

class ClientError():
    def __init__(self):
        pass