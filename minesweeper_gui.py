""" This file contains the frontend code for the game"""
# ==== Imports
import tkinter as tk
from tkinter import messagebox
import os
# from PIL import Image, ImageTK
# Importing the minesweeper class
from minesweeper_core import Minesweeper
from score_loading import load_scores,save_scores

class MinesweeperGUI(tk.Tk):

    def __init__(self,n=10,num_mines=12):
        super().__init__()
        self.title("Minesweeper")
        
        # == initialization of images
        self.images = {}
        self.load_images()
        print(self.images.keys())

        # Creating an instance of the backend
        self.game = Minesweeper(n,num_mines)
        self.buttons = {}

        # == Framing of game, score and player name ========================
        self.frame_scores = tk.Frame(self)                             
        self.frame_scores.grid(row=0, column=0, sticky="ew")

        self.frame_board = tk.Frame(self)                                
        self.frame_board.grid(row=1, column=0) 

        self.label_name = tk.Label(self.frame_scores, text="Player Name:", font=('Arial',12))
        self.label_name.pack(side="left", padx=(10,0))
        self.entry_name = tk.Entry(self.frame_scores, width=15, font=('Arial',12))
        self.entry_name.pack(side="left", padx=(0,10))

        # == Score displaying ======================

        # == Current Score
        self.current_score = tk.IntVar(value=0)                                
        self.label_score = tk.Label(self.frame_scores,                       
                                     textvariable= self.current_score, font=('Arial', 12))    
        self.label_score.pack(side="left", padx=10)

        # == Top 3 score
        self.top3_label = tk.Label(self.frame_scores,                          
                                   text="Top 3 Scores:\n1. -\n2. -\n3. -",   
                                   font=('Arial', 10))                         
        self.top3_label.pack(side="right", padx=10) 

        self.create_widgets()
        self.update_top3_display()

    # === Top scoring displaying
    def update_top3_display(self):
        top_scores = load_scores(top_n=3)  # your function returning list of scores
        text = "Top 3 Scores:\n"
        for idx, s in enumerate(top_scores, start=1):
            text += f"{idx}. {s}\n"
        # if fewer than 3 scores, fill blanks
        for idx in range(len(top_scores)+1, 4):
            text += f"{idx}. -\n"
        self.top3_label.config(text=text)
        print(f"Top scores:{top_scores}")

    def create_widgets(self):
        """ This function involves the creation of buttons
            and grid layout"""
        
        # Iterating by rows and columns
        for r in range(self.game.n):
            for c in range(self.game.n):
                # Creating button for each cell
                button = tk.Button(
                    self.frame_board,
                    image=self.images.get('hidden'),
                    width=40,
                    height=40,
                    relief="solid",       
                    bg="#f5f5dc",          
                    activebackground="#eae6d5",  
                    highlightthickness=0,
                    padx=0,
                    pady=0,
                    command = lambda r=r,c=c:self.click_cell(r,c) # command executed when button is pressed
                )
                button.grid(row=r,column=c)
                self.buttons[(r,c)] = button

    def load_images(self):
        """ Loading all the images required for the game"""

        # Define the directory where images are stored
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGE_DIR = os.path.join(BASE_DIR, "images")        
        # Store references to all images
        self.images = {}
        
        try:
            # Load number images (1 through 8)
            for i in range(1, 9):
                filename = f"{i}.png"
                print(filename)
                full_path = os.path.join(IMAGE_DIR, filename)
                print(f"Path to images:{full_path}")
                self.images[i] = tk.PhotoImage(file=full_path) 
                
            # Load special images
            self.images['mine'] = tk.PhotoImage(file=os.path.join(IMAGE_DIR, "mine.png"))
            self.images['hidden'] = tk.PhotoImage(file=os.path.join(IMAGE_DIR, "hidden.png"))

        except tk.TclError as e:
            print(f"Error loading image files from /{IMAGE_DIR}. Ensure all files are present.")
            print(f"Details: {e}")


# ==== Action when a cell is clicked
    def click_cell(self,r,c):
        
        self.game.reveal_cell(r,c)
        # Update GUI
        self.update_gui()
        # Outputs new player view in the terminal -- for debugging purposes
        self.game.player_view()
        # When clicked - disable button and keep pressed
        button = self.buttons[(r,c)]
        button.config(
            state=tk.DISABLED,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )

    def game_status(self):
        # Updating score
        self.current_score.set(self.game.score)
        self.player_name = self.entry_name.get().strip()
        if not self.player_name:
            self.player_name = "Anonymous"

        if self.game.game_active == False:
            save_scores(self.player_name,self.game.score)

            if self.game.win == False:
                # Losing situation
                again = messagebox.askyesno( "You hit a mine! So sad :(",f" \n\nScore: {self.game.score}\n\nTry again?")
            else:
                # Winning situation
                again = messagebox.askyesno("Congratulations!", f"You won! 🎉\n\nScore: {self.game.score}Play again?")

            if again:
                self.destroy()
                app = MinesweeperGUI(self.game.n, self.game.num_mines)
                app.mainloop()
            else:
                self.destroy()
            
        
    def update_gui(self):
        """ This function updates the interface after any player actions
        Buttons have 3 different state
        Hidden
        Revealed
        Flagged
        Connected to self.game.view and self.game.board
        """
        # == Reveals buttons on GUI
        for r in range(self.game.n):
            for c in range(self.game.n):
                button = self.buttons[(r,c)]

                view_state = self.game.view[r, c]
                board_content = self.game.board[r, c]

                if view_state ==1:
                    button.config(
                        state=tk.DISABLED,
                        relief=tk.FLAT,
                        borderwidth=0,
                        text=""
                    )
                
                    # == Assign the Image based on number on board

                    #Mine
                    if board_content == -1:
                        button.config(image=self.images['mine'],bg="#fa562d",)
                    # Numbers
                    elif 1<=board_content<=8:
                        button.config(image=self.images[board_content])


    
        self.game_status()

    

                   
if __name__ == "__main__":
    app = MinesweeperGUI(n=8, num_mines=10)
    app.mainloop()