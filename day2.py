from PIL import Image

image = Image.open("./butterfly.jpg")
data = image.load()

for x in range(image.width):
    for y in range(image.height):
        pixel = data[x,y]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        if (g < 120):
            k = .33*r + .33*g + .33*b
            k = int(k)
            data[x,y] = (k,k,k)
image.save("./butterfly.png")