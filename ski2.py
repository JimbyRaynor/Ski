from tkinter import *
import random
import time
import math

## score, not time
## levels: increase length of skifield


### constant parameters ##########################
mountainheight = 40   # in metres, approx, normally = 80
refreshrate = 20 # in ms, normally = 20
treedensity = 40 # higher = less trees and fences ;), normally = 40
#################################################

score = 0
highscore = 0
level = 1

speed = 1  # mountain is moving up at 1 pixel per 20ms
player1alive = True

mainwin = Tk(className=" Ski")

mainwin.geometry("800x680")
# playground
canvas1= Canvas(mainwin,width=800,height=600, bg = "white")
canvas1.place(x=0,y=0)

# Print text (labels) on screen
canvastext= Canvas(mainwin,width=784,height=64, bg = "dark blue")
canvastext.place(x=6,y=607)
font1 = ("Arial",16,"bold")
fontMED = ("Arial",20,"bold")
fontBIG = ("Arial",80,"bold")
def printscr(mytext,x,y):
    canvastext.create_text(x,y,text=mytext, fill="white",font=font1, anchor="sw") 
def printMED(mytext,x,y):
    canvas1.create_text(x,y,text=mytext, fill="black",font=fontMED)
def printBIG(mytext,x,y):
    canvas1.create_text(x,y,text=mytext, fill="red",font=fontBIG) 



def printscore():
    printscr("Aim for finish line at base of mountain",100,30)
    printscr("Keyboard Controls: a (left), d (right)",100,60)
    printscr("Score: ",600,30)
    printscr("Hi-Score: ",600,58)

scoretext = canvastext.create_text(670,30,text="",fill="white",font=font1,anchor="sw")
besttimetext = canvastext.create_text(700,58,text="",fill="white",font=font1,anchor="sw")
printscore()

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
finishline = GameObject("FinishLine.png",x=400,y=30*(mountainheight+6)+400)
mountainice.append(finishline)

def addelement(mylist,filename, xloc= 400, yloc = 400):
    img = GameObject(filename,x=xloc+xshift,y=yloc)
    if filename == "flag1.png":
        img.collisioncirclelist.append((11,2,6))
    if filename == "tree.png":
        img.collisioncirclelist.extend([(11,2,10),(6,2,-6)])
    #img.showcollisioncircles()  # for debugging collisions
    mylist.append(img)
             
player1 = GameObject("skier.png","skier2.png","skier3.png",x=400,y=200)
player1.collisioncirclelist.append((7,2,0))
#player1.showcollisioncircles()    # for debugging collisions
        
# create mountain obstacles
mountain = []

def addwalls():
    for j in range(int(30*mountainheight/35)+10):
        addelement(mountain,"tree.png",10,j*35+400)  # left
        addelement(mountain,"tree.png",1200,j*35+400) # right
    for j in range(35):  
        addelement(mountain,"tree.png",j*35,30*(mountainheight+10)+400) # bottom
    for i in range(mountainheight):
        addelement(mountain,"tree.png",500+random.randint(1,10)*35,30*i+400)

addwalls()
# add trees and flags to mountain

def addobstacles():
  for i in range(40):
    for j in range(mountainheight):
        r = random.randint(1,treedensity)
        if r == 1:
            addelement(mountain,"flag1.png",i*30+20,j*30+500)
        if r == 2:
            addelement(mountain,"tree.png",i*30+20,j*30+500)  

addobstacles()

def checkcollisioncircles(object1, object2):
    for c1 in object1.collisioncirclelist:
        for c2 in object2.collisioncirclelist:  # c0 = r, c1 = dx, c2 = dy
          if (object1.x+c1[1] - object2.x-c2[1])**2+\
             (object1.y+c1[2] - object2.y-c2[2])**2\
             < (c1[0]+c2[0])**2:
               return True
    return False

def checkfinishline():
    if (player1.y > finishline.y) and (player1.x > finishline.x-100)\
       and ((player1.x < finishline.x+100)) and (player1.y < finishline.y+10):
        return True
    else:
        return False

printMED("Level: "+str(level),700,20)

def startagain():
    global speed, player1alive, finishline, player1
    speed = 1
    player1alive = True
    canvas1.delete("all")
    speed = 1  # mountain is moving up at 1 pixel per 20ms
    mountain.clear()
    mountainice.clear()
    finishline = GameObject("FinishLine.png",x=400,y=30*(mountainheight+6)+400)
     # garbage collector frees memory for all "old" objects, don't need to "free" object
    mountainice.append(finishline)
    #adddirt()
    player1 = GameObject("skier.png","skier2.png","skier3.png",x=400,y=200)
    player1.collisioncirclelist.append((7,2,0))
    addwalls()
    addobstacles()
    timerupdate()
    printMED("Level: "+str(level),700,20)
    

def timerupdate():
    global speed, player1alive, level, score, highscore, mountainheight
    if player1alive == False: return
    speed = speed + 0.03
    if player1.theta == 270:
        score = score + 4
    else:
        score = score + 1
    if score > highscore: highscore = score
    if speed >= 8: speed = 8
    mdy = speed*math.sin(player1.theta*math.pi/180)  # convert to radians
    mdx = -speed*math.cos(player1.theta*math.pi/180)
    for m in mountain:
        m.move(mdx,mdy)
        if checkcollisioncircles(m,player1):
            printBIG("Crashed!",400,300)
            printMED("Press SPACE to start again",400,360)
            player1alive = False
            score = 0
            level = 1
            mountainheight = 40
    for m in mountainice:
        m.move(mdx,mdy)
    if checkfinishline():
       printBIG("Finished!",400,450)
       printMED("Press SPACE for NEXT level",400,510)
       player1alive = False
       mountainheight = mountainheight + 60
       level = level + 1
    canvastext.itemconfigure(scoretext, text = str(score))
    canvastext.itemconfigure(besttimetext, text = str(highscore)) 
    mainwin.after(refreshrate,timerupdate)


def mykey(event):
    global theta, speed, player1alive, finishline, starttime, besttime, player1
    if event.char == " " and player1alive == False:
      startagain()
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
