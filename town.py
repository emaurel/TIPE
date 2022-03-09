from PIL import Image, ImageDraw
import random

from matplotlib.patches import Rectangle

class Point:
    def __init__(self, x, y) :
        self.x = x
        self.y = y


    def deplace(self, dx, dy) :
        self.x += dx
        self.y += dy

    def toString(self) :
        return str((self.x,self.y))


    def __add__(self,point) :

        return Point(self.x + point.x , self.y + point.y)
    
    def __sub__(self,point) :

        return Point(self.x - point.x , self.y - point.y)

    def __mul__(self,point) :
        return Point(self.x * point.x, self.y * point.y)

    def __truediv__(self,point) :
        return Point(self.x / point.x, self.y / point.y)


    def toTuple(self) :
        return (self.x,self.y)

class Town :


    def __init__(self,w,h) :
        self.w = w
        self.h = h
        self.blocks = []
        self.cams = []

    @property
    def size(self) :
        return Point(self.w, self.h)

    @classmethod
    def create(cls,width,height,nCams,nBlocks) : 
        t = Town(width,height)
        for i in range(nCams) :
            x = random.randint(0,t.w)
            y = random.randint(0,t.h)
            t.addCam(Camera(Point(x,y)))
        for i in range(nBlocks) :
            x = random.randint(0,t.w-1)
            y = random.randint(0,t.h-1)
            t.addBlock(Block(Rectangle(Point(x,y),Point(1,1))))
        return t

    @classmethod
    def createPreset(cls, nBlock, ecart = 2) :
        t = Town(10,10)
        for i in range(0,nBlock*ecart,ecart) :
            for j in range(0,nBlock*ecart,ecart) :
                r = Rectangle(Point(i,j),Point(1,1))
                t.addBlock(Block(r))

        center = Point(0,0)
        for block in t.blocks :
            center += block.rect.center
        center *= Point(1/len(t.blocks),1/len(t.blocks))
        print(center.toString())
        dif = (t.size/Point(2,2)) - center
        for block in t.blocks :
            block.rect.translate(dif)
        return t



    def addCam(self,cam) :
        self.cams.append(cam)
    
    def addBlock(self,block) :
        self.blocks.append(block)


    def afficheCam(self) :
        for cam in self.cams :
            cam.affiche()

    def afficheBlock(self) :
        for block in self.blocks :
            block.affiche()
    

    def draw(self, img, ratio) :
        for block in self.blocks :
            block.draw(img, ratio)
"""        for cam in self.cams :
            cam.draw(img)"""
    

class Camera :
    def __init__(self,point) :
        self.position = point
    
    def affiche(self) :
        print("camera :", self.position.toString())
    
    def draw(img) :
        i=1
    

    

class Block :
    def __init__(self,rect) :
        self.rect = rect

    def draw(self,img, ratio = Point(100,100)) :
        
        drw = ImageDraw.Draw(img, 'RGBA')
        drw.polygon(self.rect.scale(ratio).allCorners, fill=(0, 255,0, 255//2))





    
class Rectangle :
    def __init__(self,topLeft,size) :
        self.topLeft = topLeft
        self.size = size

    @property
    def topRight(self) :
        return Point((self.size + self.topLeft).x, self.topLeft.y)
    
    @property
    def bottomLeft(self) :
        return Point(self.topLeft.x, self.size.y + self.topLeft.y)

    @property
    def bottomRight(self) :
        return self.topLeft + self.size

    @property
    def allCorners(self) :
        return (self.topLeft.toTuple(),self.topRight.toTuple(),self.bottomRight.toTuple(),self.bottomLeft.toTuple())


    @property
    def center(self) :
        return self.topLeft + (self.size/Point(2,2))

    def toString(self) :
        return ("Rectangle(" + self.topLeft.toString() + self.bottomRight.toString() + ")")

    def scale(self,point) :
        return Rectangle(self.topLeft * point, self.size * point)

    def translate(self,point) :
        self.topLeft += point

