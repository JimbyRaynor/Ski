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
    def __init__(self,filedown="",fileleft="",fileright="",x=0,y=0,cr=0,cdx=0,cdy=0):
        self.x = x
        self.y = y
        self.cr = cr # collision circle radius
        self.cdx = cdx # collision circle x-offset
        self.cdy = cdy # collision circle y-offset
        self.collisioncircleimage = None
        self.collisioncircle = False
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
        if self.collisioncircle:
            canvas1.delete(self.collisioncircleimage) # delete old collision circle
            self.showcollisioncircle()
    def faceleft(self):
        canvas1.itemconfigure(self.sprite,image=self.imageleft)
    def faceright(self):
        canvas1.itemconfigure(self.sprite,image=self.imageright)
    def facedown(self):
        canvas1.itemconfigure(self.sprite,image=self.image)
    def showcollisioncircle(self):
        self.collisioncircle = True
        self.collisioncircleimage = canvas1.create_oval(self.x-self.cr+self.cdx,\
                                      self.y-self.cr+self.cdy,\
                                      self.x+self.cr+self.cdx,\
                                      self.y+self.cr+self.cdy)

# mountain ice
mountainice = []
for i in range(100):
    ice1 = GameObject("ice.png",\
            x=random.randint(1,800),y=400+random.randint(1,2000),cr=0,cdx=0,cdy=0)
    mountainice.append(ice1)


def adddirt(xloc=400,yloc=400):
    icecircle1 = GameObject("circletl.png",x=xloc,y=yloc,cr=10,cdx=6,cdy=4)
    icecircle1.showcollisioncircle()
    icecircle2 = GameObject("circletr.png",x=xloc+32,y=yloc,cr=10,cdx=-6,cdy=4)
    icecircle2.showcollisioncircle()
    icecircle3 = GameObject("circlebl.png",x=xloc,y=yloc+32,cr=10,cdx=6,cdy=-4)
    icecircle3.showcollisioncircle()
    icecircle4 = GameObject("circlebr.png",x=xloc+32,y=yloc+32,cr=10,cdx=-6,cdy=-4)
    icecircle4.showcollisioncircle()
    mountainice.extend([icecircle1,icecircle2,icecircle3,icecircle4])


for i in range(100):
    adddirt(xloc=random.randint(1,800),yloc=400+random.randint(1,2000))
             
player1 = GameObject("skier.png","skier2.png","skier3.png",x=390,y=200,cr=10,cdx=2,cdy=0)
player1.showcollisioncircle()  # for debugging collisions
        

# create mountain obstacles
mountain = []
mdx = 0 # move mountain amount
mdy = -2
for i in range(100):
    flag1 = GameObject("flag1.png",\
            x=random.randint(1,800),y=400+random.randint(1,2000),cr=11,cdx=2,cdy=6)
    mountain.append(flag1)
    flag1.showcollisioncircle()  # for debugging collisions

for i in range(30):
    tree1 = GameObject("tree.png",\
            x=random.randint(1,800),y=400+random.randint(1,2000),cr=11,cdx=2,cdy=10)
    tree1.showcollisioncircle()
    mountain.append(tree1)
    
def checkcollision(object1, object2):
    if (object1.x+object1.cdx - object2.x-object2.cdx)**2+\
       (object1.y+object1.cdy - object2.y-object2.cdy)**2\
       < (object1.cr+object2.cr)**2:
       return True
    else:
       return False
    
def timerupdate():
    for m in mountain:
        m.move(mdx,mdy)
        if checkcollision(m,player1):
            print("You Crashed")
            #exit()
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

