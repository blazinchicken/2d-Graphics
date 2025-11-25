from PIL import Image, ImageTk
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog
import random

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
            background=self.color3,
            width=500,
            height=500
        )
        self.main_container.pack_propagate(False)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
        self.main_container.grid(column=0, row=1, sticky=tk.NSEW)
    
    def create_title_display(self):
        self.title_container = tk.Label(
            self.main_frame,
            background=self.color2,
            foreground=self.color6,
            font=('Ariel', 30, 'bold'),
            text="File Chosen!"
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
            command=self.choose_file
        )
        
        file_button.grid(column=0, row=1)
        
    def choose_file(self):
            global imageFileName
            file_path = filedialog.askopenfilename(
                title= "select an image file",
                filetypes=[("Image files","*.jpg *.jpeg")]
            )
            if file_path:
                imageFileName = str(file_path)
                self.transformImageforViewing(imageFileName)
            
    def transformImageforViewing(self, image):
        image = Image.open(imageFileName)
        raster = image.load()
        w = image.width
        h = image.height
        highestValue = max(w,h)
        scaleDownFactor = round((500/highestValue),3)
            
        transforms = []
            
        scaleUp = ["scaleUp", (int(w), int(h)), np.array([[1/scaleDownFactor, 0, 0],
                                                              [0, 1/scaleDownFactor, 0],
                                                              [0, 0, 1]])]
            
        scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                                      [0, scaleDownFactor, 0],
                                                                                                      [0,               0, 1]])]

        if highestValue >= 500:
            transforms = [scaleDown]
        elif highestValue < 500:
            transforms = [scaleUp]
            
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
                        openRaster[x, y] = raster[xp, yp]
        
        self.display_image(openImage)
        
    def display_image(self, image):
        
        for widget in self.main_container.winfo_children():
            widget.destroy()

        self.main_container.grid_propagate(False)
        
        self.displayImage = ImageTk.PhotoImage(image)
        display = tk.Label(
            self.main_container,
            image=self.displayImage,
            background=self.color3 
        )
        display.place(relx=0.5, rely=0.5, anchor="center")
        
    """++++++++++++++++++++++++|Functions for buttons go here|+++++++++++++++++++++++++++++++++"""
    
    def andyWarholConversion(self):
        if not imageFileName:
            return FileNotFoundError
        image = Image.open(imageFileName)
        raster = image.load()
        
        #scaledown  -  200x200/2 = 100x100, with 100 + 100 = 200
        scaleDownFactor = .5
        w = image.width
        h = image.height

        def l1_difference(a,b):
            return sum(abs(x-y) for x,y in zip(a,b))

        def closest_color(color, color_list):
            return min(color_list, key=lambda option: l1_difference(color, option))

        def random_color():
            return tuple(random.randint(0,255) for _ in range(3))

        scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                                [0, scaleDownFactor, 0],
                                                                                                [0,               0, 1]])]

        transforms = [scaleDown]

        for name, size, matrix in transforms:
            openImage = Image.new("RGB", size)
            openRaster = openImage.load()


            invMatrix = np.linalg.inv(matrix)

            for y in range(openImage.height):
                for x in range(openImage.width):
                    vector = np.array([x, y, 1])
                    result = invMatrix @ vector

                    xp = int(result[0])
                    yp = int(result[1])

                    if 0 <= xp < image.width and 0 <= yp < image.height:
                        openRaster[x, y] = raster[xp, yp]


        #kmeans pixel sampling

        k = 5
        iterations = 15
        color_count = dict()

        for y in range(openImage.height):
            for x in range(openImage.width):
                pixel = openRaster[x,y]
                if pixel not in color_count:
                    color_count[pixel] = 0
                color_count[pixel] += 1

        sorted_color_count = sorted(color_count.items(), key=lambda item:item[1], reverse=True)

        palette = [random_color() for _ in range(k)]
        for i in range(iterations):
            print(palette)
            close_color_list = [[] for _ in range(k)]

            for color_count in sorted_color_count:
                closest_palette_color = closest_color(color_count[0], palette)
                closest_index = palette.index(closest_palette_color)
                close_color_list[closest_index].append(color_count)
                
            for j in range(k):
                close_list = close_color_list[j]
                if len(close_list) == 0:
                    palette[j] = random_color()
                else:
                    sums = [0,0,0]
                    sum_weight = 0
                    for color, count in close_list:
                        sums = [a+b*count for a,b in zip(sums, color)]
                        sum_weight +=count
                    palette[j] = tuple(a//sum_weight for a in sums)

        finalImage = Image.new("RGB", (w,h))
        finalRaster = finalImage.load()

        all_palettes = [[] for _ in range(4)]

        for i in range(k):
            r, g, b, *_ = palette[i]
            
            all_palettes[0].append((r,g,b))
            all_palettes[1].append(((r+100)%255,g,b))
            all_palettes[2].append((r,(g+100)%255,b))
            all_palettes[3].append((r,g,(b+100)%255))
                
        for y in range(openImage.height):
            for x in range(openImage.width):
                pixel = openRaster[x,y]
                
                
                #want to make this more iterable, interactible and size to be defined by the user
                finalRaster[x, y] = closest_color(pixel, all_palettes[0])
                finalRaster[x+openImage.width, y] =  closest_color(pixel, all_palettes[1]) #(int(pixel[0]),int(pixel[1]),int(pixel[2]))
                finalRaster[x, y+openImage.height] = closest_color(pixel, all_palettes[2])
                finalRaster[x+openImage.width, y+openImage.height] = closest_color(pixel, all_palettes[3])
        self.display_image(finalImage)
        finalImage.save('./andyWarhol.png')
        
        
    def sepia(self): 
        finalImage = Image.open(imageFileName)
        raster = finalImage.load()
        
        for x in range(finalImage.width):
            for y in range(finalImage.height):
                r, g, b, *_ = raster[x,y]


                #algorithm found https://www.geeksforgeeks.org/java/image-processing-in-java-colored-image-to-sepia-image-conversion
                newRed = 0.393*r + 0.769*g + 0.189*b
                newGreen = 0.349*r + 0.686*g + 0.168*b
                newBlue = 0.272*r + 0.534*g + 0.131*b
                
                raster[x,y] = (int(newRed), int(newGreen), int(newBlue))
                
        self.display_image(finalImage)
        finalImage.save("./sepia.png")
        
    """++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
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
        
        file_button = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Scale Up"
        )
        
        file_button.pack(pady=10, padx=10)
        file_button1 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Scale Down"
        )
        
        file_button1.pack(pady=10, padx=10)
        file_button2 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Rotate"
        )
        
        file_button2.pack(pady=10, padx=10)
        file_button3 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Translate"
        )
        
        file_button3.pack(pady=10, padx=10)
        file_button4 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Horizontal Flip"
        )
        
        file_button4.pack(pady=10, padx=10)
        file_button5 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Andy Warhol",
            command=self.andyWarholConversion
        )
        
        file_button5.pack(pady=10, padx=10)
        file_button6 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Sepia",
            command=self.sepia
        )
        
        file_button6.pack(pady=10, padx=10)
    
root = tk.Tk()
root.title("2D Graphical Interface")
root.geometry("1280x860")
root.resizable(width = False, height = False)
my_app_instance = application(root)
root.mainloop()