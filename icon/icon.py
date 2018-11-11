'''
Render a PNG image to be used as an icon with a couple of black lines:

---------
-----
--
--
-----
---------
'''

from PIL import Image, ImageDraw


def lines(dim):
    img = Image.new("RGB", (dim, dim), "#AAAAAA")
    draw = ImageDraw.Draw(img)

    N_lines = 6
    Distance = dim/(N_lines+1)
    lengths = [1.0, 0.75, 0.5, 0.5, 0.75, 1.0]

    for i in range(N_lines):
        x0 = int(dim*.05)
        x1 = int(dim*.95*lengths[i])
        y0 = int((i+1)*Distance)
        xy = (x0, y0, x1, y0)
        draw.line(xy, fill=(0, 0, 0), width=9)

    return img


dim = 256
img = lines(dim)
img.save('list.png')
