from PIL import Image
import numpy as np
import math
import random

image = Image.open('./frog.jpg')
raster = image.load()
'''
ok so how do we go about doing this....

goal:
import an image - > have image processed to find the most common colors and find the average color to fill all those pixels
take said palette and multiply it so that the colors change, so the image is still readable but has a different base color
take image and divide it to be half the size it initial was, then write the new image with new palettes into each of y + image.height/2...
should be andy warhol image
'''
#scaledown  -  200x200/2 = 100x100, with 100 + 100 = 200
scaleDownFactor = .5
w = image.width
h = image.height

def l1_difference(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))

def closest_color(color, color_list):
    return min(color_list, key=lambda option: l1_difference(color, option))

def random_color():
    return tuple(random.randint(0,255) for _ in range(3))

scaleDown = ["scaleDown", (int(w * scaleDownFactor), int(h * scaleDownFactor)), np.array([[scaleDownFactor, 0, 0],
                                                                                          [0, scaleDownFactor, 0],
                                                                                          [0,               0, 1]])]

transforms = [scaleDown]

for name, size, matrix in transforms:
    openImage = Image.new("RGB", size)
    openRaster = openImage.load()


    invMatrix = np.linalg.inv(matrix)

    for y in range(openImage.height):
        for x in range(openImage.width):
            vector = np.array([x, y, 1])
            result = invMatrix @ vector

            xp = int(result[0])
            yp = int(result[1])

            if 0 <= xp < image.width and 0 <= yp < image.height:
                openRaster[x, y] = raster[xp, yp]


#kmeans pixel sampling

k = 20
iterations = 5
color_count = dict()

for y in range(openImage.height):
    for x in range(openImage.width):
        pixel = raster[x,y]
        if pixel not in color_count:
            color_count[pixel] = 0
        color_count[pixel] += 1

sorted_color_count = sorted(color_count.items(), key=lambda item:item[1], reverse=True)

palette = [random_color() for _ in range(k)]
for i in range(iterations):
    print(palette)
    close_color_list = [[] for _ in range(k)]

    for color_count in sorted_color_count:
        closest_palette_color = closest_color(color_count[0], palette)
        closest_index = palette.index(closest_palette_color)
        close_color_list[closest_index].append(color_count)
        
    for j in range(k):
        close_list = close_color_list[j]
        if len(close_list) == 0:
            palette[j] = random_color()
        else:
            sums = [0,0,0]
            sum_weight = 0
            for color, count in close_list:
                sums = [a+b*count for a,b in zip(sums, color)]
                sum_weight +=count
            palette[j] = tuple(a//sum_weight for a in sums)

finalImage = Image.new("RGB", (w,h))
finalRaster = finalImage.load()

for y in range(openImage.height):
    for x in range(openImage.width):
        pixel = openRaster[x,y]
        
        
        #want to make this more iterable, interactible and size to be defined by the user
        finalRaster[x, y] = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
        finalRaster[x+openImage.width, y] =  closest_color(pixel, palette) #(int(pixel[0]),int(pixel[1]),int(pixel[2]))
        finalRaster[x, y+openImage.height] = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
        finalRaster[x+openImage.width, y+openImage.height] = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
finalImage.save('./andyWarhol.png')