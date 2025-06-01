import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from PIL import Image, ImageTk  # 必要
import tkinter as tk
from tkinter import ttk

class MakeGraph():
    def __init__(self,ax,fig_canvas):
        self.ax = ax
        self.ax["location_a"].set_aspect('equal')
        self.ax["location_b"].set_aspect('equal')
        
        self.fig_canvas = fig_canvas
        
        self.robotpos = {"location_a":{"master":np.empty((1,2)), "copy_1":np.empty((1,2)),"copy_2":np.empty((1,2))},
                         "location_b":{"master":np.empty((1,2)), "copy_1":np.empty((1,2)),"copy_2":np.empty((1,2))}}
        self.robotano = {"location_a":{"master":  {"collor":"BlueViolet", "name":"Master"},
                                       "copy_1":    {"collor":"red" , "name":"Copy_1"},
                                       "copy_2":    {"collor":"hotpink" , "name":"Copy_2"}},
                         "location_b":{"master":  {"collor":"BlueViolet", "name":"Master"},
                                       "copy_1":    {"collor":"red" , "name":"Copy_1"},
                                       "copy_2":    {"collor":"hotpink" , "name":"Copy_2"}}}
        
        self.setup_tick("location_a")
        self.setup_tick("location_b")
        
        self.data = [0]*19
        radius = 335 / 2  # 直径335の半径
        self.circle = {"location_a":{},"location_b":{}}
        self.text_patch = {"location_a":{},"location_b":{}}
        self.point_patch = {"location_a":{},"location_b":{}}
        self.arrow_patch = {"location_a":{},"location_b":{}}
        for loc in ["location_a", "location_b"]:
            for key in ["master", "copy_1", "copy_2"]:
                self.circle[loc][key] = patches.Circle((0, 0), radius=radius, fill=False, edgecolor=self.robotano[loc][key]["collor"], linewidth=1)
                self.ax[loc].add_patch(self.circle[loc][key])
                self.text_patch[loc][key] = self.ax[loc].text(0, 0, self.robotano[loc][key]["name"], color=self.robotano[loc][key]["collor"], fontsize=10)
                self.point_patch[loc][key], = self.ax[loc].plot(0 , 0, 'o', color = self.robotano[loc][key]["collor"])
                self.arrow_patch[loc][key] = FancyArrowPatch(
                    posA=(0, 0),
                    posB=(radius,0),
                    arrowstyle="->",
                    color=self.robotano[loc][key]["collor"],
                    mutation_scale=15
                )
                self.ax[loc].add_patch(self.arrow_patch[loc][key])
                
    def convert_data(self,location,queue):
        self.flag = False
        max_points = 5
        while not queue.empty():
            self.data = queue.get()
            if queue.qsize() < max_points+5:
                self.robotpos[location]["master"] = np.vstack([self.robotpos[location]["master"],np.array([[self.data[0],self.data[1]]])])
                self.robotpos[location]["copy_1"] = np.vstack([self.robotpos[location]["copy_1"],np.array([[self.data[6],self.data[7]]])])
                self.robotpos[location]["copy_2"] = np.vstack([self.robotpos[location]["copy_2"],np.array([[self.data[12],self.data[13]]])])
                self.flag = True
            if self.robotpos[location]["master"].shape[0] > max_points:
                self.robotpos[location]["master"] = self.robotpos[location]["master"][-max_points:, :]
                self.robotpos[location]["copy_1"] = self.robotpos[location]["copy_1"][-max_points:, :]
                self.robotpos[location]["copy_2"] = self.robotpos[location]["copy_2"][-max_points:, :]
            
        return self.data
    
    def cal_graph(self,location):
        if self.flag:
            #self.ax[location].clear()
            self.ax[location].grid(linestyle=':',color = (1.0,0.7529,0))
            self.plot_robotpos(location,"master",self.robotpos[location]["master"],self.data[2], self.robotano[location]["master"])
            self.plot_robotpos(location,"copy_1" , self.robotpos[location]["copy_1"],self.data[8], self.robotano[location]["copy_1"])
            self.plot_robotpos(location,"copy_2", self.robotpos[location]["copy_2"],self.data[14], self.robotano[location]["copy_2"])
            self.ax[location].set_title("Data Plot")
            self.ax[location].set_xlim(0, 1100)
            self.ax[location].set_ylim(0, 1100)
            self.ax[location].minorticks_on() 
            
            

    def plot_robotpos(self, location,key ,pos, theta,annotate):
        self.point_patch[location][key].set_data(pos[:,0] , pos[:,1])
        self.circle[location][key].center= (pos[-1,0], pos[-1,1])
        self.text_patch[location][key].set_position((pos[-1,0], pos[-1,1]))
        self.arrow_patch[location][key].set_positions((pos[-1,0], pos[-1,1]), self.cal_allowend(pos[-1,0],pos[-1,1],theta))
        
    def cal_allowend(self,pos_x,pos_y, theta):
        radius = 335 / 2
        end_x =  pos_x +radius* np.cos(theta*np.pi/180)
        end_y =  pos_y +radius* np.sin(theta*np.pi/180)
        return [end_x,end_y]
    
    
    def setup_tick(self,location):
        self.ax[location].tick_params(
            axis='both',      # x軸とy軸両方に適用
            colors='gold',   # 目盛りの「ラベル」文字の色
            direction='in',   # 目盛りの方向（'in', 'out', 'inout'）
            length=5,         # 目盛り線の長さ
            width=1,          # 線の太さ
            color='gold'     # ← これが目盛り線そのものの色
        )
        
        self.ax[location].minorticks_on()  # ← 副目盛りを有効にする
        self.ax[location].tick_params(
            which='minor',   # ← minorで副目盛り，majorで主目盛り
            length=3,
            width=0.8,
            color='gold'
        )
        
        self.ax[location].set_xlim(0, 1100)
        self.ax[location].set_ylim(0, 1100)
    def draw(self):
        self.fig_canvas.draw()

class MakeleftWindow():
    def __init__(self,fig_canvas):
        self.fig_canvas = fig_canvas
        dir = "image_folder/"
        img = Image.open(dir+"target_location.png").resize((450, 55))# パスは必要に応じて調整
        self.target_location_img = ImageTk.PhotoImage(img) 
        
        img = Image.open(dir+"master_posvelo.png").resize((360, 413))# パスは必要に応じて調整
        self.master_posvelo_img = ImageTk.PhotoImage(img)
        
        button_hight = 106
        button_widh = 50
        master_img = Image.open(dir+"master_button.png").resize((button_widh, button_hight))# パスは必要に応じて調整
        copy_1_img = Image.open(dir+"copy_1_button.png").resize((button_widh, button_hight))# パスは必要に応じて調整
        copy_2_img = Image.open(dir+"copy_2_button.png").resize((button_widh, button_hight))# パスは必要に応じて調整
        self.select_button = {"master":ImageTk.PhotoImage(master_img)
            ,"copy_1":ImageTk.PhotoImage(copy_1_img)
            ,"copy_2":ImageTk.PhotoImage(copy_2_img)}
        
        self.robot_text = {"location_a":self.fig_canvas["location_a"].create_text(114, 88, text="", font=("Bahnschrift SemiBold Condensed", 18), fill="goldenrod2", anchor='nw'),
                           "location_b":self.fig_canvas["location_b"].create_text(114, 88, text="", font=("Bahnschrift SemiBold Condensed", 18), fill="goldenrod2", anchor='nw')}
        #self.robot_text = self.fig_canvas["location_b"].create_text(104, 92, text="MASTER", font=("HGゴシックE", 13,"bold"), fill="goldenrod2", anchor='nw')
        self.push_key = {"location_a":"master", "location_b":"master"}
        self.location_text = {"location_a":None, "location_b":None}
        for loc in ["location_a", "location_b"]:
            self.fig_canvas[loc].create_image(10, 10, image=self.target_location_img, anchor='nw')
            self.fig_canvas[loc].create_image(75, 60, image=self.master_posvelo_img, anchor='nw') 
            self.location_text[loc] = self.fig_canvas[loc].create_text(415, 16, text="A", font=("Bahnschrift SemiBold Condensed", 25,), fill="goldenrod2", anchor='nw')
    
    def update_target_location(self,n,targetname):
        # Labelに画像を設定
        if n == 0:
            loc = "location_a"
        else:
            loc = "location_b"       
        self.fig_canvas[loc].itemconfig(self.location_text[loc], text=targetname)
        
    def make_noteobok(self):
        # スタイル設定
        style = ttk.Style()
        style.theme_use("default")  # 安定して色が効くテーマ

        # Notebookの本体部分
        style.configure("Black.TNotebook", background="black", borderwidth=0)

        #
        style.layout("TNotebook.Tab", [])
        self.inner_notebook = {
            "location_a": ttk.Notebook(self.fig_canvas["location_a"], style="Black.TNotebook"),
            "location_b": ttk.Notebook(self.fig_canvas["location_b"], style="Black.TNotebook")
        }
        self.inner_notebook["location_a"].place(x=265, y=130)
        self.inner_notebook["location_b"].place(x=265, y=130)
        frame_width = 120
        frame_hight = 320
        self.inner_frame = {"location_a":{"master":tk.Frame(self.inner_notebook["location_a"], width=frame_width, height=frame_hight,bg="black",borderwidth=0,highlightthickness=0),
                    "copy_1":tk.Frame(self.inner_notebook["location_a"], width=frame_width, height=frame_hight,bg="black",borderwidth=0,highlightthickness=0),
                    "copy_2":tk.Frame(self.inner_notebook["location_a"], width=frame_width, height=frame_hight,bg="black",borderwidth=0,highlightthickness=0)},
                    "location_b":{"master":tk.Frame(self.inner_notebook["location_b"], width=frame_width, height=frame_hight,bg="black",borderwidth=0,highlightthickness=0),
                    "copy_1":tk.Frame(self.inner_notebook["location_b"], width=frame_width, height=frame_hight,bg="black",borderwidth=0,highlightthickness=0),
                    "copy_2":tk.Frame(self.inner_notebook["location_b"], width=frame_width, height=frame_hight,bg="black",borderwidth=0,highlightthickness=0)}}
        self.inner_canvas = {"location_a":{},"location_b":{}}
        self.makepara = {"location_a":{},"location_b":{}}
        
        for loc in ["location_a", "location_b"]:
            for key in ["master", "copy_1", "copy_2"]:
                self.inner_notebook[loc].add(self.inner_frame[loc][key], text=key)
                self.inner_canvas[loc][key] = tk.Canvas(self.inner_frame[loc][key], width=150, height=340, bg="black",borderwidth=0,highlightthickness=0)
                self.inner_canvas[loc][key].place(x = 0, y = 0)
                self.makepara[loc][key] = MakeParameter(self.inner_canvas[loc][key],loc)
                
                #self.makepara[loc][key].make_pos_velo_img()
                
                
    def make_button(self,master):
        button_hight = 106
        button_widh = 50
        hight = 95
        select_button = {"location_a":{},"location_b":{}}
        for loc in ["location_a", "location_b"]:
            for key in ["master", "copy_1", "copy_2"]:
                select_button[loc][key] = tk.Button(master,command=lambda l=loc, k=key: self.set_para(l, k),
                        height=button_hight,width=button_widh,image=self.select_button[key],borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
                select_button[loc][key].place(x=900,y=hight)
                hight += 100
            hight = 570
        
        
    def push_master(self,data):
        for loc in ["location_a", "location_b"]:
            self.inner_notebook[loc].select(self.inner_frame[loc][self.push_key[loc]])
            self.makepara[loc][self.push_key[loc]].make_pos_velo_fig(data[loc],self.push_key[loc] )
            
            if self.push_key[loc] == "master":
                robot_text = "MASTER"
            elif self.push_key[loc] == "copy_1":
                robot_text = "COPY_01"
            else :
                robot_text = "COPY_02"
            self.fig_canvas[loc].itemconfig(self.robot_text[loc],text = robot_text)
            self.fig_canvas[loc].tag_raise(self.robot_text[loc])
        
    def set_para(self, loc,key):
        self.push_key[loc] = key
             
                
                
class MakeParameter():
    def __init__(self,inner_canvas, location):
        self.inner_canvas = inner_canvas
        self.location_name = location
        
        # 各パラメータ
        basepos = 10
        offset = 47.2
        xbasepos = 0
        fontsize = 20
        self.pos_x_text = self.inner_canvas.create_text(xbasepos, basepos, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.pos_y_text = self.inner_canvas.create_text(xbasepos, basepos+offset, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.pos_theta_text = self.inner_canvas.create_text(xbasepos, basepos+2*offset, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.vel_x_text = self.inner_canvas.create_text(xbasepos, basepos+3*offset, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.vel_y_text = self.inner_canvas.create_text(xbasepos, basepos+4*offset, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.vel_theta_text = self.inner_canvas.create_text(xbasepos, basepos+ 5*offset, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.count_text = self.inner_canvas.create_text(xbasepos, basepos+ 6*offset, text="", font=("HGSゴシックE", fontsize,), fill="goldenrod2", anchor='nw')
        self.data = [0]*19

    def make_pos_velo_fig(self,data,key):
        self.data = data
        robot_num = 0
        if key == "master":
            robot_num = 0
        elif key == "copy_1":
            robot_num = 6
        elif key == "copy_2":
            robot_num = 12
            
        if len(data) < robot_num + 6 or len(data) <= 18:
            print(f"[警告] dataの長さが不足しています: len={len(data)}, robot_num={robot_num}")
            return
        
        self.inner_canvas.itemconfig(self.pos_x_text, text=str(self.data[0+robot_num]))
        self.inner_canvas.itemconfig(self.pos_y_text, text=str(self.data[1+robot_num]))
        self.inner_canvas.itemconfig(self.pos_theta_text, text=str(data[2+robot_num]))
        self.inner_canvas.tag_raise(self.pos_x_text)
        self.inner_canvas.tag_raise(self.pos_y_text)
        self.inner_canvas.tag_raise(self.pos_theta_text)
        self.inner_canvas.itemconfig(self.vel_x_text, text=format(self.data[3+robot_num], ".4f"))
        self.inner_canvas.itemconfig(self.vel_y_text, text=format(self.data[4+robot_num], ".4f"))
        self.inner_canvas.itemconfig(self.vel_theta_text, text=format(self.data[5+robot_num], ".4f"))
        self.inner_canvas.tag_raise(self.vel_x_text)
        self.inner_canvas.tag_raise(self.vel_y_text)
        self.inner_canvas.tag_raise(self.vel_theta_text)
        self.inner_canvas.itemconfig(self.count_text, text=str(self.data[18]))
        self.inner_canvas.tag_raise(self.count_text)
    