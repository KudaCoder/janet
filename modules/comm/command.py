import json
import socket
import threading

from .server import TCPServer
from modules.redis import RedisWrapper


class MExchange:
    def __init__(self):
        # TODO: Change this to use environ
        self.server = TCPServer("192.168.1.199", 9998)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

        self.redis = RedisWrapper().connect()

    def receive(self):
        while True:
            message = self.server.recv_q.get()
            if message:
                command = json.loads(message.decode("utf-8"))
                if command.get("redis"):
                    for k, v in command["redis"].items():
                        self.redis.set(k, v)

    def send(self, message):
        # TODO: Change this to use environ
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(("192.168.1.139", 9999))
        sock.send(message.encode())
        sock.close()

    def destroy(self):
        self.server.shutdown()
