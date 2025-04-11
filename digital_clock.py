import ntplib
from datetime import datetime, timezone, timedelta
import time
from PIL import Image, ImageTk  # 必要
import tkinter as tk

from seven_segment import SevenSegmentDigit

class DigitalClockApp_7seg:
    def __init__(self, canvas):
        self.canvas = canvas
        # 各桁（6桁 + コロン）
        self.digits = []
        x_offsets = [10 + i * 80 for i in range(6)]
        for x in x_offsets[:2]:
            self.digits.append(SevenSegmentDigit(self.canvas, x))
        self.colon = self.canvas.create_text(x+80, 54, text=":", font=("Courier New", 60), fill="black")
        for x in x_offsets[2:4]:
            self.digits.append(SevenSegmentDigit(self.canvas, x + 20))
        self.colon2 = self.canvas.create_text(x+100, 54, text=":", font=("Courier New", 60), fill="black")
        for x in x_offsets[4:]:
            self.digits.append(SevenSegmentDigit(self.canvas, x + 40))

        self.ntp_time = self.get_ntp_time()
        
        self.start_timestamp = time.time()

    def update_clock(self):
        now = self.ntp_time + timedelta(seconds=int(time.time() - self.start_timestamp))
        time_str = now.strftime("%H%M%S")
        for i, digit in enumerate(time_str):
            self.digits[i].draw(digit)

        # コロンを点滅させたいなら以下を活用
        self.canvas.itemconfig(self.colon, fill="black" if int(now.second) % 2 == 0 else "red")
        self.canvas.itemconfig(self.colon2, fill="black" if int(now.second) % 2 == 0 else "red")

    # NTPから時刻を取得する関数
    def get_ntp_time(self):
        try:
            client = ntplib.NTPClient()
            response = client.request('ntp.nict.jp', version=3)
            return datetime.fromtimestamp(response.tx_time, timezone.utc) + timedelta(hours=9)  # 日本時間に補正
        except Exception as e:
            print("NTP取得失敗:", e)
            return datetime.now()

class DigitalClockApp_Text:
    def __init__(self, canvas):
        self.canvas = canvas
        # 背景画像の読み込み
        self.bg_image = Image.open("image_folder/"+"clock_background.png").resize((525, 235))# パスは必要に応じて調整
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        
        self.time_h_text = self.canvas.create_text(140, 144, text="", font=("HGPゴシックE", 70,), fill="gold2") #Bahanschrift SemiBold Condensed
        self.time_m_text = self.canvas.create_text(278, 144, text="", font=("HGPゴシックE", 70), fill="gold2") #Bahanschrift SemiBold Condensed
        self.time_s_text = self.canvas.create_text(408, 142, text="", font=("HGPゴシックE", 70), fill="gold2") #Bahanschrift SemiBold Condensed

        self.ntp_time = self.get_ntp_time()
        self.start_timestamp = time.time()

    def update_clock(self):
        now = self.ntp_time + timedelta(seconds=int(time.time() - self.start_timestamp))
        self.canvas.itemconfig(self.time_h_text, text=now.strftime("%H"))
        self.canvas.itemconfig(self.time_m_text, text=now.strftime("%M"))
        self.canvas.itemconfig(self.time_s_text, text=now.strftime("%S"))

    def get_ntp_time(self):
        try:
            client = ntplib.NTPClient()
            response = client.request('ntp.nict.jp', version=3)
            return datetime.fromtimestamp(response.tx_time, timezone.utc) + timedelta(hours=9)  # 日本時間に補正
        except Exception as e:
            print("NTP取得失敗:", e)
            return datetime.now()