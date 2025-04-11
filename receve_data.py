from udp_connect import Udp_connect
import queue
from collections import deque

class ReceveData:
    def __init__(self,port):
        ip = "0.0.0.0"
        data_pieces = 18
        self.queue = queue.Queue()
        self.csvsave_queue = deque(maxlen=10)
        self.udp_connect = Udp_connect(ip, port, data_pieces)
        self.timeout_flag = False
        
    def receive_data(self,location):
        self.running = True
        while self.running:
            received_data = self.udp_connect.udp_server()
            self.queue.put(received_data)
            
            self.csvsave_queue.append(received_data)  # ←古いの自動削除
            self.timeout_flag = self.udp_connect.get_flag()
            
    def stop(self):
        self.running = False