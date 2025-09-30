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
    file_path = filedialog.askopenfilename()
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
    image.save('./bw.png')

###

window = tkinter.Tk()

window.title("Image Editing Software")

label = tkinter.Label(window, text="Welcome to my Image Editing Software!").pack()

button = tkinter.Button(window, text="browse", command=choose_file).pack()
button = tkinter.Button(window, text="Make Image Black and White", command=bw).pack()

window.mainloop()