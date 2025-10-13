from PIL import Image
import numpy as np


image = Image.open('./greenSquare.png').convert("RGBA")
raster = image.load()

maxGreen = 0
greenBlue = 0
greenRed = 0

for x in range(image.width):
    for y in range(image.height):
        pixel = raster[x,y]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        a = pixel[3]

        if (g >= maxGreen):
            maxGreen = g
            greenBlue = b
            greenRed = r

            print(maxGreen)
            print(greenBlue)
            print(greenRed)




for x in range(image.width):
    for y in range(image.height):
        pixel = raster[x,y]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        a = pixel[3]

        if (g >= 250):
            a = 0
            g = 0

        raster[x, y] = (r, g, b, a)


image.save('./greenScreen.png')