from socket import create_connection

class Client():
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def put(self, key, value, timestamp):
        connect = create_connection((self.host, self.port), 1)
        connect.sendall( f"put {key} {value} {timestamp}\n".encode('utf-8'))
        return connect.recv(1024)
    
    def get(self, key):
        connect = create_connection((self.host, self.port), 1)
        connect.sendall(f"get {key}\n".encode('utf-8'))
        return connect.recv(1024)

class ClientError():
    def __init__(self):
        pass