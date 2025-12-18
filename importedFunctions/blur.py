from PIL import Image
import numpy as np
import math
import random
"""
    what am i doing here

    GOAL: make multiple blur functions that change the image by a bit at a time, allowing for multiple functions to be added to the GUI

    1. jitter blur
        - I was thinking that this could just be a simple randomization between the axis of a pixel, in that it would pull the color 
        values from the pixels surrounding each pixel, and then randomly choose one of the options to then go through and fill for that pixel,
        this would be extremely expensive in terms of time but would work.

    2. interpolation
        - This one seems a little faster in that it is a closest neighbor function that doesnt act in a simple matrix, would apply this for any real changes from the main one.
        
    3. spiral? 
        - This one is a different thing, and could be much harder to implement, but the goal would be to find points on the base image, write to the base image the blur points
        that are from the middle point of the image, and then proceed in a spiral so that it will be able to continue to look like a full spiral.
            - I am not sure that this is actively how I would go about doing this, but overall its odd. 
    """
def randomBlur():
    image = Image.open("./frog.jpg")
    raster = image.load()


    for y in range(1, image.height-1):
        for x in range(1, image.width-1):
                pixelRandom1 = raster[x,y-1]
                pixelRandom2 = raster[x-1,y-1]
                pixelRandom3 = raster[x-1,y]
                pixelRandom4 = raster[x-1,y+1]
                pixelRandom5 = raster[x+1,y]
                pixelRandom6 = raster[x,y+1]
                pixelRandom7 = raster[x+1,y+1]
                pixelRandom8 = raster[x+1,y-1]
                    
                randomDict = [pixelRandom1, pixelRandom2, pixelRandom3, pixelRandom4, pixelRandom5, pixelRandom6, pixelRandom7, pixelRandom8]
                    
                chosenPixel = randomDict[math.floor(random.randint(0,7))]
                    
                raster[x,y] = chosenPixel
    image.save("./blur.png")
            