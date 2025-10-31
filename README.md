# Zharys' Minesweeper v1
As part of Rockborne's Python project, we have been tasked with 
creating a game. This project involves the recreation of the classic minesweeper game. Hope you enjoy!

## Description
Minesweeper v1, contains the basic logic of the game. This project was written in different .py scripts, a brief description of each being shown below:
- minesweeper_core.py: containing game logic to follow the rules of the game
- minesweeper_gui.py: containing code for the user interface for the player to play the game.
minesweeper_main.py: Main file to be run containing only the main() function.
- score_loading.py: This file contains functions relating to the loading and writing of the score history stored in scores_history.csv.
## Getting Started
### Prerequisites - Imports:
* numpy, os, csv, datetime,tkinter

### Executing the program - playing the game
1. Right click on minesweeper_main.py and run with Python
2. Select game difficulty
3. Write your player name
4. Press start game

## General game information
### Difficulty levels:
* Easy - 64 tiles, 10 mines 
* Medium - 100 tiles, 20 mines
* Hard - 144 tiles , 30 mines
* Insane - 225 tiles - 45 mines

### How to play:
1. Click a tile to uncover it - aim is to uncover as many safe tiles as possible
    +20 for every safe tile revealled
2. Tiles with numbers give hints to how many mines are in their surrounding neighbours. 
    Use this to help deduce where mines are, and where safe tiles are located
3. Game will end when a mine is uncovered OR when all safe tiles are found
HAVE FUN :>

## Acknowledgments
* Images within the game taken from 
    1. [Frepik] (<a href="https://www.flaticon.com/free-icons/bomb" title="bomb icons">Bomb icons created by Freepik - Flaticon</a>)
    2. [IconsBox](<a href="https://www.flaticon.com/free-icons/IconsBox - Flaticon</a>)
