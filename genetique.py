import random
import math
import numpy
from PIL import Image, ImageDraw
Tx = 10
Ty = 10



def genCamera(n) :
    l = []
    while len(l) !=n :
        x = random.randint(1,Tx)
        y = random.randint(1,Ty)
        d = random.randint(0,360)
        c = (x,y,d)
        b = True
        for i in range(len(l)) :
            if l[i][:2] == (x,y) :
                b = False
        if b :
            l.append(c)
    return l

def getAire(a) :
    return (abs(a[0]-a[2]) * abs(a[1]-a[3]))


def genObstacle(n) :
    l = []
    while len(l) !=n :
        x1 = random.randint(0,Tx-1)
        y1 = random.randint(0,Ty-1)
        x2 = random.randint(x1+1,Tx)
        y2 = random.randint(y1+1,Ty)
        if (x1,y1,x2,y2) not in l :
            if getAire((x1,y1,x2,y2)) <= 2 :
                l.append((x1,y1,x2,y2))
    return l

print(genCamera(20))


def genZone(camera, longueur) :
    c1 = (camera[0],camera[1])
    g,d = (camera[2]-(45//2))%360,(camera[2]+(45//2))%360
    mg = (longueur*math.cos((g*math.pi)/180)+c1[0],longueur*math.sin((g*math.pi)/180)+c1[1])
    md = (longueur*math.cos((d*math.pi)/180)+c1[0],longueur*math.sin((d*math.pi)/180)+c1[1])
    return (c1,mg,md)



cameraList = [genZone(i,5) for i in genCamera(10)]
def drawCam(n) :
    ratio = 100
    l = cameraList
    img = Image.new('RGB',(Tx*ratio,Ty*ratio),(0,0,0))
    for i in range(len(l)) :
        a = l[i]
        a1 = (a[0][0]*ratio,a[0][1]*ratio)
        a2 = (a[1][0]*ratio,a[1][1]*ratio)
        a3 = (a[2][0]*ratio,a[2][1]*ratio)
        drw,drw2 = ImageDraw.Draw(img, 'RGBA'),ImageDraw.Draw(img, 'RGBA')
        drw.polygon(xy=[a1, a2, a3], fill=(255, 255,255,255//2))
        drw2.ellipse((a1[0]-10,a1[1]-10,a1[0]+10,a1[1]+10),fill = (255,0,0))
        del drw
        del drw2

    img.save("cam"+".png", 'PNG')

def drawObs(n) :
    ratio = 100
    l = genObstacle(n)
    img = Image.new('RGB',(Tx*ratio,Ty*ratio),(0,0,0))
    for i in range(len(l)) :
        a = l[i]
        a1 = (a[0]*ratio,a[1]*ratio)
        a2 = (a[2]*ratio,a[1]*ratio)
        a3 = (a[2]*ratio,a[3]*ratio)
        a4 = (a[0]*ratio,a[3]*ratio)

        drw = ImageDraw.Draw(img, 'RGBA')
        drw.polygon(xy=[a1, a2, a3,a4], fill=(0, 255,0))
        del drw

    img.save("Obs"+".png", 'PNG')


drawCam(10)

imcam = Image.open("cam.png")
imobs = Image.open("Obs.png")
img = Image.new("RGBA",(Tx*100,Ty*100),(255,255,255,255//2))
im = Image.composite(imcam,imobs,img)



camList = numpy.asarray(imcam)
obsList = numpy.asarray(imobs)
"""for i in range(len(camList)) :
    for j in range(len(camList[0])) :
        if obsList[i][j][1] == 255 :
            camList[i][j] = (0,0,0)
"""



nl = []
for i in cameraList :
    m1 = min(i[0][0],i[1][0],i[2][0])
    m2 = min(i[0][1],i[1][1],i[2][1])
    m3 = max(i[0][0],i[1][0],i[2][0])
    m4 = max(i[0][1],i[1][1],i[2][1])
    nl.append((m1,m2,m3,m4))

for i in range(len(nl)) :
    for j in range(int(nl[i][1]),int(nl[i][3])) :
        for k in range(int(nl[i][0]),int(nl[i][2])) :
            if obsList[k,j][1] != 0 :
                camList[k,j] = (0,0,0)
                if camList[k,j][0] != 0 :
                    camList[k,j] = (0,0,0)


imcam.show()
imcam = Image.fromarray(camList)

im = Image.composite(imcam,imobs,img)
imcam.show()
im.show()