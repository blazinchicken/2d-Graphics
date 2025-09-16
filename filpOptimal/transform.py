from PIL import Image
import numpy as np
import math

originalImage = Image.open("./frog.jpg")
originalRaster = originalImage.load()

w = originalImage.width
h = originalImage.height



matrix = np.array([[1, 0, 0]
                 ,[0, -1, originalImage.height-1]
                 ,[0, 0, 1]])