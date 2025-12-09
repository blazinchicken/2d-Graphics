from PIL import Image
import numpy as np
import math
"""
what am i doing here

GOAL: make multiple blur functions that change the image by a bit at a time, allowing for multiple functions to be added to the GUI

1. jitter blur
    - I was thinking that this could just be a simple randomization between the axis of a pixel, in that it would pull the color 
    values from the pixels surrounding each pixel, and then randomly choose one of the options to then go through and fill for that pixel,
    this would be extremely expensive in terms of time but would work.

2. interpolation
    - This one seems a little faster in that 
"""
image = Image.open("./wave.jpg")
raster = image.load()