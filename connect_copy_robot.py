import tkinter as tk
from PIL import Image, ImageTk  # Pillowライブラリが必要from ssh_connect import SSHConnect  # SSH接続用のクラスをインポート
import subprocess
import re

class ConnectCopyRobot:
    def __init__(self, select_canvas, select_location):
        self.select_canvas = select_canvas
        dir = "image_folder/"
        img = Image.open(dir+"connect_copy_robot.png").resize(((338, 62)))
        self.select_location_img = ImageTk.PhotoImage(img) 
        self.select_canvas.create_image(21, 0, image=self.select_location_img, anchor='nw')  
        self.select_location = select_location
        self.start_end_button()
        self.select_canvas.create_text(21, 200, text="| Run Command", font=("Bahnschrift SemiBold Condensed", 18,), fill="goldenrod2", anchor='nw')
        self.select_canvas.create_text(21,240, text=" | raspi |   ./run target_loc copy_ip pc_ip pc_port", font=("Bahnschrift SemiBold Condensed", 16,), fill="goldenrod2", anchor='nw')
        self.select_canvas.create_text(21, 265, text=
                                       "             | target_loc   :   select a,b,c,d"+ "\n" +
                                       "             | copy_ip        :   check the notion"+ "\n" +
                                       "             | pc_ip            :   ip of this PC" + "\n" +
                                       "             | pc_port        :   port of this PC", font=("Bahnschrift SemiBold Condensed", 16,), fill="goldenrod2", anchor='nw')
        self.select_canvas.create_text(21, 400, text=" | cr |   ./forcecontrol", font=("Bahnschrift SemiBold Condensed", 16,), fill="goldenrod2", anchor='nw')
    def start_end_button(self):
        """選択ボタンを作成する
        """
        dir = "image_folder/"
        button_widh = 104
        button_hight = 117 
        
        img = Image.open(dir+"copyrobot_connect_start.png").resize(((button_widh, button_hight)))
        self.copyrobot_connect_start_img = ImageTk.PhotoImage(img)
        self.start_button = tk.Button(self.select_canvas, command=self.connect_copy_robot ,height=button_hight,width=button_widh,
                image=self.copyrobot_connect_start_img,borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        self.start_button.place(x=21,y=70) 
        
        img = Image.open(dir+"copyrobot_connect_end.png").resize(((button_widh, button_hight)))
        self.copyrobot_connect_end_img = ImageTk.PhotoImage(img)
        self.end_button = tk.Button(self.select_canvas,command= self.disconnect_copy_robot ,height=button_hight,width=button_widh,
                               image=self.copyrobot_connect_end_img,borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        self.end_button.place(x=130,y=70) 
        
    def connect_copy_robot(self):
        print(self.select_location.use_location[0])
        self.start_button.config(state=tk.DISABLED)
        ### SSH接続の実行
        hostname, username = self.select_copy_robot()
        
        for i in range(len(hostname)):
            subprocess.run(f'start cmd /k "mode con: cols=50 lines=15 &&" ssh {hostname[i]}', shell = True)
        
        
    def disconnect_copy_robot(self):
        self.start_button.config(state=tk.NORMAL)
        pass
    
    def select_copy_robot(self):
        hostname = ["raspi-a","raspi-b","crb1","cra1"]
        username = ["raspi-a","raspi-b","debian","debian"]
        match self.select_location.use_location[0]:
            case "location_a":
                match self.select_location.use_location[1]:
                    case "location_a":
                        pass
                    case "location_b":
                        hostname = ["raspi-a","raspi-b","crb1","cra1"]
                        username = ["raspi-a","raspi-b","debian","debian"]
                    case "location_c":
                        hostname = ["raspi-a","raspi-c","crc1","cra2"]
                        username = ["raspi-a","raspi-c","debian","debian"]
                    case "location_d":
                        hostname = ["raspi-a","raspi-d","crc1","cra3"]
                        username = ["raspi-a","raspi-d","debian","debian"]
            case "location_b":
                 match self.select_location.use_location[1]:
                    case "location_a":
                        hostname = ["raspi-b","raspi-a","cra1","crb1"]
                        username = ["raspi-b","raspi-a","debian","debian"]
                    case "location_b":
                        pass
                    case "location_c":
                        hostname = ["raspi-b","raspi-c","crc2","crb2"]
                        username = ["raspi-b","raspi-c","debian","debian"]
                    case "location_d":
                        hostname = ["raspi-b","raspi-d","crc2","crb3"]
                        username = ["raspi-b","raspi-d","debian","debian"]
            case "location_c":
                match self.select_location.use_location[1]:
                    case "location_a":
                        hostname = ["raspi-c","raspi-a","cra2","crc1"]
                        username = ["raspi-c","raspi-a","debian","debian"]
                    case "location_b":
                        hostname = ["raspi-c","raspi-b","crb2","crc2"]
                        username =  ["raspi-c","raspi-b","debian","debian"]
                    case "location_c":
                        pass
                    case "location_d":
                        pass
            case "location_d":
                match self.select_location.use_location[1]:
                    case "location_a":
                        hostname = ["raspi-d","raspi-a","crc_a3","crc_c1"]
                        username = ["raspi-d","raspi-a","debian","debian"]
                    case "location_b":
                        hostname = ["raspi-d","raspi-b","crc_b3","crc_c2"]
                        username = ["raspi-d","raspi-b","debian","debian"]
                    case "location_c":
                        pass
                    case "location_d":
                        pass
        return hostname, username 