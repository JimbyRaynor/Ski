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
        self.image = PhotoImage(file=filedown).zoom(2,2)
        self.sprite = canvas1.create_image(2,2,anchor=NW,image=self.image)
        if fileleft != "":
           self.imageleft = PhotoImage(file=fileleft).zoom(2,2)
        if fileright != "":
           self.imageright = PhotoImage(file=fileright).zoom(2,2)
        canvas1.move(self.sprite,x,y)
    def move(self,dx=0,dy=0):
        self.x = self.x + dx
        self.y = self.y + dy
        canvas1.move(self.sprite,dx,dy)
    def faceleft(self):
        canvas1.itemconfigure(self.sprite,image=self.imageleft)
    def faceright(self):
        canvas1.itemconfigure(self.sprite,image=self.imageright)
    def facedown(self):
        canvas1.itemconfigure(self.sprite,image=self.image)
        

player1 = GameObject("skier.png","skier2.png","skier3.png",x=390,y=200)

mountain = []
mdx = 0 # move mountain amount
mdy = -2

for i in range(1000):
    mountain.append(GameObject("flag1.png",\
      x=random.randint(1,800),y=400+random.randint(1,20000)))



def timerupdate():
    #player1.move(0,0)
    for m in mountain:
        m.move(mdx,mdy)
    mainwin.after(50,timerupdate)

def mykey(event):
    global mdx, mdy
    if event.char == "w":
        mdx = 0
        mdy = -2
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

