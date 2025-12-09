from PIL import Image
import numpy as np
import math


image = Image.open('./frog.jpg')
raster = image.load()

w = image.width
h = image.height

horizontalFlip = ["horizontalFlip", (w, h), np.array([[-1, 0, w-1],
                                                      [0,  1,   0],
                                                      [0,  0,   1]])]

translate = ["translate", (w,h), np.array([[1, 0,  100],
                                           [0, 1, -200],
                                           [0, 0,    1]])]

radians = math.radians(45)

rotationMatrix = np.array([[math.cos(radians), -math.sin(radians), 0],
                           [math.sin(radians), math.cos(radians),   0],
                           [0,               0,                     1]])

corners = [np.array([0, 0, 1]), np.array([w, 0, 1]), np.array([w, h, 1]), np.array([0, h, 1])]
rotatedCorners = [rotationMatrix @ corner for corner in corners]

xs = [rotatedCorner[0] for rotatedCorner in rotatedCorners]
ys = [rotatedCorner[1] for rotatedCorner in rotatedCorners]

newWidth = int(max(xs) - min(xs))
newHeight = int(max(ys) - min(ys))
newSize = (newWidth, newHeight)

shiftUpLeft = np.array([[1, 0, -w/2],
                        [0, 1, -h/2],
                        [0, 0,    1]])

shiftDownRight = np.array([[1, 0, newWidth/2],
                           [0, 1, newHeight/2],
                           [0, 0, 1]])

centeredRotation = shiftDownRight @ rotationMatrix @ shiftUpLeft

rotation = ["rotation", newSize, centeredRotation]

transforms = [horizontalFlip]

for name, size, matrix in transforms:
    newImage = Image.new("RGB", size)
    newRaster = newImage.load()
    
    invMatrix = np.linalg.inv(matrix)
    
    for x in range(newImage.width):
        for y in range(newImage.height):
            vector = np.array([x, y, 1])
            result = invMatrix @ vector
            
            xp = result[0]
            yp = result[1]
            
            if 0 <= xp < image.width and 0 <= yp < image.height:
                newRaster[x, y] = raster[int(xp), int(yp)]

newImage.save(name + ".png")