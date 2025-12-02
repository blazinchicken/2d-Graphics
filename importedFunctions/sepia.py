'''
initial thoughts:

2 methods:

1. hsv - sepia
    -using a static sepia brown hue
    -changing value will change brightness of this brown, effectively spanning the value spectrum
    -saturation of the brown is core to the color, so this will stay static aswell
    
2. rgb - sepia matrix
    -mentioned by ricks as "the way" to do it
    -look into matrix, cite whoever i get it from
'''
from PIL import Image

image = Image.open("./frog.jpg")
raster = image.load()

def rgb_to_hsv(r, g, b):
    _max = max(r, g, b)
    _min = min(r, g, b)
    _diff = _max-_min

    v = _max
    if v == 0:
        return 0, 0, 0
    
    s = (_max-_min)/_max
    if s == 0:
        return 0, s, v
    
    if r == _max:
        h = (360 + ((g-b)*60/_diff))%360
    elif g == _max:
        h = 120 + ((b-r)*60/_diff)
    elif b == _max:
        h = 240 + ((r-g)*60/_diff)
    
    h = 24
    s = s/2
    return h, s, v

def hsv_to_rgb(h, s, v):
    _max = v
    _min = _max - s*_max

    f = (_max-_min)/60


    if h < 60: return (_max, ((h-0)*f+_min), _min)
    if h < 120: return ((_min-(h-120)*f), _max, _min)
    if h < 180: return (_min, _max, (_min-(h-120)*f))
    if h < 240: return (_min, (_min-(h-240)*f), _max)
    if h < 300: return (((h-240)*f+_min), _min, _max)
    if h < 360: return (_max, _min, (_min-(h-360)*f))
    
def jank_sepia(r, g, b):
    
    h, s, v = rgb_to_hsv(r, g, b)
    r, g, b = hsv_to_rgb(h, s, v)

    return r, g, b

    
for x in range(image.width):
    for y in range(image.height):
        r, g, b, *_ = raster[x,y]


        #algorithm found https://www.geeksforgeeks.org/java/image-processing-in-java-colored-image-to-sepia-image-conversion
        newRed = 0.393*r + 0.769*g + 0.189*b
        newGreen = 0.349*r + 0.686*g + 0.168*b
        newBlue = 0.272*r + 0.534*g + 0.131*b
        
        raster[x,y] = (int(newRed), int(newGreen), int(newBlue))

image.save("./sepia.png")