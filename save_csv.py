import tkinter as tk
from tkinter import Toplevel
import csv
import threading
import time
from PIL import Image, ImageTk  # Pillowライブラリが必要

class CSVLoggerApp:
    def __init__(self, csv_frame,recevedata):
        self.recevedata = recevedata
        self.csv_frame = csv_frame
        #self.csv_frame.title("CSV保存アプリ")
        self.is_saving = False
        dir  = "image_folder/"

        # ファイル名入力欄
        image = Image.open(dir+"csv_label.png").resize((360, 56))  # 画像ファイルのパス
        self.csv_label = ImageTk.PhotoImage(image)
        self.label = tk.Label(csv_frame, image=self.csv_label,bg="black",borderwidth=0,highlightthickness=0)
        self.label.place(x = 0,y = 0)
        
        image = Image.open(dir+"csv_entry.png").resize((444, 59))  # 画像ファイルのパス
        self.csv_entry = ImageTk.PhotoImage(image)
        self.entry_label = tk.Label(csv_frame, image=self.csv_entry,bg="black",borderwidth=0,highlightthickness=0)
        self.entry_label.place(x = 0,y = 55)

        self.filename_entry = tk.Entry(csv_frame,relief="solid",bg="black",bd=5,font=("Bahnschrift SemiBold Condensed", 15),fg="goldenrod2",insertbackground = "goldenrod2")
        self.filename_entry.place(x = 158,y = 65,width=280, height=36)

        # 開始ボタン
        image = Image.open(dir+"save_start.png").resize((156, 175))  # 画像ファイルのパス
        self.save_start = ImageTk.PhotoImage(image)
        self.start_button = tk.Button(csv_frame, image=self.save_start, command=self.start_saving,borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        self.start_button.place(x = 20,y = 115,width=156, height=175)

        # 停止ボタン
        image = Image.open(dir+"save_stop.png").resize((156, 175))  # 画像ファイルのパス
        self.save_stop = ImageTk.PhotoImage(image)
        self.stop_button = tk.Button(csv_frame, text="保存停止", image=self.save_stop,command=self.stop_saving,borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        self.stop_button.place(x = 200,y = 115,width=156, height=175)

        
        # 保存中
        image = Image.open(dir+"save_run.png").resize((180, 270))  # 画像ファイルのパス
        self.save_run = ImageTk.PhotoImage(image)
        
    def start_saving(self):
        filename = self.filename_entry.get()

        self.is_saving = True
        #self.start_button.config(state=tk.DISABLED)
        #self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.save_csv, args=(filename,), daemon=True).start()

    def stop_saving(self):
        self.is_saving = False

    def save_csv(self, filename):
        self.status_label = tk.Label(self.csv_frame, image=self.save_run,borderwidth=0,highlightthickness=0)
        self.status_label.place(x=480, y=50)
        print(f"test:")
        with open("output_file/"+filename + "_location_a.csv", mode='a', newline='') as file_a, \
            open("output_file/"+filename + "_location_b.csv", mode='a', newline='') as file_b:

            writer_a = csv.writer(file_a)
            writer_b = csv.writer(file_b)
            head = ["master_pos_x","master_pos_y","master_pos_theta","master_vel_x","master_vel_y","master_vel_theta",
                    "copy_1_pos_x","copy_1_pos_y","copy_1_pos_theta","copy_1_vel_x","copy_1_vel_y","copy_1_vel_theta",
                    "copy_2_pos_x","copy_2_pos_y","copy_2_pos_theta","copy_2_vel_x","copy_2_vel_y","copy_2_vel_theta","time"]
            writer_a.writerow(head)
            writer_b.writerow(head)
            while self.is_saving:
                
                wrote = False

                # location_aのキュー処理
                while self.recevedata["location_a"].csvsave_queue:
                    data = self.recevedata["location_a"].csvsave_queue.popleft()
                    writer_a.writerow(data)
                    wrote = True

                # location_bのキュー処理
                while self.recevedata["location_b"].csvsave_queue:
                    data = self.recevedata["location_b"].csvsave_queue.popleft()
                    writer_b.writerow(data)
                    wrote = True

                if not wrote:
                    time.sleep(0.01)

        #messagebox.showinfo("保存完了", f"{filename} に保存を完了しました")
        self.status_label.destroy()
        self.complete_save()
    
    def complete_save(self):
        top = Toplevel()
        top.title("画像UI")
        top.geometry("409x144+450+600")
        top.resizable(False, False)
        top.overrideredirect(True)
        # 背景画像
        dir = "image_folder/"
        bg_img = Image.open(dir+"save_complete.png").resize((409, 144))
        bg_photo = ImageTk.PhotoImage(bg_img)

        bg_label = tk.Label(top, image=bg_photo)
        bg_label.image = bg_photo  # 参照保持
        bg_label.place(x=0, y=0, width=409, height=144)

        # OKボタン（画像ボタンも可能）
        
        img = Image.open(dir+"confirm.png").resize((90, 38))
        comfirm_button = ImageTk.PhotoImage(img)
        bg_label.comfirm_button = comfirm_button
        ok_button = tk.Button(top, command=top.destroy, image= comfirm_button,
                            borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        ok_button.place(x = 157, y=95,width=90, height=38)  # 好きな位置に配置

# GUI実行
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVLoggerApp(root)
    root.mainloop()
