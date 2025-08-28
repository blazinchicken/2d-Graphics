from PIL import Image

image = Image.open("./lizard.jpg")
data = image.load()

for x in range(image.width):
    for y in range(image.width):
        pixel = data[x,y]


        data[x,y] = pixel
image.save("./lizard.png")