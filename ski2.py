from tkinter import *
import random
import os
import time
import math

### constant parameters ##########################
mountainheight = 80   # in metres, approx, normally = 80
refreshrate = 20 # in ms, normally = 20
treedensity = 40 # higher = less trees ;), normally = 40
#################################################

besttime = 0
starttime = time.time()

mainwin = Tk(className=" Ski")

mainwin.geometry("800x680")
# playground
canvas1= Canvas(mainwin,width=800,height=600, bg = "white")
canvas1.place(x=0,y=0)

# status text box frame
canvas2= Canvas(mainwin,width=798,height=78, bg = "grey")
canvas2.place(x=0,y=600)

# Print text (labels) on screen
canvastext= Canvas(mainwin,width=784,height=64, bg = "dark blue")
canvastext.place(x=6,y=607)
font1 = ("Arial",16,"bold")
fontBIG = ("Arial",64,"bold") 
def printscr(mytext,x,y,mycolour):
    canvastext.create_text(x,y,text=mytext, fill=mycolour,font=font1, anchor="sw") 
def printBIG(mytext,x,y,mycolour):
    canvas1.create_text(x,y,text=mytext, fill=mycolour,font=fontBIG, anchor="sw") 

def printscore():
    printscr("Keyboard Controls: a,s,d",70,28,"white")
    printscr("Left (a)      Slow Down (s)      Right (d)",15,58,"white")
    printscr("Time: ",600,24,"white")
    printscr("Best: "+str(besttime)+" s",600,58,"white")

timetext = canvastext.create_text(660,24,text="0ms",fill="white",font=font1,anchor="sw")
printscore()


speed = 1  # mountain is moving up at 1 pixel per 20ms


# player class (template)
class GameObject:
    def __init__(self,filedown="",fileleft="",fileright="",x=0,y=0):
        self.x = x
        self.y = y
        self.theta = 270  # skier is facing down (degrees)
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
    def facedirection(self):
        if player1.theta == 270-45:
            canvas1.itemconfigure(self.sprite,image=self.imageleft)
        elif player1.theta == 270+45:
            canvas1.itemconfigure(self.sprite,image=self.imageright)
        else:  # theta = 270
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

xshift = -200   # move all objects in mountain by a fixed amount            
# mountain ice
mountainice = []

def adddirt(xloc=400,yloc=400):
    icecircle = GameObject("circle.png",x=xloc+xshift,y=yloc)
    icecircle.collisioncirclelist.append((16,0,0))
    #icecircle.showcollisioncircles() # for debugging collisions
    mountainice.extend([icecircle])

# add dirt
for i in range(24):
    for j in range(int(30*mountainheight/50)):
        if random.randint(1,10) == 1:
          adddirt(i*50+20,j*50+500)
             
player1 = GameObject("skier.png","skier2.png","skier3.png",x=400,y=200)
player1.collisioncirclelist.append((10,2,0))
#player1.showcollisioncircles()    # for debugging collisions
        

# create mountain obstacles
mountain = []


def addflag(xloc=400,yloc=400):
    img = GameObject("flag1.png",x=xloc+xshift,y=yloc)
    img.collisioncirclelist.append((11,2,6))
    #img.showcollisioncircles()  # for debugging collisions
    mountain.append(img)

def addtree(xloc=400,yloc=400):
    img = GameObject("tree.png",x=xloc+xshift,y=yloc)
    img.collisioncirclelist.extend([(11,2,10),(6,2,-6)])
    #img.showcollisioncircles()  # for debugging collisions
    mountain.append(img)

def addwalls():
    for j in range(int(30*mountainheight/35)+10):
        addtree(10,j*35+400)  # left
        addtree(1200,j*35+400) # right
    for j in range(35):  
        addtree(j*35,30*(mountainheight+10)+400) # bottom


addwalls()
# add trees and flags
for i in range(40):
    for j in range(mountainheight):
        r = random.randint(1,treedensity)
        if r == 1:
            addflag(i*30+20,j*30+500)
        if r == 2:
            addtree(i*30+20,j*30+500)  
    
def checkcollisioncircles(object1, object2):
    for c1 in object1.collisioncirclelist:
        for c2 in object2.collisioncirclelist:  # c0 = r, c1 = dx, c2 = dy
          if (object1.x+c1[1] - object2.x-c2[1])**2+\
             (object1.y+c1[2] - object2.y-c2[2])**2\
             < (c1[0]+c2[0])**2:
               return True
    return False

def timerupdate():
    global speed
    speed = speed + 0.03
    if speed >= 8: speed = 8
    mdy = speed*math.sin(player1.theta*math.pi/180)  # convert to radians
    mdx = -speed*math.cos(player1.theta*math.pi/180)
    for m in mountain:
        m.move(mdx,mdy)
        if checkcollisioncircles(m,player1):
            print("Circles Crash "+str(speed));
            speed = 1
    for m in mountainice:
        m.move(mdx,mdy)
    mytime = str(time.time()-starttime)[:5]
    canvastext.itemconfigure(timetext, text = mytime+" s")
    mainwin.after(refreshrate,timerupdate)


def mykey(event):
    global theta, speed
    if event.char == "s":
        speed = speed - 2
        if speed <= 1: speed = 1
    if event.char == "d":
        player1.theta = player1.theta + 45 # player rotate left
        if player1.theta > 270+45: player1.theta = 270+45
    if event.char == "a":
        player1.theta = player1.theta - 45 # player rotate right
        if player1.theta < 270-45: player1.theta = 270-45
    player1.facedirection()

mainwin.bind("<Key>", mykey)
timerupdate()
mainwin.mainloop()

