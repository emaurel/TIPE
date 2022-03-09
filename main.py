from town import *
town = Town.create(10,10,5,10)
img = Image.new('RGB',(1000,1000))

ratio = Point(img.size[0], img.size[1]) / town.size

town.draw(img, ratio)
img.save("test.png", 'PNG')

townPreset = Town.createPreset(3, 3)
img2 = Image.new('RGB',(1000,1000))

townPreset.draw(img2,ratio)
img2.save("preset.png",'PNG')