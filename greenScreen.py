from PIL import Image
import numpy as np


image = Image.open('./greenScreenBefore.jpg').convert("RGBA")
raster = image.load()

maxGreen = 0

for x in range(image.width):
    for y in range(image.height):
        pixel = raster [x,y]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        if (g >= maxGreen):
            maxGreen = g


for x in range(image.width):
    for y in range(image.height):
        pixel = raster [x,y]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        a = pixel[3]

        if (g == maxGreen):
            a = 0
            r = 0
            g = 0
            b = 0

        raster[x, y] = (r, g, b, a)

image.save('./greenScreen.png')