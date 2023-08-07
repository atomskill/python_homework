import socket
import time

class Client():
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def put(self, key, value, timestamp = int(time.time())):
        with socket.create_connection((self.host, self.port), self.timeout) as connect:
            connect.sendall( f"put {key} {value} {timestamp}\n".encode('utf-8'))
        answer = connect.recv(1024)
        if answer.decode().split('\n')[0] != 'ok':
            raise ClientError("Bad Request")
    
    def get(self, key):
        with socket.create_connection((self.host, self.port), self.timeout) as connect:
            connect.sendall(f"get {key}\n".encode('utf-8'))
        answer = connect.recv(1024).decode()
        ansObjs = answer.split('\n')
        if ansObjs[0] != 'ok':
            raise ClientError("Bad Request")
        metrics = {}
        for m in ansObjs:
            if(m == 'ok' or m == ''): continue
            ms = m.split()
            key = ms[0]
            timestamp = float(ms[1])
            value = float(ms[2])
            if key not in metrics:
                metrics[key] = [(value, timestamp)]
            else:
                metrics[key].append((value, timestamp))
        for key in metrics:
            metrics[key] = sorted(metrics[key], key=lambda x: x[1], reverse=True)
        return metrics

class ClientError(Exception):
    def __init__(self, message):
        super().__init__(message)