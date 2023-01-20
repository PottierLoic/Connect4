# Connect 4 game 
# Author : Loïc Pottier
# Creation date : 15/01/2023

# IMPORTS
import numpy as np
from tkinter import *

# CONSTANTS
WIDTH = 7
HEIGHT = 6
BACKGROUND_COLOR = "#3333FF"
SQUARE_SIZE = 100
IN_BETwEEN = 10

class Board:
    def __init__(self) -> None:
        self.board = np.zeros((HEIGHT, WIDTH), dtype=int)
        self.turn=1
        self.finished=False

    def nextAction(self, column):
        if self.finished:
            return
        if column<0 or column>6:
            return
        done=False
        for i in range(5,-1,-1):
            if self.board[i][column]==0:
                self.board[i][column]=self.turn
                done=True
                break
        if done:
            if self.checkWin():
                tourLabel.config(text=f"Le joueur {self.turn} a gagné !")
                self.finished=True
            else:
                self.turn=2 if self.turn==1 else 1
                tourLabel.config(text=f"Tour : {self.turn}")
            self.graphics()
            
    def changeWinColor(self, color, way, i, j):
        if way=="line":
            for x in range(4):
                self.board[i][j+x]=color+2
        elif way=="collum":
            for y in range(4):
                self.board[i+y][j]=color+2
        elif way=="diagonal1":
            for x in range(4):
                self.board[i+x][j+x]=color+2
        elif way=="diagonal2":
            for x in range(4):
                self.board[i-x][j+x]=color+2

    def checkWin(self) -> bool:
        # check line
        for i in range(HEIGHT):
            for j in range(WIDTH-3):
                if self.board[i][j]==self.board[i][j+1]==self.board[i][j+2]==self.board[i][j+3]!=0:
                    self.finished=True
                    self.changeWinColor(self.board[i][j], "line", i, j)
                    return self.board[i][j]
        
        # check column
        for i in range(HEIGHT-3):
            for j in range(WIDTH):
                if self.board[i][j]==self.board[i+1][j]==self.board[i+2][j]==self.board[i+3][j]!=0:
                    self.finished=True
                    self.changeWinColor(self.board[i][j], "collum", i, j)
                    return self.board[i][j]

        # check diagonal 1
        for i in range(HEIGHT-3):
            for j in range(WIDTH-3):
                if self.board[i][j]==self.board[i+1][j+1]==self.board[i+2][j+2]==self.board[i+3][j+3]!=0:
                    self.finished=True
                    self.changeWinColor(self.board[i][j], "diagonal1", i, j)
                    return self.board[i][j]

        # check diagonal 2
        for i in range(3,HEIGHT):
            for j in range(WIDTH-3):
                if self.board[i][j]==self.board[i-1][j+1]==self.board[i-2][j+2]==self.board[i-3][j+3]!=0:
                    self.finished=True
                    self.changeWinColor(self.board[i][j], "diagonal2", i, j)
                    return self.board[i][j]
       

    def graphics(self):
        canvas.delete("case")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]==0:
                    color="black"
                elif self.board[i][j]==1:
                    color="red"
                elif self.board[i][j]==2:
                    color="yellow"
                else:
                    color="green"
                canvas.create_oval(j*SQUARE_SIZE+IN_BETwEEN*(j+1), i*SQUARE_SIZE+IN_BETwEEN*(i+1), (j+1)*SQUARE_SIZE+IN_BETwEEN*(j+1), (i+1)*SQUARE_SIZE+IN_BETwEEN*(i+1), fill=color, tag="case")

    def reset(self):
        self.board = np.zeros((HEIGHT, WIDTH), dtype=int)
        self.turn=1
        self.finished=False
        canvas.config(bg=BACKGROUND_COLOR)
        tourLabel.config(text=f"Tour : {self.turn}")
        self.graphics()

    def __str__(self) -> str:
        returnStr=""
        for row in self.board:
            for value in row:
                returnStr+=str(value)+" "
            returnStr+="\n"
        return returnStr

def click(event):
    global b
    if not b.finished:
        x=event.x
        y=event.y
        if x<0 or x>WIDTH*SQUARE_SIZE+IN_BETwEEN*(WIDTH+1) or y<0 or y>HEIGHT*SQUARE_SIZE+IN_BETwEEN*(HEIGHT+1):
            return
        column = x//(SQUARE_SIZE+IN_BETwEEN)
        b.nextAction(column)
    else:
        b.reset()


if __name__=="__main__":

    # WINDOW AND TKINTER SECTION
    window = Tk()
    window.title("Connect-4")
    window.resizable(False, False)

    label = Label(window, text="Connect-4", font=("consolas", 10))
    label.pack()

    tourText="Tour : 1"
    tourLabel = Label(window, text=tourText, font=("consolas", 10))
    tourLabel.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT*SQUARE_SIZE+IN_BETwEEN*(HEIGHT+1), width=WIDTH*SQUARE_SIZE+IN_BETwEEN*(WIDTH+1))
    canvas.pack()

    window.update()

    windowWidth = window.winfo_width()
    windowHeight = window.winfo_height()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    x = int((screenWidth/2) - (windowWidth/2))
    y = int((screenHeight/2) - (windowHeight/2))

    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

    # BINDINGS
    window.bind("<Button-1>", click)

    b = Board()

    window.mainloop()



