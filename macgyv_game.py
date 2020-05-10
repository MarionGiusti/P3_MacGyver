#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Labyrinthe game: MacGyver must escape !
MacGyver can move with the arrow keys on the computer keyboard.
To win : find the arrival and sedate the watchman !
    - He has to collect the 3 survival items (plastic tube, needle and
     ether) to make a syringe.
    - Only at this condition, he will escape.
    - Otherwise, the watchman will still be awake...
    may his soul rest in peace.

Script Python
Files:
macgyv_game.py (main script),
macgyv_classes.py and macgyv_constants.py (modules),
n1 (labyrinth structure), images.
"""

from macgyv_classes import GameManager

def main():
    """ Run the game """
    game = GameManager()
    game.choose_random()
    game.game_loop(game.window)

if __name__ == "__main__":
    main()
    