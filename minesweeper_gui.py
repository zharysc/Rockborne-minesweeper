## ================= minesweeper_core.py ======================== ##
""" 
This .py file contains the frontend code for the minesweeper game.
Includes code for the User interface.

"""
## == Imports
import tkinter as tk
from tkinter import messagebox
import os
from minesweeper_core import Minesweeper
from score_loading import load_scores,save_scores

##================================================================ ##

class MinesweeperGUI(tk.Tk):

    def __init__(self,n=10,num_mines=12):
        super().__init__()
        self.title("Minesweeper")
        
        # == initialization of images
        self.images = {}
        self.load_images()
        print(self.images.keys())

        
        # == Elements for User Interface ========================
        """
        This section here contains the creation of elements for 
        the user interface

        """
        self.frame_scores = tk.Frame(self)                             
        self.frame_scores.grid(row=0, column=0, sticky="ew")

        # == Picking difficulty 
        self.label_difficulty = tk.Label(self.frame_scores, text="Difficulty:",
                                          font=('Arial',12))
        self.label_difficulty.pack(side="left", padx=(10,0))

        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_options = ["Easy", "Medium", "Hard","Insane"]
        self.option_difficulty = tk.OptionMenu(
            self.frame_scores, self.difficulty_var, *difficulty_options)
        self.option_difficulty.pack(side="left", padx=(0,10))

        # == Start Button
        self.btn_start = tk.Button(self.frame_scores,
                                    text="Start Game", command=self.start_game)
        self.btn_start.pack(side="left", padx=(0,10))

    
        # == Board
        self.frame_board = tk.Frame(self)                                
        self.frame_board.grid(row=1, column=0) 

        # == Input for player name
        self.label_name = tk.Label(self.frame_scores,
                                    text="Player Name:",
                                      font=('Arial',12))
        self.label_name.pack(side="left", padx=(10,0))
        self.entry_name = tk.Entry(self.frame_scores, width=15,
                                    font=('Arial',12))
        self.entry_name.pack(side="left", padx=(0,10))

        # == Current Score
        self.current_score = tk.IntVar(value=0)                                
        self.label_score = tk.Label(
                                self.frame_scores,
                                textvariable= self.current_score,
                                font=('Arial', 12))    
        self.label_score.pack(side="left", padx=10)

        # == Displaying the top 3 scores
        self.top3_label = tk.Label(self.frame_scores,                          
                                   text="Top 3 Scores:\n1. -\n2. -\n3. -",   
                                   font=('Arial', 10))                         
        self.top3_label.pack(side="right", padx=10) 
        self.update_top3_display() # call function to update top scores
    

    def start_game(self):
        """
        This function carries the processes that happens when
        'start game' button is pressed. It create an instance
        of the game with the correct difficulty.
        Parameters:
            self
        Returns:
        """
        # Determine difficulty and set parameters
        sel = self.difficulty_var.get()
        if sel == "Easy":
            n, num_mines = 8, 10
        elif sel == "Medium":
            n, num_mines = 10, 20
        elif sel == "Hard":
            n, num_mines = 12, 30
        else:  # Insane
            n, num_mines = 15, 45

        # Creating an instance of the game
        self.game = Minesweeper(n, num_mines)
        self.buttons = {}

        # Clear anything in frame_board (if previous game)
        for widget in self.frame_board.winfo_children():
            widget.destroy()

        # Create the board buttons
        self.create_widgets() 


    def update_top3_display(self):
        """
        This function calls 'load_scores' and grabs the
        top scores to input into the text label for the UI.
        Parameters:
            self
        Returns:

        """
        # Grab list of top scores
        top_scores = load_scores(top_n=3)
        text = "Top 3 Scores:\n"
        for idx, s in enumerate(top_scores, start=1):
            text += f"{idx}. {s}\n"
        # if fewer than 3 scores, fill blanks
        for idx in range(len(top_scores)+1, 4):
            text += f"{idx}. -\n"
        self.top3_label.config(text=text)
        print(f"Top scores:{top_scores}")


    def create_widgets(self):
        """
        This function involves the creation of buttons
            and grid layout
        Parameters:
            self
        Returns:
        """
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
                    command = lambda r=r,c=c:self.click_cell(r,c)
                )
                button.grid(row=r,column=c)
                self.buttons[(r,c)] = button


    def load_images(self):
        """
        This function loads all the images required for the game
        Parameters:
            self
        Returns:
        """

        # Define the directory where images are stored
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGE_DIR = os.path.join(BASE_DIR, "images")        
        # Store references to all images
        self.images = {}
        
        # Error handling if images cannot be found
        try:
            # Load number images
            for i in range(1, 9):
                filename = f"{i}.png"
                print(filename)
                full_path = os.path.join(IMAGE_DIR, filename)
                print(f"Path to images:{full_path}")
                self.images[i] = tk.PhotoImage(file=full_path) 
                
            # Load special images
            self.images['mine'] = tk.PhotoImage(
                file=os.path.join(IMAGE_DIR, "mine.png"))
            self.images['hidden'] = tk.PhotoImage(
                file=os.path.join(IMAGE_DIR, "hidden.png"))

        except tk.TclError as e:
            print(f"Error loading image files from /{IMAGE_DIR}. Ensure all files are present.")
            print(f"Details: {e}")


    def click_cell(self,r,c):
        """
        This function calls 'reveal_cell()' from backend side,
        to update backend information. Then calls 'update_gui()'
        to update the user interface.
        Parameters:
            self
            r - index, row position of clicked cell
            c - index, column position of clicked cell
        Returns:
        """
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
        """
        This function checks the status of the game after every move.
        Updates the score, and cehcks if user is in a win/lose/playon
        situation.
        Parameters:
            self
        Returns:
        """
        # Updating score
        self.current_score.set(self.game.score)
        self.player_name = self.entry_name.get().strip()
        if not self.player_name:
            self.player_name = "Anonymous"

        # Checks if backend has set game as inactive
        if self.game.game_active == False:
            save_scores(self.player_name,self.game.score)
            # Losing situation
            if self.game.win == False:
                again = messagebox.askyesno( "You hit a mine! So sad :(",f" \n\nScore: {self.game.score}\n\nTry again?")
            # Winning situation
            else:
                again = messagebox.askyesno("Congratulations!", f"You won! 🎉\n\nScore: {self.game.score}Play again?")
            # Checks if the user has requested to play again
            if again:
                self.destroy()
                app = MinesweeperGUI(self.game.n, self.game.num_mines)
                app.mainloop()
            else:
                self.destroy()
            
        
    def update_gui(self):
        """
        This function updates the interface after any player actions
        Buttons have 3 different states [Hidden,Revealed,Flagged].
        Connected to self.game.view and self.game.board
        Parameters:
            self
        Returns:
        """
        # Reveals buttons on GUI
        for r in range(self.game.n):
            for c in range(self.game.n):
                button = self.buttons[(r,c)]
                view_state = self.game.view[r, c]
                board_content = self.game.board[r, c]

                # Gives button revealed format
                if view_state ==1:
                    button.config(
                        state=tk.DISABLED,
                        relief=tk.FLAT,
                        borderwidth=0,
                        text=""
                    )
                    # Assigning correct image to the button
                    if board_content == -1:
                        button.config(image=self.images['mine'],bg="#fa562d",)
                    elif 1<=board_content<=8:
                        button.config(image=self.images[board_content])
        # Calls game_status to update on GUI
        self.game_status()

             
if __name__ == "__main__":
    app = MinesweeperGUI(n=8, num_mines=10)
    app.mainloop()