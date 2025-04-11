import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk

class EmergencyMessage:
    def __init__(self):
        self.top = Toplevel()
        self.top.title("画像UI")
        self.top.geometry("409x144+785+467")
        self.top.resizable(False, False)
        self.top.overrideredirect(True)
        bg_img = Image.open("data_miss.png").resize((430, 175))
        bg_photo = ImageTk.PhotoImage(bg_img)
    def show_image_ui(self):
        
        
        # 背景画像
        

        bg_label = tk.Label(self.top, image=bg_photo)
        bg_label.image = bg_photo  # 参照保持
        bg_label.place(x=0, y=0, width=409, height=144)

    def delete_image(self):
        self.top.destroy
    