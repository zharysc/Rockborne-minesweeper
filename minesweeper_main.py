from minesweeper_gui import MinesweeperGUI

def main():
    """Entry point to start the Minesweeper game GUI."""
    app = MinesweeperGUI(n=10, num_mines=12)
    app.mainloop()

if __name__ == "__main__":
    main()