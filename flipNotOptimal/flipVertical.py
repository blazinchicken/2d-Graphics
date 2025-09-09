from PIL import Image

originalImage = Image.open("./butterfly.jpg")
originalRaster = originalImage.load()
finalImage = Image.new("RGB", (originalImage.width, originalImage.height))
finalRaster = finalImage.load()

for x in range(originalImage.width):
    for y in range(originalImage.height):
        pixel = originalRaster[x,y]
        
        xp = x
        yp = originalImage.height - 1 - y
        
        finalRaster[xp,yp] = pixel

finalImage.save("./vertical_flip_butterfly.png")