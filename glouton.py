from pydraw import *
import random
Ux = 100
Uy = 100
def createSet(nb) :
    SE = []
    while len(SE) < nb :
        xd = random.randint(0,Ux-1)
        x1=xd+1
        yd = random.randint(0,Uy-1)
        y1=yd+1
        xf = random.randint(x1,Ux)
        yf = random.randint(y1,Uy)
        SE.append([(xd,yd),(xf,yf)])
    return SE

def cover(l, seul = False):
    if seul :
        return (l[1][0]-l[0][0]) * (l[1][1]-l[0][1])
    else :
        return [(i[1][0]-i[0][0])*(i[1][1]-i[0][1]) for i in l]

def intersect(a,b) :
    l = []
    if a[0][0] <= b[0][0] <= a[1][0] :
        if a[0][1] <= b[0][1] <= a[1][1] :
            l = [(b[0][0],b[0][1]),(min(b[1][0],a[1][0]),min(b[1][1],a[1][1]))]

        elif b[0][1] < a[0][1] :
            if b[1][1] >= a[0][1] :
                l=[(b[0][0],a[0][1]),(min(a[1][0],b[1][0]),min(a[1][1],b[1][1]))]

    elif b[0][0] < a[0][0] :
        if b[1][0] >= a[0][0] and b[0][1] <= a[1][1] and b[1][1] >= a[0][1]:
            l=[(a[0][0],max(a[0][1],b[0][1])),(min(a[1][0],b[1][0]),min(a[1][1],b[1][1]))]

    return l

def pointIn(p, a) :
    if a[0][0] <= p[0] <= a[1][0] and a[0][1]<= p[1] <= a[1][1] :
        return True
    return False


def InUnion(a,l) :
    a1 = a[0]
    a2 = (a[1][0],a[0][1])
    a3 = a[1]
    a4 = (a[0][0],a[1][1])
    c1,c2,c3,c4 = False,False,False,False
    for i in range(len(l)) :
        if pointIn(a1,l[i]):
            c1 = True
        if pointIn(a2,l[i]) :
            c2 = True
        if pointIn(a3,l[i]) :
            c3 = True
        if pointIn(a4,l[i]) :
            c4 = True
    if c1 and c2 and c3 and c4 :
        return True
    return False

def newCover(a,b) :
    cf = intersect(a,b)
    if cf != [] :
        return cover(b,True) - cover(cf,True)
    else :
        return(cover(b,True))

def bestCover(total,lf) :
    ls = total
    lcb = []
    for h in range(len(ls)) :
        k = True
        lc = [newCover(lf[m],ls[h]) for m in range(len(lf))]
        if InUnion(ls[h],lf) :
            sc = 0
            k = False
        if 0 in lc :
            sc = 0
            k = False
        if k:
            sc = sum(lc)
        lcb.append(sc)
    return total[lcb.index(max(lcb))]


def maxGlouton(k,lSet) :
    coverage = cover(lSet)
    ls = lSet
    m = ls[coverage.index(max(coverage))]
    lf = [m]
    ls.remove(m)
    for i in range(k-1):
        b = bestCover(ls,lf)
        lf.append(b)
        ls.remove(b)
    return lf


"""
def draw(rate, rs) :
    kx = Ux
    ky=Uy
    turtle.up()
    turtle.fillcolor("blue")
    turtle.begin_fill()
    turtle.goto(-Ux*rate,-Uy*rate)
    turtle.down()
    turtle.goto(Ux*rate,-Uy*rate)
    turtle.goto(Ux*rate,Uy*rate)
    turtle.goto(-Ux*rate,Uy*rate)
    turtle.goto(-Ux*rate,-Uy*rate)
    turtle.end_fill()
    for i in range(len(rs)) :
        turtle.up()
        turtle.fillcolor("red")

        turtle.begin_fill()
        turtle.goto((rs[i][0][0]-kx)*rate,(rs[i][0][1]-ky)*rate)
        turtle.down()
        turtle.goto((rs[i][1][0])*rate,(rs[i][0][1]-ky)*rate)
        turtle.goto(rs[i][1][0]*rate,rs[i][1][1]*rate)
        turtle.goto((rs[i][0][0]-kx)*rate,rs[i][1][1]*rate)
        turtle.goto((rs[i][0][0]-kx)*rate,(rs[i][0][1]-ky)*rate)
        turtle.end_fill()
    turtle.done()
"""
from PIL import Image, ImageDraw

def pourcentage(rs) :
    p = 0
    for x in range(Ux) :
        for y in range(Uy) :
            for i in range(len(rs)) :
                if pointIn((x,y),rs[i]) :
                    p+=1
                    break
    return (p/(Ux*Uy))*100



def draw(rs,ratio,name,retour = False) :

    img = Image.new('RGB', (Ux*ratio, Uy*ratio))
    for i in range(len(rs)) :
        a = rs[i]
        a1 = (a[0][0]*ratio,a[0][1]*ratio)
        a2 = (a[1][0]*ratio,a[0][1]*ratio)
        a3 = (a[1][0]*ratio,a[1][1]*ratio)
        a4 = (a[0][0]*ratio,a[1][1]*ratio)
        drw = ImageDraw.Draw(img, 'RGBA')
        drw.polygon(xy=[a1, a2, a3,a4], fill=(255, 0, 0, 700//(len(rs))))
        del drw
    if retour :
        return img
    else :
        img.save(name+".png", 'PNG')




im = Image.new('RGB', (Ux*10, Uy*10))
ls = []
lp = []
for j in range(1,6) :
    for i in range(10) :
        result = maxGlouton(10,createSet(10*j))
        ls.append((draw(result,10,"d",True),pourcentage(result)))
ls.sort(key = lambda x:x[1])
lt = [i[0] for i in ls]
print(lt)

im.save('out2.gif', save_all=True, append_images=lt,loop = 0,duration = 100)

"""for j in range(1,51) :
    for i in range(50) :
        result = maxGlouton(10,createSet(10*j))
        draw(result,10,"pour " +str(10*j) + " valeurs " + str(pourcentage(result))[:5] + " pourcents")
        #draw(result,10,"test_opaque-"+str(i), False)

with open("info.txt", "w") as filout :
    l = []
    for j in range(1,51) :
        pl = []
        for i in range(50) :
            result = maxGlouton(10,createSet(10*j))
            pr = pourcentage(result)
            filout.write(str(j*10) +" " + str(pr))
            filout.write("\n")
            print(pourcentage(result))
            pl.append(pr)
        l.append(10*j)
        l.append(pl)

txt2 = open("moyenne.txt","w")
for i in range(len(l)) :
    if i%2 == 0 :
        txt2.write(str(l[i]) + " ")
    else :
        txt2.write(str(sum(l[i])/len(l[i]))+ "\n")
"""