from PIL import Image
import numpy as np


image = Image.open('./frog.jpg')
raster = image.load()

w = image.width
h = image.height

scaleDownFactor = .25

scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                          [0, scaleDownFactor, 0],
                                                                                          [0,               0, 1]])]

scaleUp = ["scaleUp", (int(w), int(h)), np.array([[1/scaleDownFactor, 0, 0],
                                                  [0, 1/scaleDownFactor, 0],
                                                  [0, 0, 1]])]

transforms = [scaleDown]
transform2 = [scaleUp]

for name, size, matrix in transforms:
    
    newImage = Image.new("RGB", size)
    newRaster = newImage.load()


    invMatrix = np.linalg.inv(matrix)

    for x in range(newImage.width):
        for y in range(newImage.height):
            vector = np.array([x, y, 1])
            result = invMatrix @ vector

            xp = int(result[0])
            yp = int(result[1])

            if 0 <= xp < image.width and 0 <= yp < image.height:
                newRaster[x, y] = raster[xp, yp]
                
for name, size, matrix in transform2:
    
    finalImage = Image.new("RGB", size)
    finalRaster = finalImage.load()


    invMatrix = np.linalg.inv(matrix)

    for x in range(finalImage.width):
        for y in range(finalImage.height):
            vector = np.array([x, y, 1])
            result = invMatrix @ vector

            xp = int(result[0])
            yp = int(result[1])

            if 0 <= xp < newImage.width and 0 <= yp < newImage.height:
                finalRaster[x, y] = newRaster[xp, yp]

    finalImage.save(name + ".png")