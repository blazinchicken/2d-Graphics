from PIL import Image
import numpy as np
import math
import tkinter
from tkinter import filedialog


imageFileName = ""
###

def say_hello():
    print("hello")

def choose_file():
    global imageFileName
    file_path = filedialog.askopenfilename(
        title= "select an image file",
        filetypes=[("Image files","*.jpg *.jpeg")]
    )
    if file_path:
        imageFileName = str(file_path)


def bw():
    image = Image.open(imageFileName)
    raster = image.load()


    for x in range(image.width):
        for y in range(image.height):
            pixel = raster [x,y]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            v = int(.2*r + .7*g + .1*b)
            raster[x, y] = (v, v, v)
    image.save('./applicationBW.png')

def histogram():
    image = Image.open("./frog.jpg")
    raster = image.load()

    levels = [0 for _ in range(256)]

    for x in range(image.width):
        for y in range(image.height):
            pixel = raster [x,y]

            r = pixel[0]
            g = pixel[1]
            b = pixel[2]

            v = int(.2*r + .7*g + .1*b)
            levels[v] +=1

            raster[x, y] = (v, v, v)

    max_level = max(levels)

    histogram = Image.new("RGB", (256,256))
    histogramRaster = histogram.load()

    for x in range(256):
        for y in range(256):
            level = levels[x]
            if((256-y-1) < level/max_level*256):
                histogramRaster[x,y] = (x, x, x)
            else:
                histogramRaster[x,y] = (100, 100, 255)
    histogram.save("applicationHistogram.png")

def rgb_to_hsv():
    return

def hsv_to_rgb():
    return

def pixelate():
    return

###

window = tkinter.Tk()

window.title("Image Editing Software")

label = tkinter.Label(window, text="Welcome to my Image Editing Software!").pack()
blank = tkinter.Label(window, text="").pack()
browseLabel = tkinter.Label(window, text="First, pick a jpg file!").pack()
button = tkinter.Button(window, text="browse", command=choose_file).pack()
blank = tkinter.Label(window, text="", height=2, width=10).pack()
label = tkinter.Label(window, text="Image Processes! Pick One after you Pick a File!").pack()
blank = tkinter.Label(window, text="").pack()
button = tkinter.Button(window, text="Make Image Black and White", command=bw).pack()
button = tkinter.Button(window, text="Make a Histogram to Show Value in an Image!", command=histogram).pack()
button = tkinter.Button(window, text="Convert an Image to HSV from RGB", command=hsv_to_rgb).pack()
button = tkinter.Button(window, text="Convert an Image from HSV to RGB", command=rgb_to_hsv).pack()


window.mainloop()