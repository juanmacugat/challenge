import sys
import random
from PIL import Image

img = Image.open('challenge.png')
pix = img.load()
width, height = img.size

BLOCKLEN = 50
i = 0
Colors = set()
Borders = set()
Corners = set()

Color = {}

width, height = img.size
# Imprimo el tamano de la imagen
print("Tamano de imagen:", width, height)

xblock = width // BLOCKLEN
yblock = height // BLOCKLEN
# Imprimo cantidad de filas y columnas
print("Tamano de bloques:", xblock, yblock)

blockmap = [(xb * BLOCKLEN, yb * BLOCKLEN, (xb + 1) * BLOCKLEN, (yb + 1) * BLOCKLEN)
            for xb in range(xblock) for yb in range(yblock)]
# Imprimo cantidad de bloques
print("Cantidad de bloques:", len(blockmap))

with open('data.txt', 'w') as f:
    for item in blockmap:
        i += 1
        x, y, w, z = item
        c1 = pix[x + 5, y + 5]
        Color = {'color': c1, 'index': 1}
        if c1 not in Colors:
            Colors.add(c1)

        c2 = pix[w - 5, y + 5]
        if c2 not in Colors:
            Colors.add(c2)
            Color[str(c2)] = Color[str(c2)] + 1
        c3 = pix[x + 5, z - 5]
        if c3 not in Colors:
            Colors.add(c3)
            Color[str(c3)] = Color[str(c3)] + 1
        c4 = pix[w - 5, z - 5]
        if c4 not in Colors:
            Colors.add(c4)
            Color[str(c3)] = Color[str(c3)] + 1

        f.write("Bloque # %s\n" % i)
        f.write("Color cuadrante #1: %s\n" % str(c1))
        f.write("Color cuadrante #2: %s\n" % str(c2))
        f.write("Color cuadrante #3: %s\n" % str(c3))
        f.write("Color cuadrante #4: %s\n" % str(c4))

print("Cantidad de colores distintos:",len(Colors))
print("Bloques borde:",Borders)
print("Cantidad de bloques borde:", len(Borders))
print("Corners: ", Corners)
print("Colors:" + Color)

shuffle = list(blockmap)
random.shuffle(shuffle)

result = Image.new(img.mode, (width, height))
for box, sbox in zip(blockmap, shuffle):
    c = img.crop(sbox)
    result.paste(c, box)
result.save('result.png')

# pix_val = list(img.getdata())
# pix_val_flat = [x for sets in pix_val for x in sets]
#
# with open('data.txt', 'w') as f:
#    for item in pix_val_flat:
#        f.write("%s" % item)