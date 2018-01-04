from Tkinter import *
import tkMessageBox, tkSimpleDialog, itertools, numpy as np
PLAYING = True

class Board():
    
    def __init__(self, root):
        self.root = root
        self.grid = []

    def buttons(self):
        for i in range(15):
            row = []
            for j in range(15):
                row.append(Button(self.root, width = 2 , height = 1 ,command = lambda i = i, j = j: self.click(i, j)))
                row[-1].grid(row=i,column=j)
            self.grid.append(row)

    def player(self):
        count_moves = 0
        for row in self.grid:
            for j in row:
                if j["bg"]=="black" or j["bg"]== "peachpuff":
                    count_moves += 1
        if count_moves % 2 == 0:
            return 1
        return 2

    def opp_player(self):
        if self.player() == 1:
            return 2
        return 1

    def click(self, i, j):
        
        # If there is already a piece, do nothing on click
        if self.grid[i][j]["bg"] == "peachpuff" or self.grid[i][j]["bg"] == "black":
            return

        # Else, fill clicked button with player's color
        pn = self.player()
        if pn == 1:
            self.grid[i][j]["bg"] = "peachpuff"
        else:
            self.grid[i][j]["bg"] = "black"

        # Declare winner and handle either restart or quit, depending on input
        if self.game_over():
            label.configure(text = str("Player " + str( self.opp_player() ) + " won") )
            input_str = ""
            while input_str != "y" and input_str != "n":
                input_str = tkSimpleDialog.askstring("Play again?","y or n")
            if input_str == "y":
                self.root.destroy()
            else: # input_str == "n"
                global PLAYING
                PLAYING = False
                self.root.destroy()
        else: # game not over
            label.configure(text=str("Player " + str(self.player()) + "'s turn"))

    # Takes a 1 dimensional list, determines if 5 of the same user colors appear in a row
    def five_in_a_row_1d(self, list_):
        i = 0
        return_val = -1
        while i < len(list_) - 4:
            ls = [list_[i+x]["bg"] for x in range(0,5)]
            if ls[1:] == ls[:-1] and (ls[0]=="black" or ls[0]=="peachpuff"):
                for x in range(0,5):
                    list_[i+x]["bg"] = "cyan"
                return_val = ls[0]
            i += 1
        return return_val


    def game_over(self):
        
        # Scan horizontals for five in a row
        for row in self.grid:
            if self.five_in_a_row_1d(row) != -1:
                return True

        # Scan verticals 
        for i in range(0, len(self.grid)):
            if self.five_in_a_row_1d([r[i] for r in self.grid]) != -1:
                return True

        # Scan diagonals
        a = np.array(self.grid)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
        for x in [n.tolist() for n in diags]:
            if self.five_in_a_row_1d(x) != -1:
                return True
            
        return False
    

def on_closing():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        global PLAYING
        PLAYING = False

while PLAYING:
    root = Tk()
    root.title('Gomoku')
    label = Label(root, text="Player 1's turn")
    label.grid(row=16, column=4, columnspan=8, sticky="new")
    board = Board(root)
    board.buttons()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
