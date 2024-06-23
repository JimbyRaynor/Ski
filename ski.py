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

class Player:
    def __init__(self,myfilename="",x=0,y=0):
        self.x = x
        self.y = y
        self.image = PhotoImage(file=myfilename).zoom(4,4)
        self.sprite = canvas1.create_image(2,2,anchor=NW,image=self.image)
        canvas1.move(self.sprite,x,y)
    def move(self,dx=0,dy=0):
        self.x = self.x + dx
        self.y = self.y + dy
        canvas1.move(self.sprite,dx,dy)
        




player1 = Player("skier.png",200,200)

flag1 = Player("flag1.png",400,400)


def timerupdate():
    #player1.move(0,0)
    flag1.move(0,-2)
    mainwin.after(100,timerupdate)

mainwin.after(100,timerupdate)
mainwin.mainloop()
