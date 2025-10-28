from PIL import Image
import numpy as np
import math

image = Image.open('./frog.jpg')
raster = image.load()

string = "P6\n"
string += f"{image.width}\n"
string += f"{image.height}\n"
string += "256\n"

for y in range(image.height):
    for x in range(image.width):
        pixel = raster [x,y]
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        
        string += r.to_bytes().encode("latin-1")
        string += g.to_bytes().encode("latin-1")
        string += b.to_bytes().encode("latin-1")
    string += "\n"
    
with open("out.pppm", "w") as f:
    f.write(string)
    
lines = string.split("\n")
assert lines[0] == "P6"
width = int(lines[1])
height = int(lines[2])
_ = int(lines[3])
raster_lines = lines[4:]

ppm_image = Image.new("RGB", (width, height))
ppm_raster = ppm_image.load()

for y in range(height):
    line = raster_lines[y]
    rgb_triples = line.split()
    for x in range(width):
        index = x*3
        r = int(rgb_triples[index+0])
        g = int(rgb_triples[index+1])
        b = int(rgb_triples[index+2])
        ppm_raster[x,y] = (r, g, b)
        
image.save("ppm.png")        