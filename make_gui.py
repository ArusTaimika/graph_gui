import tkinter as tk
from PIL import Image, ImageTk  # 必要
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from concurrent.futures import ThreadPoolExecutor
from matplotlib.gridspec import GridSpec   

from make_graph import MakeGraph, MakeleftWindow
from digital_clock import DigitalClockApp_Text
from save_csv import CSVLoggerApp
from receve_data import ReceveData
from get_ip import GetIP
from select_location import SelectLocation
from connect_copy_robot import ConnectCopyRobot
from make_copy_graph import TimeDelay

class Application(tk.Frame):
    def __init__(self, master=None):
        self.recevedata ={"location_a":ReceveData(50222,18,1),"location_b":ReceveData(51222,18,1),
                          "raspi-a":ReceveData(52222,7,1),"raspi-b":ReceveData(53222,7,1)}
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.running = False

        super().__init__(master)
        self.master = master
        self.master.title('matplotlib graph')
        self.plot_id = None
        
        self.init_start_end() 
        self.write_ipport()
        self.init_make_graph()
        self.init_make_para()
        self.init_make_timedelay_graph()
        self.init_make_digital_clock()
        self.make_button()
        self.init_csv()
        self.init_select_location()
        
        #self.init_connect_copyrobot()
        
    def init_make_digital_clock(self):
        """時計の初期化
        """
        self.clock_canvas = tk.Canvas(self.master , width=450, height=210, bg='black'  ,bd=0,highlightthickness=0) # 1054*470
        self.clock_canvas.place(x = 440, y = 10)
        self.digital_clock = DigitalClockApp_Text(self.clock_canvas)
        self.update_clock()
        
    def init_make_graph(self):
        """グラフ領域の初期化
        """
        # matplotlib配置用フレーム
        graph_frame = tk.Frame(self.master,width=700, height=1000, bg = 'black')
        graph_frame.pack(side="right",anchor="n")
        graph_frame.pack_propagate(False)
        # 描画領域
        fig = Figure(facecolor='black')
        fig.subplots_adjust(top=0.95, bottom=0.05, left=0.1, right=1, hspace=0.2)
        self.ax = {"location_a":fig.add_subplot(2, 1, 1),"location_b":fig.add_subplot(2, 1, 2) }
        self.ax["location_a"].set_facecolor('black')
        self.ax["location_b"].set_facecolor('black')
        self.fig_canvas = FigureCanvasTkAgg(fig, graph_frame)
        self.fig_canvas.get_tk_widget().place(x=0, y=0, width= 700  , height=1000)
        self.makegraph = MakeGraph(self.ax, self.fig_canvas)
        self.return_data = {"location_a":[0]*19,"location_b":[0]*19}
        
        graph_frame.pack()
    
    def init_make_para(self):
        """パラメータ領域の初期化
        """
        para_canvas = {"location_a":tk.Canvas(self.master , width=450, height=470, bg='black'  ,bd=0,highlightthickness=0),
                       "location_b":tk.Canvas(self.master , width=450, height=470, bg='black'  ,bd=0,highlightthickness=0)} # 1054*470
        para_canvas["location_a"].place(x =880,y = 10)
        para_canvas["location_b"].place(x =880,y = 490)
        self.makeleftwindow = MakeleftWindow(para_canvas)
        
        self.makeleftwindow.make_noteobok()
        
    def init_make_timedelay_graph(self):
        self.copy_data = {"raspi-a":[],"raspi-b":[]}
        
        self.timedelay_frame = tk.Frame(self.master,width=450, height=960, bg = 'black')
        self.timedelay_frame.place(x = 450, y = 220)
        self.timedelay_frame.pack_propagate(False)
        # 描画領域
        fig = Figure(facecolor='black')
        fig.subplots_adjust(top=0.95, bottom=0.2, left=0.1, right=0.9, hspace=0.2)
        # 上：1行1列のレイアウトの1番目（全幅）
        
        # 下：1行2列のレイアウトをグリッドで作るため GridSpec を使う
        # 下段左右の極座標グラフ
        gs = GridSpec(2, 2, height_ratios=[1, 3], figure=fig)
        ax0 = fig.add_subplot(gs[0, :])  # 全幅
        ax1 = fig.add_subplot(gs[1, 0], projection='polar')  # 左下
        ax2 = fig.add_subplot(gs[1, 1], projection='polar')  # 右下
        self.axes = [ax0, ax1, ax2]
        self.axes[0].set_facecolor('black')
        self.axes[0].set_position([0.08, 0.75, 0.92, 0.23])  # 左下の位置調整
        self.axes[1].set_facecolor('black')
        self.axes[1].set_position([0, 0, 0.5, 0.5])  # 左下の位置調整
        self.axes[2].set_facecolor('black')
        self.axes[2].set_position([0.5, 0, 0.5, 0.5])  # 左下の位置調整
        self.timedelay_canvas = FigureCanvasTkAgg(fig, self.timedelay_frame)
        self.timedelay_canvas.get_tk_widget().place(x=0, y=50, width= 450  , height=800)
        self.maketimedelaygraph = TimeDelay(self.axes, self.timedelay_canvas, self.timedelay_frame)
    
    def init_start_end(self):
        """開始と終了エリアの初期化
        """
        self.info_canvas = tk.Canvas(self.master , width=900, height=470, bg='black'  ,bd=0,highlightthickness=0)
        self.info_canvas.place(x = 0, y = 0)
        dir = "image_folder/"
        entry_img = Image.open(dir+"entry_start.png").resize((104, 117))# パスは必要に応じて調整
        abort_img = Image.open(dir+"entry_abort.png").resize((104, 117))# パスは必要に応じて調整
        self.startabort = {"start":ImageTk.PhotoImage(entry_img)
            ,"abort":ImageTk.PhotoImage(abort_img)}
        info_img = Image.open(dir+"info.png").resize((420, 190))# パスは必要に応じて調整
        self.info_img = ImageTk.PhotoImage(info_img)
        self.info_canvas.create_image(10,20, image = self.info_img, anchor = 'nw')
        a_status_img = Image.open(dir+"a_status.png").resize((90, 135))
        b_status_img = Image.open(dir+"b_status.png").resize((90, 135))
        
        self.loc_status = {"location_a":ImageTk.PhotoImage(a_status_img)
            ,"location_b":ImageTk.PhotoImage(b_status_img)}
        self.status_image_id = {"location_a":None,"location_b":None}
        self.datamiss_label = {"location_a":None,"location_b":None}
        self.status_flag  = {"location_a":True,"location_b":True}
        self.datamiss_flag  = {"location_a":True,"location_b":True}
    
        img = Image.open(dir+"data_miss.png").resize((430, 175))
        self.datamiss = ImageTk.PhotoImage(img)
        
    def init_csv(self):
        csv_frame = tk.Frame(self.master,width= 440, height=300, bg = 'black')#,borderwidth=0,highlightthickness=0)
        csv_frame.place(x = 10,y = 430)
        save_csv = CSVLoggerApp(csv_frame,self.recevedata)
    
    def init_select_location(self):
        """位置選択の初期化
        """
        self.select_canvas = tk.Canvas(self.master , width=400, height=450, bg='black'  ,bd=0,highlightthickness=0) # 1054*470
        self.select_canvas.place(x = 10, y = 700)
        self.select_location = SelectLocation(self.select_canvas)
        self.select_location.select_button(self.makeleftwindow, self.maketimedelaygraph)
    
    def init_connect_copyrobot(self):
        self.connect_canvas = tk.Canvas(self.master , width=400, height=450, bg='black'  ,bd=0,highlightthickness=0) # 1054*470     
        self.connect_canvas.place(x = 500, y = 440)
        self.connect_copyrobot = ConnectCopyRobot(self.connect_canvas, self.select_location)
    
        
    def write_ipport(self):
        """ IP Port番号の記載
        """
        getip = GetIP()
        self.info_canvas.create_text(250,80, text=getip.get_ip_address(), font=("Bahnschrift Condensed", 20), fill="goldenrod2", anchor='nw')
        self.info_canvas.create_text(250,122, text="5 0 2 2 2", font=("Bahnschrift Condensed", 20), fill="goldenrod2", anchor='nw')
        self.info_canvas.create_text(250,164, text="5 1 2 2 2", font=("Bahnschrift Condensed", 20), fill="goldenrod2", anchor='nw')
    
    def run_status(self,loc):
        """実行中の表示
        """
        if loc == "location_a":
            xpos = 250
            ypos = 150
        else:
            xpos = 350
            ypos = 650
        if self.recevedata[loc].timeout_flag and self.status_flag[loc]:
            self.status_image_id[loc] = self.info_canvas.create_image(xpos,205, image = self.loc_status[loc], anchor = 'nw')
            self.delete_datamiss(loc)
            self.status_flag[loc]= False
        elif not self.recevedata[loc].timeout_flag and self.datamiss_flag[loc]:
            self.delete_status(loc)
            self.datamiss_label[loc] = tk.Label(self.master, image=self.datamiss,bg="black",borderwidth=0,highlightthickness=0)
            self.datamiss_label[loc].place(x = 1400, y = ypos)
            self.datamiss_flag[loc] = False
            
    def delete_status(self,loc):
        """実行中の削除
        """
        if self.status_image_id[loc] is not None:
            self.info_canvas.delete(self.status_image_id[loc])
            self.status_flag[loc] = True
            
    def delete_datamiss(self,loc):
        if self.datamiss_label[loc] is not None:
            self.datamiss_label[loc].destroy()
            self.datamiss_flag[loc] = True

    def plot_data(self):
        """dataのプロット
        """
        for loc in ["location_a", "location_b"]:          
            self.return_data[loc] = self.makegraph.convert_data(loc,self.recevedata[loc].queue)
            self.makegraph.cal_graph(loc)
            self.run_status(loc)    
        self.makeleftwindow.push_master(self.return_data)
        self.makegraph.draw()
        
        for ras in ["raspi-a", "raspi-b"]:
                self.maketimedelaygraph.convert_data(ras, self.recevedata[ras].queue)
        self.maketimedelaygraph.plot_timedelay()
        self.maketimedelaygraph.plot_polar_data()
        self.maketimedelaygraph.draw()
        
        
        self.plot_id  = self.after(50, self.plot_data)

        
    def update_clock(self):
        """時計のupdate
        """
        self.digital_clock.update_clock()
        self.after(1000, self.update_clock)


    def make_button(self):
        """ボタンの作成
        """
        self.start_button = tk.Button(self.info_canvas, text='', command = self.app_start,
                                 height=117,width=104,image=self.startabort["start"],borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        self.end_button = tk.Button(self.info_canvas, text='', command = self.app_stop,
                                 height=117,width=104,image=self.startabort["abort"],borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
        self.start_button.place(x=10,y=220)
        self.end_button.place(x=120,y=220)
        self.makeleftwindow.make_button(self.master)

    def app_start(self):
        self.running = True
         # スレッドでデータ受信
        self.after(60, self.plot_data)
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.executor.submit(self.recevedata["location_a"].receive_data, "location_a" )
        self.executor.submit(self.recevedata["location_b"].receive_data, "location_b")
        self.executor.submit(self.recevedata["raspi-a"].receive_data, "raspi-a" )
        self.executor.submit(self.recevedata["raspi-b"].receive_data, "raspi-b")
    
    def app_stop(self):
        self.running = False
        if self.plot_id is not None:
            self.after_cancel(self.plot_id)
        for loc in ["location_a", "location_b"]:
            self.delete_status(loc)
            self.delete_datamiss(loc)
            self.recevedata[loc].stop()
        self.recevedata["raspi-a"].stop()
        self.recevedata["raspi-b"].stop()
        self.executor.shutdown(wait=False)
        
        
    def on_closing(self):
        self.running = False
        if self.plot_id is not None:
            self.after_cancel(self.plot_id)
            self.executor.shutdown(wait=False)
            
        self.recevedata["location_a"].stop()
        self.recevedata["location_b"].stop()
        self.recevedata["raspi-a"].stop()
        self.recevedata["raspi-b"].stop()
        self.master.destroy()




if __name__=='__main__':
    root = tk.Tk()
    root.geometry("1920x1080") 
    root.configure(bg="black")
    app = Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
