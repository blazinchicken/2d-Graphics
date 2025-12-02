from PIL import Image
import numpy as np
import math

fileName = input("Enter File Name: (format as ./fileneame.jpg)")

image = Image.open(fileName)
raster = image.load()

imageCenter = (image.width/2, image.height/2)
imageX, imageY = imageCenter

vignetteScale = 200

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
 
image.save('./bw_vignette.png')