from PIL import Image, ImageTk
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog
import random

class application(tk.Frame):
    
    def  __init__(self, root):
        
        self.current_page_index = 0
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
    
    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
    
    def create_main_container(self):
        self.main_container = tk.Frame(
            self.main_frame,
            background=self.color3,
            width=1000,
            height=600
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
            text="Image Editor"
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
            
    def transformImageforViewing(self, image:Image, switch:int=None):
        if not switch:
            image = Image.open(imageFileName)
        raster = image.load()
        w = image.width
        h = image.height
        highestValue = max(w,h)
        scaleDownFactor = round((700/highestValue),3)
            
        scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                                      [0, scaleDownFactor, 0],
                                                                                                      [0,               0, 1]])]

        transforms = [scaleDown]
            
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
        
    def display_image(self, image:Image):
        
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

        k = 8
        iterations = 10
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
        self.transformImageforViewing(finalImage, 1)
        finalImage.save('./andyWarhol.png')
        
    """============================================================="""
        
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
                
        self.transformImageforViewing(finalImage, 1)
        finalImage.save("./sepia.png")
        
    """============================================================="""
    
    def pixelate(self):
        image = Image.open(imageFileName)
        raster = image.load()

        w = image.width
        h = image.height

        scaleDownFactor = .25

        scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                                [0, scaleDownFactor, 0],
                                                                                                [0,               0, 1]])]

        scaleUp = ["scaleUp", (int(w), int(h)), np.array([[1/scaleDownFactor, 0, 0],
                                                        [0, 1/scaleDownFactor, 0],
                                                        [0, 0, 1]])]

        transforms = [scaleDown]
        transform2 = [scaleUp]

        for name, size, matrix in transforms:
            
            newImage = Image.new("RGB", size)
            newRaster = newImage.load()


            invMatrix = np.linalg.inv(matrix)

            for x in range(newImage.width):
                for y in range(newImage.height):
                    vector = np.array([x, y, 1])
                    result = invMatrix @ vector

                    xp = int(result[0])
                    yp = int(result[1])

                    if 0 <= xp < image.width and 0 <= yp < image.height:
                        newRaster[x, y] = raster[xp, yp]
                        
        for name, size, matrix in transform2:
            
            finalImage = Image.new("RGB", size)
            finalRaster = finalImage.load()


            invMatrix = np.linalg.inv(matrix)

            for y in range(finalImage.height):
                for x in range(finalImage.width):
                    vector = np.array([x, y, 1])
                    result = invMatrix @ vector

                    xp = int(result[0])
                    yp = int(result[1])

                    if 0 <= xp < newImage.width and 0 <= yp < newImage.height:
                        finalRaster[x, y] = newRaster[xp, yp]

            self.transformImageforViewing(finalImage, 1)
            finalImage.save("pixelate.png")
        
    """============================================================="""
        
    def vignette(self):
            image = Image.open(imageFileName)
            raster = image.load()

            imageCenter = (image.width/2, image.height/2)
            imageX, imageY = imageCenter

            vignetteScale = imageY*1.2

            print(imageCenter)

            #distance formula = sqrt((x2-x1)**2 + (y2-y1)**2)
            def distance(x1,x2,y1,y2):
                d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                return d

            for x in range(image.width):
                for y in range(image.height):

                    pixel = raster [x,y]

                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]

                    #v = int(.2*r + .7*g + .1*b)
                    powerScale = 0
                    
                    if(distance(imageX, x, imageY, y) >= vignetteScale):
                        powerScale = (((distance(imageX, x, imageY, y)) - vignetteScale)*5)

                        #print(powerScale)

                        if(powerScale < 0):
                            break

                        r = r - int(powerScale)
                        g = g - int(powerScale)
                        b = b - int(powerScale)
                    
                        raster[x,y] = (r, g, b)
                    else:
                        raster[x, y] = (r, g, b)
            
            self.transformImageforViewing(image, 1)
            image.save('./bw_vignette.png')
            
    """============================================================="""
    
    def color_inversion(self):
        image = Image.open(imageFileName)
        raster = image.load()
        
        def rgb_to_hsv(r, g, b):
            _max = max(r, g, b)
            _min = min(r, g, b)
            _diff = _max-_min

            v = _max
            if v == 0:
                return 0, 0, 0
            
            s = (_max-_min)/_max
            if s == 0:
                return 0, s, v
            
            if r == _max:
                h = (360 + ((g-b)*60/_diff))%360
            elif g == _max:
                h = 120 + ((b-r)*60/_diff)
            elif b == _max:
                h = 240 + ((r-g)*60/_diff)
            
            return h, s, v

        def hsv_to_rgb(h, s, v):
            _max = v
            _min = _max - s*_max

            f = (_max-_min)/60


            if h < 60: return (_max, ((h-0)*f+_min), _min)
            if h < 120: return ((_min-(h-120)*f), _max, _min)
            if h < 180: return (_min, _max, (_min-(h-120)*f))
            if h < 240: return (_min, (_min-(h-240)*f), _max)
            if h < 300: return (((h-240)*f+_min), _min, _max)
            if h < 360: return (_max, _min, (_min-(h-360)*f))
            
        for x in range(image.width):
            for y in range(image.height):
                r, g, b, *_ = raster[x,y]

                h, s, v = rgb_to_hsv(r, g, b)
                #line that inverts
                h = (h + 180) % 360
                r, g, b = hsv_to_rgb(h, s, v)


                raster[x,y] = (int(r), int(g), int(b))
        self.transformImageforViewing(image, 1)
        image.save("./hsvConversion.png")
        
    """============================================================="""
        
    def transform(self, transformType):
        image = Image.open(imageFileName)
        raster = image.load()

        w = image.width
        h = image.height
        chosen = ""

        scaleDownFactor = .25

        scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                                [0, scaleDownFactor, 0],
                                                                                                [0,               0, 1]])]

        scaleUp = ["scaleUp", (int(w), int(h)), np.array([[1/scaleDownFactor, 0, 0],
                                                        [0, 1/scaleDownFactor, 0],
                                                        [0, 0, 1]])]
        
        horizontalFlip = ["horizontalFlip", (w, h), np.array([[-1, 0, w-1],
                                                            [0,  1,   0],
                                                            [0,  0,   1]])]

        translate = ["translate", (w,h), np.array([[1, 0,  100],
                                                [0, 1, -200],
                                                [0, 0,    1]])]

        radians = math.radians(45)

        rotationMatrix = np.array([[math.cos(radians), -math.sin(radians), 0],
                                [math.sin(radians), math.cos(radians),   0],
                                [0,               0,                     1]])

        corners = [np.array([0, 0, 1]), np.array([w, 0, 1]), np.array([w, h, 1]), np.array([0, h, 1])]
        rotatedCorners = [rotationMatrix @ corner for corner in corners]

        xs = [rotatedCorner[0] for rotatedCorner in rotatedCorners]
        ys = [rotatedCorner[1] for rotatedCorner in rotatedCorners]

        newWidth = int(max(xs) - min(xs))
        newHeight = int(max(ys) - min(ys))
        newSize = (newWidth, newHeight)

        shiftUpLeft = np.array([[1, 0, -w/2],
                                [0, 1, -h/2],
                                [0, 0,    1]])

        shiftDownRight = np.array([[1, 0, newWidth/2],
                                [0, 1, newHeight/2],
                                [0, 0, 1]])

        centeredRotation = shiftDownRight @ rotationMatrix @ shiftUpLeft

        rotation = ["rotation", newSize, centeredRotation]
        
        if transformType == "rotation":
            chosen = rotation
        elif transformType == "horizontalFlip":
            chosen = horizontalFlip
        elif transformType == "translate":
            chosen = translate
        elif transformType == "scaleDown":
            chosen = scaleDown
        elif transformType == "scaleUp":
            chosen = scaleUp
        else:
            return None
        transforms = [chosen]

        for name, size, matrix in transforms:
            newImage = Image.new("RGB", size)
            newRaster = newImage.load()
            
            invMatrix = np.linalg.inv(matrix)
            
            for x in range(newImage.width):
                for y in range(newImage.height):
                    vector = np.array([x, y, 1])
                    result = invMatrix @ vector
                    
                    xp = result[0]
                    yp = result[1]
                    
                    if 0 <= xp < image.width and 0 <= yp < image.height:
                        newRaster[x, y] = raster[int(xp), int(yp)]
                        
        self.transformImageforViewing(newImage, 1)
        newImage.save(name + ".png")
        
    """============================================================="""
        
    def watermark(self):
        image = Image.open(imageFileName)
        raster = image.load()

        watermark = Image.open('./TestWatermark.png').convert("RGB")
        watermarkRaster = watermark.load()

        opacity = .4

        offsetX = image.width - watermark.width
        offsetY = image.height - watermark.height

        for y in range(watermark.height):
            for x in range(watermark.width):
                wr, wg, wb = watermarkRaster[x,y]
                
                imageX = x + offsetX
                imageY = y + offsetY
                
                r, g, b = raster[imageX, imageY]
                
                newR = int(r * (1-opacity) + wr * opacity)
                newG = int(g * (1-opacity) + wg * opacity)
                newB = int(b * (1-opacity) + wb * opacity)
                
                
                raster[imageX, imageY] = (newR, newG, newB)
        
        self.transformImageforViewing(image, 1)
        image.save('./watermark.png')
        
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
            text="Scale Up",
            command=lambda: self.transform("scaleUp")
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
            text="Scale Down",
            command=lambda: self.transform("scaleDown")
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
            text="Rotate",
            command=lambda: self.transform("rotation")
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
            text="Translate",
            command=lambda: self.transform("translate")
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
            text="Horizontal Flip",
            command=lambda: self.transform("horizontalFlip")
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
        file_button7 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Pixelate",
            command=self.pixelate
        )
        
        file_button7.pack(pady=10, padx=10)
        file_button8 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Vignette",
            command=self.vignette 
        )
        
        file_button8.pack(pady=10, padx=10)
        file_button9 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Color Inversion",
            command=self.color_inversion 
        )
        
        file_button9.pack(pady=10, padx=10)
        file_button10 = tk.Button(
            self.function_menu,
            background=self.color1,
            foreground=self.color5,
            activebackground=self.color1,
            activeforeground=self.color5,
            relief=tk.FLAT,
            font=("Arial", 26),
            text="Watermark",
            command=self.watermark 
        )
        
        file_button10.pack(pady=10, padx=10)
root = tk.Tk()
root.title("2D Graphical Interface")
root.geometry("1280x860")
root.resizable(width = False, height = False)
my_app_instance = application(root)
root.mainloop()