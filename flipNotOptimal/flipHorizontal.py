from PIL import Image
originalImage = Image.open("./butterfly.jpg")
originalRaster = originalImage.load()
finalImage = Image.new("RGB", (originalImage.width, originalImage.height))
finalRaster = finalImage.load()

for x in range(originalImage.width):
    for y in range(originalImage.height):
        pixel = originalRaster[x,y]

        xp = originalImage.width - 1 - x
        yp = y

        finalRaster[xp, yp] = pixel

finalImage.save("./horizontal_flip_butterfly.png")