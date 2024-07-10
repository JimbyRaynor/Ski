from tkinter import *
import random
import os
import time

mainwin = Tk(className=" Ski")

mainwin.geometry("800x680")
# playground
canvas1= Canvas(mainwin,width=800,height=600, bg = "white")
canvas1.place(x=0,y=0)

# player class (template)
class GameObject:
    def __init__(self,filedown="",fileleft="",fileright="",x=0,y=0):
        self.x = x
        self.y = y
        self.collisioncirclelist = []
        self.collisioncircleimages = []
        self.collisioncircleshow = False
        self.image = PhotoImage(file=filedown).zoom(2,2)
        self.sprite = canvas1.create_image(2,2,image=self.image)
        if fileleft != "":
           self.imageleft = PhotoImage(file=fileleft)
        if fileright != "":
           self.imageright = PhotoImage(file=fileright)
        canvas1.move(self.sprite,x,y)
    def move(self,dx=0,dy=0):
        self.x = self.x + dx
        self.y = self.y + dy
        canvas1.move(self.sprite,dx,dy)
        if self.collisioncircleshow:
            for circle in self.collisioncircleimages:
                canvas1.delete(circle)
            self.showcollisioncircles()      
    def faceleft(self):
        canvas1.itemconfigure(self.sprite,image=self.imageleft)
    def faceright(self):
        canvas1.itemconfigure(self.sprite,image=self.imageright)
    def facedown(self):
        canvas1.itemconfigure(self.sprite,image=self.image)
    def showcollisioncircles(self):
        self.collisioncircleshow = True
        self.collisioncircleimages.clear()
        for c in self.collisioncirclelist:  # c0 = r, c1 = dx, c2 = dy
            myimage = canvas1.create_oval(self.x-c[0]+c[1],\
                                      self.y-c[0]+c[2],\
                                      self.x+c[0]+c[1],\
                                      self.y+c[0]+c[2])
            self.collisioncircleimages.append(myimage)
            
# mountain ice
mountainice = []
for i in range(100):
    ice1 = GameObject("ice.png",\
            x=random.randint(1,800),y=400+random.randint(1,2000))
    mountainice.append(ice1)


def adddirt(xloc=400,yloc=400):
    icecircle = GameObject("circle.png",x=xloc,y=yloc)
    icecircle.collisioncirclelist.append((16,0,0))
    icecircle.showcollisioncircles()
    mountainice.extend([icecircle])


for i in range(100):
    adddirt(xloc=random.randint(1,800),yloc=400+random.randint(1,2000))
             
player1 = GameObject("skier.png","skier2.png","skier3.png",x=390,y=200)
player1.collisioncirclelist.append((10,2,0))
player1.showcollisioncircles()    # for debugging collisions
        

# create mountain obstacles
mountain = []
mdx = 0 # move mountain amount
mdy = -2
for i in range(100):
    flag1 = GameObject("flag1.png",\
            x=random.randint(1,800),y=400+random.randint(1,2000))
    flag1.collisioncirclelist.append((11,2,6))
    mountain.append(flag1) 
    flag1.showcollisioncircles() # for debugging collisions

for i in range(30):
    tree1 = GameObject("tree.png",\
            x=random.randint(1,800),y=400+random.randint(1,2000))
    tree1.collisioncirclelist.extend([(11,2,10),(6,2,-10)])
    tree1.showcollisioncircles() # for debugging collisions
    mountain.append(tree1)
    
def checkcollisioncircles(object1, object2):
    for c1 in object1.collisioncirclelist:
        for c2 in object2.collisioncirclelist:  # c0 = r, c1 = dx, c2 = dy
          if (object1.x+c1[1] - object2.x-c2[1])**2+\
             (object1.y+c1[2] - object2.y-c2[2])**2\
             < (c1[0]+c2[0])**2:
               return True
    return False
    
def timerupdate():
    for m in mountain:
        m.move(mdx,mdy)
        if checkcollisioncircles(m,player1):
            print("Circles Crash ;)");
    for m in mountainice:
        m.move(mdx,mdy)    
    mainwin.after(50,timerupdate)

def mykey(event):
    global mdx, mdy
    if event.char == "w":
        mdx = 0
        mdy = 0
        player1.facedown()
    if event.char == "d":
        mdx = -2
        mdy = -2
        player1.faceright()
    if event.char == "a":
        mdx = 2
        mdy = -2
        player1.faceleft()
    if event.char == "s":
        mdx = 0
        mdy = -4
        player1.facedown()

mainwin.bind("<Key>", mykey)
mainwin.after(100,timerupdate)
mainwin.mainloop()

