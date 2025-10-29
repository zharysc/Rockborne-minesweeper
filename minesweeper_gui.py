""" This file contains the frontend code for the game"""
# ==== Imports
import tkinter as tk
# Importing the minesweeper class
from minesweeper_core import Minesweeper

class MinesweeperGUI(tk.Tk):

    def __init__(self,n=10,num_mines=12):
        super().__init__()
        self.title("Minesweeper")

        # Creating an instance of the backend
        self.game = Minesweeper(n,num_mines)
        self.buttons = {}

        self.create_widgets()

    def create_widgets(self):
        """ This function involves the creation of buttons
            and grid layout"""
        
        # Iterating by rows and columns
        for r in range(self.game.n):
            for c in range(self.game.n):
                # Creating button for each cell
                button = tk.Button(
                    self,
                    text = "",
                    width=3,
                    height=1,
                    command = lambda r=r,c=c:self.click_cell(r,c) # command executed when button is pressed
                )
                button.grid(row=r,column=c)
                self.buttons[(r,c)] = button
                
# ==== Action when a cell is clicked
    # def click_cell(self,r,c):
        # pending... need to build function to reveal cell

if __name__ == "__main__":
    app = MinesweeperGUI(n=8, num_mines=10)
    app.mainloop()