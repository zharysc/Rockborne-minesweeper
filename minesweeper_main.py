# ========= minesweeper_main.py ============= # 
"""
This code contains the main() function only which use is to make an instance
of the game
"""
# ==== TODO: this is a list of things to do for future versions of the game
# Add flag system

# ===========================================

## == Imports ========
from minesweeper_gui import MinesweeperGUI

def main():
    """

    Entry point to start the Minesweeper game GUI.

    Parameters:
    Returns:
    
    """
    app = MinesweeperGUI(n=10, num_mines=12)
    app.mainloop()

if __name__ == "__main__":
    main()