from town import *
town = Town.create(10,10,5,10)
img = Image.new('RGB',(1000,1000))
fond = Image.new("RGBA",(1000,1000),(255,255,255,255//2))
ratio = Point(img.size[0], img.size[1]) / town.size

town.draw(img, ratio)

townPreset = Town.createPreset(3, 3)
img2 = Image.new('RGB',(1000,1000))

townPreset.draw(img2,ratio)


img3 = Image.new('RGB',(1000,1000))
for i in range(20) :
    triangle = Triangle(Point(random.randint(0,10),random.randint(0,10)),2,45)
    triangle.rotate(random.randint(0,360))
    triangle.draw(img3)

im = Image.composite(img2,img3,fond)
im.show()