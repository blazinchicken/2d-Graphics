from PIL import Image
import numpy as np

image = Image.open('./frog.jpg')
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