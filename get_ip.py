import socket

class GetIP:
    def __init__(self):
        pass
    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # ダミーの外部アドレスに接続（実際には接続しない）
            s.connect(("100.100.100.100", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            return "100.100.100.100"

#print("自身のIPアドレス:", get_ip_address())