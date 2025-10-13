from PIL import Image
import numpy as np

image = Image.open('./frog.jpg')
raster = image.load()

def rgb_to_cmyk(r, g, b):
    pr = r/255
    pg = g/255
    pb = b/255
    
    pk = 1-max(pr, pg, pb)
    
    if pk == 1:
        return (0, 0, 0, pk*100)
    
    c = (1-pr-pk)/(1-pk)
    m = (1-pg-pk)/(1-pk)
    y = (1-pb-pk)/(1-pk)
    
    return (c*100, m*100, y*100, pk*100)

def cmyk_to_rgb(c, m, y, k):
    pc = c/100
    pm = m/100
    py = y/100
    pk = k/100
    
    

for x in range(image.width):
    for y in range(image.height):
        pixel = raster [x,y]
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        
    
        c, m, _y, k = rgb_to_cmyk(r, g, b)
        
        raster[x, y] = tuple([int(i*255/100) for i in [k, k, k]])
        
image.save('./cmyk.png')  