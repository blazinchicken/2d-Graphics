from PIL import Image
import numpy as np
import math


image = Image.open('./frog.jpg')
raster = image.load()

print(f"The Image is of Size {image.width} by {image.height}. That's {(image.width*image.height)} Pixels")

size = image.width * image.height
print(f"That's {(size*4):,} Bytes")

all_colors = dict()

for x in range(image.width):
    for y in range(image.height):
        pixel = raster[x,y]
        
        if pixel not in all_colors:
            all_colors[pixel] = 0
        all_colors[pixel] += 1
        
        
print(f"this image has {len(all_colors):,} unique pixels.")

bits = math.log2(len(all_colors))

print(f"It would take {bits} bits to store the colors as a palette")
#save format
def to_save(image):
    string = "CAT\n"
    string += f"{image.width}\n"
    string += f"{image.height}\n"
    string += "255/n"
    string += ""
    
    raster = image.load()
    
    zero_pad_size = 0
    delimiter_size = 0
    
    for x in range(image.width):
        for y in range(image.height):
            zero_pad_size += math.ceil(math.log10(image.width*image.height))
            
            pixel = raster[x,y]
            i = image.width*y + x
            
            if pixel not in all_colors:
                all_colors[pixel] = []
            all_colors[pixel].append(i)
            
    for pixel in all_colors:
        indices = all_colors[pixel]
        
        string += f"{str(pixel[0]).zfill(3)}{str(pixel[1]).zfill(3)}{str(pixel[2]).zfill(3)}\n"
                
    return string

#read from format
def from_save(string):
    pass #new image

print(to_save(image))