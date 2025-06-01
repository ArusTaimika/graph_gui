import tkinter as tk
from PIL import Image, ImageTk  # Pillowライブラリが必要

class SelectLocation:
    def __init__(self, select_canvas):
        self.select_canvas = select_canvas
        dir = "image_folder/"
        img = Image.open(dir+"select_location.png").resize(((354, 246)))
        self.select_location_img = ImageTk.PhotoImage(img) 
        self.select_canvas.create_image(0, 0, image=self.select_location_img, anchor='nw')  
        
        self.use_location = ["location_a","location_b"]
        self.location_1_txt = self.select_canvas.create_text(128, 104, text="A", font=("Bahnschrift SemiBold Condensed", 20), fill="goldenrod2", anchor='nw')
        self.location_2_txt = self.select_canvas.create_text(128, 196, text="B", font=("Bahnschrift SemiBold Condensed", 20), fill="goldenrod2", anchor='nw')
        
    def select_button(self,makeleftwindow, maketimedelaygraph):
        """選択ボタンを作成する
        """
        dir = "image_folder/"
        self.select_locationimg = {}
        select_button = [{},{}]
        button_widh = 90
        button_hight = 40
        xpos = 170 
        ypos = 60
        
        for loc in ["location_a","location_b","location_c","location_d"]:
            img = Image.open(dir+"select_"+loc+".png").resize((90, 40))
            self.select_locationimg[loc] = ImageTk.PhotoImage(img) 
        for n in range(2):
            if n== 1:
                xpos = 170
                ypos  = 155
            for loc in ["location_a","location_b","location_c","location_d"]:
                if loc =="location_c":
                    ypos += button_hight + 3
                    xpos = 170
                select_button[n][loc] = tk.Button(self.select_canvas,command=lambda l=loc,n=n: self.set_location(l,n,makeleftwindow, maketimedelaygraph),height=button_hight,width=button_widh,
                                        image=self.select_locationimg[loc],borderwidth=0,highlightthickness=0,activebackground="goldenrod2")
                select_button[n][loc].place(x=xpos,y=ypos)
                xpos += button_widh + 10

    
    def set_location(self,loc,n,makeleftwindow, maketimedelaygraph):
        self.use_location[n] = loc
        if n == 0:
            if loc == "location_a":
                txt  = "A"
            elif loc == "location_b":
                txt  = "B"
            elif loc == "location_c":
                txt  = "C"
            elif loc == "location_d":
                txt  = "D"
            self.select_canvas.itemconfig(self.location_1_txt, text=txt)
            makeleftwindow.update_target_location(n,txt)
            maketimedelaygraph.update_location(n,txt)
        if n == 1:
            if loc == "location_a":
                txt  = "A"
            elif loc == "location_b":
                txt  = "B"
            elif loc == "location_c":
                txt  = "C"
            elif loc == "location_d":
                txt  = "D"
            self.select_canvas.itemconfig(self.location_2_txt, text=txt)
            makeleftwindow.update_target_location(n,txt)
            maketimedelaygraph.update_location(n,txt)
                
    def get_location(self):
        return self.use_location