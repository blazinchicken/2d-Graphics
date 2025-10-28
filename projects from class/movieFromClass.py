from PIL import Image
import numpy as np
import math

image = Image.open('./frog.jpg')
raster = image.load()

frames = []

max_frame = 100

def nearestNeighbor2D(x, y):
    if(0<=x<image.width and 0<=y<image.height):
        return raster[int(x), int(y)]   
    else:
        return (0,0,0)
    
def linear_1d(one, two, p):
    return[(1-p)*a+p*b for a, b in zip(one, two)]

def bilinear_2d(x, y):
    if (x <= 0 or x >= image.width-1 or y<=0 or y>=image.height-1):
        return nearestNeighbor2D(x,y)
    
    A = raster[int(x), int(y)]
    B = raster[int(x)+1, int(y)]
    C = raster[int(x), int(y)+1]
    D = raster[int(x)+1, int(y)+1]

    x_factor = x - int(x)
    y_factor = y - int(y)

    top = linear_1d(A, B, x_factor)
    bottom = linear_1d(C, D, x_factor)
    middle = linear_1d(top, bottom, y_factor)

    return tuple([int(i) for i in middle])


for i in range(max_frame):
    frame = Image.new("RGB", (image.width, image.height))
    frameRaster = frame.load()
    
    scaleMatrix = np.array([
                [1+i/max_frame, 0, 0],
                [0, 1+i/max_frame, 0],
                [0, 0, 1]
            ])

    inv_matrix = np.linalg.inv(scaleMatrix)
    
    for x in range(image.width):
        for y in range(image.height):
            
            vector = np.array([x, y, 1])

            coords = inv_matrix @ vector

            

            frameRaster[x,y] = bilinear_2d(coords[0], coords[1])

        
            
    frames.append(frame)
            
frames[0].save(
    "movieFromClass.png",
    save_all = True,
    append_images = frames[1:],   
    duration = 100, 
    loop = 0
)