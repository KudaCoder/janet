import socketserver
from queue import Queue


class QueueHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.server = server
        server.client_address = client_address
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv(4096)
        self.server.recv_q.put(data)


# Not sure how this should work yet!
# Need a system to pass a thread_q into an app and a worker
# to check for the response in a non-blocking loop!
class Worker:
    def __init__(self, speech):
        self.thread_q = Queue()
        self.speech = speech

    def thread_q_worker(self):
        while True:
            if not self.thread_q.empty():
                value = self.thread_q.get()
                self.speech.speak(value)
