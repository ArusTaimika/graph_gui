import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from PIL import Image, ImageTk  # 必要
import tkinter as tk
from tkinter import ttk
import datetime
from datetime import datetime, timezone, timedelta
from matplotlib.dates import DateFormatter
import time

class TimeDelay:
    def __init__(self, axes, fig_canvas, timedelay_frame):
        self.ax_main = axes[0]       # 時系列グラフ
        self.ax_polar_a = axes[1]    # 極座標（raspi-a）
        self.ax_polar_b = axes[2]    # 極座標（raspi-b）

        self.fig_canvas = fig_canvas
        self.timedelay_frame = timedelay_frame

        self.para_canvas = tk.Canvas(self.timedelay_frame, width=500, height=200, bg="black",bd=0,highlightthickness=0)
        self.para_canvas.place(x=0, y=330)
        
        self.td_canvas = tk.Canvas(self.timedelay_frame, width=380, height=50, bg="black", bd=0, highlightthickness=0)
        self.td_canvas.place(x=50, y=30)
        
        self.copy_data = {"raspi-a": [], "raspi-b": []}
        self.x_data = {"raspi-a": np.empty((0, 1)), "raspi-b": np.empty((0, 1))}
        self.y_data = {"raspi-a": np.empty((0, 1)), "raspi-b": np.empty((0, 1))}
        self.max_points = 1400
        self.flag = False

        self.polar_data = {
            "raspi-a": np.empty((0, 6)),  # 3つの大きさ・角度 = 6要素
            "raspi-b": np.empty((0, 6))
        }
        self.init_main_plot()
        self.init_polar_plot()
        self.init_image()
        self.init_parameter()
        
    def init_main_plot(self):
        """時間遅延用の主プロットの初期化"""
        self.setup_tick(self.ax_main)
        self.lines = {
            "raspi-a": self.ax_main.plot([], [], 'r', label='raspi-a')[0],
            "raspi-b": self.ax_main.plot([], [], 'b', label='raspi-b')[0],
        }
        self.ax_main.set_ylim(0, 130)
        fontsize = 18
        self.td_canvas.create_text(150, 34, text= "ー", fill="blue", font=("Bahnschrift SemiBold Condensed", 30,))
        self.td_canvas.create_text(300, 34, text= "ー", fill="red", font=("Bahnschrift SemiBold Condensed", 30,))
        self.tdloc_para = [self.td_canvas.create_text(200, 34, text= "Rx A", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,)),
                        self.td_canvas.create_text(350, 34, text= "Rx B", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,))]
    
    def init_polar_plot(self):
        """極座標プロットの基本設定"""
        for polar_ax in [self.ax_polar_a, self.ax_polar_b]:
            polar_ax.set_theta_zero_location('E')
            polar_ax.set_theta_direction(1)
            polar_ax.grid(True, color = 'gold', linestyle='--', linewidth=0.5)
            
            #polar_ax.tick_params(colors='gold')

    def init_parameter(self):
        fontsize = 20
        self.location_para = [self.para_canvas.create_text(128, 38, text= "B", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,)),
                              self.para_canvas.create_text(348, 38, text= "A", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,))
                                ]
        y_pos = 78
        self.robot_para = {"raspi-a": [self.para_canvas.create_text(148, y_pos, text="0.0", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,)),
                                       self.para_canvas.create_text(148, y_pos + 42, text="0.0", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,)),
                                       self.para_canvas.create_text(148, y_pos + 84, text="0.0", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,))],
                           "raspi-b": [self.para_canvas.create_text(368, y_pos, text="0.0", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,)),
                                       self.para_canvas.create_text(368, y_pos + 42, text="0.0", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,)),
                                       self.para_canvas.create_text(368, y_pos + 84, text="0.0", fill="goldenrod2", font=("Bahnschrift SemiBold Condensed", fontsize,))]}
    def update_location(self, n, txt):
        self.para_canvas.itemconfig(self.location_para[n], text=txt)
        self.td_canvas.itemconfig(self.tdloc_para[n], text=f"Rx {txt}")
    def update_robot_para(self, raspi_name, n, para):
        self.para_canvas.itemconfig(self.robot_para[raspi_name][n], text=f"{para:.2f}")
        
    def init_image(self):
        """画像ラベル表示"""
        dir = "image_folder/"
        img = Image.open(dir + "timedelay.png").resize((454, 46))
        self.timedelay_img = ImageTk.PhotoImage(img)
        tk.Label(self.timedelay_frame, image=self.timedelay_img).place(x=0, y=0, width=454, height=46)
        
        img = Image.open(dir + "forcedata.png").resize((454, 46))
        self.forcedata_img = ImageTk.PhotoImage(img)
        tk.Label(self.timedelay_frame, image=self.forcedata_img).place(x=0, y=283, width=454, height=46)
        
        img = Image.open(dir + "force_para.png").resize((193, 206))
        self.force_para = {"raspi-a":ImageTk.PhotoImage(img), "raspi-b":ImageTk.PhotoImage(img)}
        self.para_canvas.create_image(18, 0, anchor=tk.NW, image=self.force_para["raspi-a"])
        self.para_canvas.create_image(238, 0, anchor=tk.NW, image=self.force_para["raspi-b"])
        
    def setup_tick(self, ax):
        """軸の目盛り設定"""
        ax.tick_params(axis='both', colors='gold', direction='in', length=5, width=1)
        ax.minorticks_on()
        ax.tick_params(which='minor', length=3, width=0.8, color='gold')
        
    def convert_data(self, ras, queue):
        """データキューから抽出し整形"""
        while not queue.empty():
            self.copy_data[ras] = queue.get()
            if queue.qsize() < self.max_points + 5:
                now_time = self.copy_data[ras][7] / 1_000_000_000
                dt_utc = datetime.fromtimestamp(now_time, tz=timezone.utc)
                jst = dt_utc.astimezone(timezone(timedelta(hours=9)))
    
                # 時系列データ追加
                x_val = np.array([[jst]])
                y_val = np.array([[self.copy_data[ras][6]]])
                self.x_data[ras] = np.vstack([self.x_data[ras], x_val])
                self.y_data[ras] = np.vstack([self.y_data[ras], y_val])
    
                # 極座標データ追加（0〜5を1行として追加）
                polar_val = np.array([self.copy_data[ras][i] for i in range(6)]).reshape(1, 6)
                self.polar_data[ras] = np.vstack([self.polar_data[ras], polar_val])
    
                self.flag = True
    
                # サイズ制限
                if self.y_data[ras].shape[0] > self.max_points:
                    self.x_data[ras] = self.x_data[ras][-self.max_points:, :]
                    self.y_data[ras] = self.y_data[ras][-self.max_points:, :]
                    self.polar_data[ras] = self.polar_data[ras][-self.max_points:, :]


    def plot_timedelay(self):
        """主プロット更新"""
        if self.flag:
            for ras in ["raspi-a", "raspi-b"]:
                if self.x_data[ras].shape[0] > 0:
                    self.lines[ras].set_data(self.x_data[ras].flatten(), self.y_data[ras].flatten())

            end_time = self.x_data["raspi-a"][-1, 0]
            start_time = end_time - timedelta(seconds=30)
            self.ax_main.set_xlim(start_time, end_time)
            self.ax_main.xaxis.set_major_formatter(DateFormatter('%M:%S'))
            self.ax_main.relim()
            self.ax_main.autoscale_view(scalex=False)

    def plot_polar_data(self):
        """極座標プロット更新"""
        for raspi_name, ax in [("raspi-a", self.ax_polar_a), ("raspi-b", self.ax_polar_b)]:
            ax.clear()
            self.init_polar_plot()
            ax.set_ylim(0, 20)

            if self.polar_data[raspi_name].shape[0] > 0:
                data = self.polar_data[raspi_name][-1]
                print(data)
                for i in range(3):
                    # 値の取り出し（raspi-aの1個目だけ順序が違う）
                    if i == 0:
                        mag = data[0]
                        angle = data[2]
                    else:
                        angle = data[2*i]
                        mag = data[2*i + 1]
                    if mag > 0.1:
                        # 色と線種の指定
                        if raspi_name == "raspi-a":
                            colors = ['red', 'deeppink', 'white']
                            linestyles = ['solid', 'solid', '--']
                        else:  # raspi-b
                            colors = ['blue', 'blueviolet', 'white']
                            linestyles = ['solid', 'solid', '--']

                        # ベクトル描画
                        ax.plot([angle, angle], [0, mag],
                                lw=2, color=colors[i], linestyle=linestyles[i])

                        ax.annotate("",
                            xy=(angle, mag), xytext=(angle, mag - 0.1),
                            arrowprops=dict(arrowstyle="->", color=colors[i], lw=3),
                            annotation_clip=False
                        )
                        self.update_robot_para(raspi_name, i, mag)
    def draw(self):
        self.fig_canvas.draw()
