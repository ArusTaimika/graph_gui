import socket
import struct
import time

class Udp_connect:
    def __init__(self,ip, port, data_pieces, time_pieces):
        # UDPソケットを作成
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.ip = ip
        self.port = port
        self.data_pieces = data_pieces
        self.time_pieces = time_pieces  # タイムスタンプの個数（例: 1個）
        if self.ip == '0.0.0.0':
            self.udp_socket.bind((self.ip, self.port))
            self.udp_socket.settimeout(1.0) 
        self.timeout_flag = False
    def udp_server(self): 
        try:
            # データを受信（バッファサイズは1024バイト）
            data, addr = self.udp_socket.recvfrom(self.data_pieces * 8 + self.time_pieces * 8)  # 4は整数のサイズ)
            self.timeout_flag = True
            #バイナリデータをアンパックして複数の浮動小数点数として解釈
            return struct.unpack(f'<{self.data_pieces}d{self.time_pieces}q', data) # data_piecesの個数のdoubleをアンパック
        except socket.timeout:
            dummy_data = [1.0]*self.data_pieces
            dummy_data.append(1)
            self.timeout_flag = False
            return tuple(dummy_data)
    
    
    def udp_client(self, data):
        # サーバーにデータを送信
        #self.udp_socket.sendto(message.encode(), (server_ip, server_port))# 文字列を想定した場合
        # data（リスト型）を展開して渡す
        self.udp_socket .sendto(struct.pack(f'!i{self.data_pieces}d', *data), (self.ip, self.port))

    def get_flag(self):
        return self.timeout_flag
    
    def udp_close(self):
        # ソケットを閉じる
        self.udp_socket.close()
        
        


#server用
if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 12345
    data_pieces = 2
    udp_connect = Udp_connect(ip, port, data_pieces)

    try:
        while True:
            received_numbers = udp_connect.udp_server()
    except KeyboardInterrupt:
        print("ーーーーーーーーー終了ーーーーーーーーーーーー")
    finally:
        udp_connect.udp_close()
    
"""
#client用
if __name__ == "__main__":
    ip = "192.168.132.154"
    port = 12345
    data_pieces = 2
    udp_connect = Udp_connect(ip, port, data_pieces)

    # 送信データ
    data = [0.1,0.1,0.1]
    try:
        while True:
            udp_connect.udp_client(data)
            time.sleep(1/30)
    except KeyboardInterrupt:
        print("ーーーーーーーーー終了ーーーーーーーーーーーー")
    finally:
        udp_connect.udp_close()
    
"""