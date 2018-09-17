from PIL import Image
from numpy import * 
import qrtools

class Cuadradito(object):
    '''
        ul: Up Left (r,g,b)
        ur: Up Right (r,g,b)
        dl: Donw Left (r,g,b)
        dr: Down Right (r,g,b)
    '''
    def __init__(self, ul, ur, dl, dr, image):
        self.ul = ul 
        self.ur = ur
        self.dl = dl
        self.dr = dr
        self.image = image
        self.x_position = 0
        self.y_position = 0

    def isUpperCornerLeft(self):
        if ((isWhite(self.ul) or isBlack(self.ul)) and (isWhite(self.ur) or isBlack(self.ur)) and (isWhite(self.dl) or isBlack(self.dl))):
            return True
        return False

    def isUpperCornerRight(self):
        if ((isWhite(self.ul) or isBlack(self.ul)) and (isWhite(self.ur) or isBlack(self.ur)) and (isWhite(self.dr) or isBlack(self.dr))):
            return True
        return False

    def isLowerCornerLeft(self):
        if ((isWhite(self.ul) or isBlack(self.ul)) and (isWhite(self.dr) or isBlack(self.dr)) and (isWhite(self.dl) or isBlack(self.dl))):
            return True
        return False

    def isLowerCornerRight(self):
        if ((isWhite(self.dr) or isBlack(self.dr)) and (isWhite(self.ur) or isBlack(self.ur)) and (isWhite(self.dl) or isBlack(self.dl))):
            return True
        return False

    def isLeftSide(self):
        if ((isWhite(self.ul) or isBlack(self.ul)) and (isWhite(self.dl) or isBlack(self.dl))):
            return True
        return False
    def isUpperSide(self):
        if ((isWhite(self.ul) or isBlack(self.ul)) and (isWhite(self.ur) or isBlack(self.ur))):
            return True
        return False
    def isDownSide(self):
        if ((isWhite(self.dl) or isBlack(self.dl)) and (isWhite(self.dr) or isBlack(self.dr))):
            return True
        return False
    def isRightSide(self):
        if ((isWhite(self.dr) or isBlack(self.dr)) and (isWhite(self.ur) or isBlack(self.ur))):
            return True
        return False

def isBlack(a):
    if (a[0] == 0) and (a[1] == 0) and (a[2] == 0):
        return True

def isWhite(a):
      if (a[0] == 255) and (a[1] == 255) and (a[2] == 255):
        return True  



def crop(input, height, width):
    list = []
    im = Image.open(input)
    imgwidth, imgheight = im.size


    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j + 1, i + 1, j+width, i+height)
            list.append(im.crop(box))
    return list

list = crop("challenge.png", 50, 50)
cuadradito_list = []
for x in list:
    ul = x.getpixel((5,5))
    ur = x.getpixel((43,5))
    dl = x.getpixel((5,43))
    dr = x.getpixel((43,43))
    cuadradito = Cuadradito(ul, ur, dl, dr, x)
    if (cuadradito.isUpperCornerLeft()):
        cul = cuadradito
    cuadradito_list.append(cuadradito)

qr = qrtools.QR()

def show(l):
    new_im = Image.new('RGB', (980, 980))
    x_offset = 0
    y_offset = 0

    for col in l:
        for e in col:
            new_im.paste(e.image, (x_offset,y_offset))
            y_offset += e.image.size[1]
        y_offset = 0
        x_offset += 49
    new_im.save('out_.png')
    qr.decode('out_.png')
    if qr.data != "NULL":
        print(qr.data)
    


def completeNextRow(cuadraditos_left, nw):

    if len(cuadraditos_left) == 0:
        show(nw)
        return

    if len(nw[len(nw)-1]) == 20:
        left = cuadraditos_left[:]
        nwnwl = [x[:] for x in nw]
        nwnwl.append([])
        completeNextRow(left, nwnwl)
        return


    left_cuadradito = nw[len(nw)-2][len(nw[len(nw)-1])]
    for c in cuadraditos_left:
        if len(nw[len(nw)-1]) == 0:
            if (left_cuadradito.dr == c.dl) and c.isUpperSide():
                left = cuadraditos_left[:]
                left.remove(c)
                nwnwl = [x[:] for x in nw]
                nwnwl[len(nwnwl)-1].append(c)
                completeNextRow(left, nwnwl)
                continue
            continue

        up_cuadradito = nw[len(nw)-1][len(nw[len(nw)-1])-1]
        if (left_cuadradito.dr == c.dl) and (left_cuadradito.ur == c.ul) and (up_cuadradito.dl == c.ul) and (up_cuadradito.dr == c.ur) :
            left = cuadraditos_left[:]
            left.remove(c)
            nwnwl = [x[:] for x in nw]
            nwnwl[len(nwnwl)-1].append(c)
            completeNextRow(left, nwnwl)

        if (c.isDownSide() and (left_cuadradito.ur == c.ul) and (up_cuadradito.dl == c.ul) and (up_cuadradito.dr == c.ur)) :
            left = cuadraditos_left[:]
            left.remove(c)
            nwnwl = [x[:] for x in nw]
            nwnwl[len(nwnwl)-1].append(c)
            completeNextRow(left, nwnwl)

        if (c.isRightSide() and (left_cuadradito.ur == c.ul) and (up_cuadradito.dl == c.ul)) :
            left = cuadraditos_left[:]
            left.remove(c)
            nwnwl = [x[:] for x in nw]
            nwnwl[len(nwnwl)-1].append(c)
            completeNextRow(left, nwnwl)

    return

def completeRow(l, cuadraditos_left):

    if len(l) == 20:
        if l[len(l)-1].isLowerCornerLeft(): 
            completeNextRow(cuadraditos_left, [l, []])
        return

    for c in cuadraditos_left:
        if (l[len(l)-1].dr == c.ur and c.isLeftSide()):
            newl = l[:]
            left = cuadraditos_left[:]
            newl.append(c)
            left.remove(c)
            completeRow(newl, left)
    return

completeRow([cul], cuadradito_list)
