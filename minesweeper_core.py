## ================= minesweeper_core.py ======================== ##
""" 
This .py file contains the backend logic for the minesweeper game

"""
## == Imports
import numpy as np

##================================================================
# Poetry and not environment
# Mention packages on README
# Stats
# Error handling
# Logic

class Minesweeper:
    """
    This is a class for an instance of a minesweeper game.
    Holding full board information on where the mines are,
    and numbers that should be displayed in each tile. It also
    keeps a version of the board that the player can see.
    """
    def __init__(self,n,num_mines=10):
        self.n = n
        self.num_mines = num_mines
        self.score = 0
        # Board with all the known locations of the board
        self.board = self._make_board()
        # == Apply numbers to cells
        self.surrounding_bomb_count()

        # Board that player can see
        self.view = np.zeros((n,n),dtype=int)

        # State of the game
        self.game_active = True
        self.count_safe_cells = (n*n)-self.num_mines
        self.revealed_safe = 0

        # Assumption - playing is winning till they uncover a bomb
        self.win = True

    def _make_board(self):
        """
        Creates an 2d array similating the board layout and randomly places
        mines as required. Mines represented as '-1' in array.
        Parameters:
            self - all attriutes of the class
        Returns:
            board - array, 2d array of board format and placements of mines
    
        """
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

        return board

    def get_neighbours(self,r,c):
        """
        Checks the neighbours of a specific tile, to see which ones
        have mines in them
        Parameters:
            self - all attriutes of the class
            r - index, row of tile
            c - index, column of tile
        Returns:
            neighbours - array, list of the locations of neighbours that have mines
        """
        n = self.n

        neighbours = []
        for i in range(max(0,r-1),min(n,r+2)):
            for j in range(max(0,c-1),min(n,c+2)):
                # Skipping current cell
                if (i,j) !=(r,c):
                    neighbours.append((i,j))
        return neighbours

    def surrounding_bomb_count(self):
        """
        This function counts the number of bombs surrounding each cell, and
        fills that cell with that number
        Parameters:
            self - all attriutes of the class
        Returns:
        """
        n = self.n
        for r in range(n):
            for c in range(n):
                # Only doing counting for cells with no mines
                if self.board[r,c] != -1:
                    mine_count = 0
                    for nr, nc in self.get_neighbours(r,c):
                        # If cell has a bomb
                        if self.board[nr,nc] == -1:
                            mine_count+=1
                    self.board[r,c] = mine_count

    def reveal_cell(self,r,c):
        """
        This cell handles what happens after a player choses a cell,
        and it updates self.view of the player
        Parameters:
            self - all attriutes of the class
            r - index, row of tile
            c - index, column of tile
        Returns:
        """
        n = self.n

        # Handling out of bounds cases
        if not (0 <= r < n and 0 <= c < n):
            return
        # Handling revealed
        cell_value = self.board[r,c]
        self.view[r,c]=1

        if self.view[r,c]!=0:
            self.score += 20
            self.revealed_safe += 1

        #Game over - lose situation
        if cell_value == -1:
            self.game_active = False
            self.win = False
            return 
        
        # Game over - win situation
        if self.revealed_safe == self.count_safe_cells:
            self.game_active = False
            # Bonus score
            self.score +=1000 # TODO: add timer => shorter time it takes to finish = larger multiplyer score
        
        # Handling when there are no bombs surrounding
        """ In this case, you recursively reveal all neighbours till a cell
        with a number is revealed"""
        
        if cell_value ==0:
            for nr,nc in self.get_neighbours(r,c):
                if self.view[nr, nc] == 0:
                    self.reveal_cell(nr,nc) # Here the function will be calling itself
    
  

## === Debugging area =====================================================
    def print_mine_board(self):
        """
        This function holds the layout of the board
        Parameters:
            self - all attriutes of the class
        Returns:
        """
        print(f"\n **Full Mine Board ({self.n}x{self.n})**:")
        print("(-1 = Mine, 0-8 = Surrounding Mine Count)")
        print(self.board)
    
    def player_view(self):
        """
        This function holds the current state of the
        player view of the game
        Parameters:
            self - all attriutes of the class
        Returns:
            display_arr - array, simulation view of what the player is seeing
        """
        n = self.n
        display_arr = np.full((self.n, self.n), 'H', dtype=object)


        # Looping through every cell
        for r in range(n):
            for c in range(n):

                # Check if cell is revealed - show value on player view
                if self.view[r,c] == 1:
                    value = self.board[r, c]
                    display_arr[r, c] = str(value)
                    
        print(display_arr)
        return display_arr

if __name__ == "__main__":
    board_size = 10
    game = Minesweeper(board_size, num_mines=12)

# ==Simulation of a game

    print("#== Initial State ==#")
    game.print_mine_board()
    game.player_view()

    # Corner click simulation
    print("*Corner click*")
    game.reveal_cell(0, 0)
    game.player_view()

    # Center click 
    print("*Center click*")
    game.reveal_cell(3,3)
    game.player_view()
    


