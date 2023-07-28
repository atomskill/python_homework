from socket import create_connection
class Client():
    def __init__(self, host, port, timeout = 1):
            try:
                self.connect = create_connection((host, port))
            except:
                 pass
    def put(self, key, value, timestamp):
        self.connect.send(bytes(f"put {key} {value} {timestamp}\n",'utf-8'))
        return self.connect.recv(1024)
    
    def get(self, key):
        self.connect.send(bytes(f"get {key}\n",'utf-8'))
        return self.connect.recv(1024)    

class ClientError():
    def __init__(self):
        pass