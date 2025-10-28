from PIL import Image
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog

class application(tk.Frame):
    
    def  __init__(self, root):
        
        self.current_page_index = 0
        self.pages = []
        self.color1 = "#135E4B"
        self.color2 = "#4CB572"
        self.color3 = "#A1D8B5"
        self.color4 = "#CCDCDB"
        self.color5 = "WHITE"
        self.color6 = "BLACK"
        
        super().__init__(
            root,
            bg = self.color2
        )
        
        self.main_frame = self
        
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        for i in range(3):
            self.main_frame.rowconfigure(i, weight=1)
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=3)
        
        self.main_frame.rowconfigure(1, weight=3)
        
        self.load_main_widgets()
    
    def load_main_widgets(self):
        self.create_main_container()
        self.create_title_display()
        self.create_function_menu()
        self.create_image_select()
        #self.pages[self.current_page_index]()
    
    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
    
    def create_main_container(self):
        self.main_container = tk.Frame(
            self.main_frame,
            background=self.color3
        )
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
        self.main_container.grid(column=0, row=1, sticky=tk.NSEW)
    
    def create_title_display(self):
        self.title_container = tk.Frame(
            self.main_frame,
            background=self.color2,
        )
        self.title_container.columnconfigure(0, weight=1)
        self.title_container.rowconfigure(1, weight=1)
        
        self.title_container.grid(column=0, row=0, sticky=tk.NSEW)
    
    def create_image_select(self):
        self.image_select = tk.Frame(
            self.main_frame,
            background=self.color2
        )
        self.image_select.columnconfigure(0, weight=1)
        self.image_select.rowconfigure(1, weight=1)
        
        self.image_select.grid(column=0, row=2, sticky=tk.NSEW)
        
        def choose_file(self):
            global imageFileName
            file_path = filedialog.askopenfilename(
                title= "select an image file",
                filetypes=[("Image files","*.jpg *.jpeg")]
            )
            if file_path:
                imageFileName = str(file_path)
            transformImage(imageFileName)
            
        def transformImage(self, image, transform):
            image = Image.open(imageFileName)
            raster = image.load()
            w = image.width
            h = image.height
            transforms = [transform]
            
            scaleDownFactor = 0
            
            scaleUp = ["scaleUp", (int(w), int(h)), np.array([[1/scaleDownFactor, 0, 0],
                                                              [0, 1/scaleDownFactor, 0],
                                                              [0, 0, 1]])]
            
            scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                                      [0, scaleDownFactor, 0],
                                                                                                      [0,               0, 1]])]

            for name, size, matrix in transforms:
    
                openImage = Image.new("RGB", size)
                openRaster = openImage.load()


                invMatrix = np.linalg.inv(matrix)

                for x in range(openImage.width):
                    for y in range(openImage.height):
                        vector = np.array([x, y, 1])
                        result = invMatrix @ vector

                        xp = int(result[0])
                        yp = int(result[1])

                        if 0 <= xp < image.width and 0 <= yp < image.height:
                            newRaster[x, y] = raster[xp, yp]
                    
                
        file_button = tk.Button(
            self.image_select,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            width=15,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Choose an Image",
            command=lambda button = self:choose_file(button)
        )
        
        file_button.grid(column=0, row=1)
    
    def create_function_menu(self):
        self.canvas = tk.Canvas(
            self.main_frame,
            background=self.color4
        )
        self.scrollbar = tk.Scrollbar(
            self.main_frame,
            orient='vertical',
            command=self.canvas.yview
        )
        self.function_menu = tk.Frame(
            self.canvas,
            background=self.color4
        )
        
        self.canvas.grid(column=1, row=0, rowspan=3, sticky=tk.NSEW)
        self.scrollbar.grid(column=2, row=0, rowspan=3, sticky=tk.NS)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.function_menu.bind(
            '<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.function_menu, anchor="nw")
        
        self.function_menu.columnconfigure(0, weight=1)
        self.function_menu.rowconfigure(0, weight=1)
        
    
root = tk.Tk()
root.title("2D Graphical Interface")
root.geometry("1280x860")
root.resizable(width = False, height = False)
my_app_instance = application(root)
root.mainloop()