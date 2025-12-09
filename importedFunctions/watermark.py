from PIL import Image
import numpy as np
"""
how to do this

1. open image for watermark
2. open watermark
3. determine where we want the watermark (placed in bottom right of the image.)
4. loop over watermark, saving all the information within the raster
5. when going to loop for the watermark, can add to the base image by just saving over the x + offsetX and y accordingly
"""
image = Image.open('./frog.jpg')
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
        
image.save('./watermark.png')