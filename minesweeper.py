# Poetry and not environment
# Mention packages on README
# Stats
# Error handling
# Logic
import tkinter
import numpy as np

## ==== Minesweeper backend ==== ##

class Minesweeper:
    def __init__(self,n,num_mines=10):
        self.n = n
        self.num_mines = num_mines
        self.game_over = False

        # Board with all the known locations of the board
        self.board = self._make_board()
        # == Apply numbers to cells
        self._surrounding_bomb_count()

        # Board that 
        self.view = np.zeros((n,n),dtype=int)



# Define squares
# ==== Making the board ===== #
    def _make_board(self):
            n = self.n
            board = np.zeros((n,n),dtype=int)
            print(board)
            n = self.n
            # Check if board large enough for number of mines
            if self.num_mines > n * n:
                raise ValueError("Number of mines exceeds board capacity")
            
            # Unique indices
            all_indices = np.arange(n*n)

            # Randomly placing the mines
            mine_indices = np.random.choice(all_indices, size = self.num_mines, replace = False)

            # Multi-dimensional indices
            mine_locations = np.unravel_index(mine_indices, board.shape)

            # Placing mines
            board[mine_locations] = - 1

            print(f"Board size: {n}x{n}. Mines placed: {self.num_mines}.")
            print("Mines are represented by -1.")
            return board


    # ======== Assigning the numbers for uncovered cells ======== #

    # == Function to get neighbours of a cell == #
    def _get_neighbours(self,r,c):
        """ Returns a list for all 8 neighbours of a cell"""
        n = self.n
        neighbours = []
        for i in range(max(0,r-1),min(n,r+2)):
            for j in range(max(0,c-1),min(n,c+2)):
                # Skipping current cell
                if (i,j) !=(r,c):
                    neighbours.append((i,j))
        return neighbours

    def _surrounding_bomb_count(self):
        """ This function counts the number of bombs surrounding each cell, and
                fills that cell with that number """
        n = self.n
        for r in range(n):
            for c in range(n):
                # Only doing counting for cells with no mines
                if self.board[r,c] != -1:
                    mine_count = 0
                    for nr, nc in self._get_neighbours(r,c):
                        # If cell has a bomb
                        if self.board[nr,nc] == -1:
                            mine_count+=1
                        self.board[r,c] = mine_count
    
    

    def print_mine_board(self):
        print(f"\n **Full Mine Board ({self.n}x{self.n})**:")
        print("(-1 = Mine, 0-8 = Surrounding Mine Count)")
        print(self.board)

    def print_player_view(self):
        display_arr = np.full((self.n, self.n), 'H', dtype=object)
        
        # This function currently just shows all 'H' since no cells have been revealed (view is all 0s)
        print(f"\n👀 **Player View ({self.n}x{self.n})**:")
        print("('H' = Hidden Cell)")
        print(display_arr)





# == Minesweeper methods == #
# Modify values 


# function to update board
board_size = 10
game = Minesweeper(board_size, num_mines=12)

# Print both boards
game.print_mine_board()
game.print_player_view()
