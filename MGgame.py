#!/usr/bin/python3
# -*- coding: Utf-8 -*

""" 
Labyrinthe game: MacGyver must escape !
MacGyver can move with the arrow keys on the computer keyboard.
To win : find the arrival and sedate the watchman !
	- He has to collect the 3 survival items (plastic tube, needle and ether) to make a syringe. 
	- Only at this condition, he will escape.
	- Otherwise, the watchman will still be awake...may his soul rest in peace.
"""

import pygame
from pygame.locals import *

import math
from random import randrange

from MGconstants import *
from MGclasses import *

pygame.init()

# Open the window pygame (square)
window = pygame.display.set_mode((window_side, window_side))
# Add icon
icon = pygame.image.load(image_icon)
pygame.display.set_icon(icon)
# Title
pygame.display.set_caption(window_title)

level = Level('n1')
level.generate()
level.display_level(window)

# Creation of MacGyver
mg = Person(image_perso, level)
watchman = Person(image_arrival, level)

(watchman.pix_x, watchman.pix_y) = ((nbr_sprite_side - 1) * sprite_size, (nbr_sprite_side - 1) * sprite_size)



# Rafraichissement
pygame.display.flip()

# MAIN LOOP
continue_main = 1
pygame.key.set_repeat(400,30)

while continue_main:

	for event in pygame.event.get():
		# If the user want to quit: escape button or close window icon
		# variable continue_main = 0
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
			continue_main = 0


	
	level.display_level(window)
	window.blit(mg.face, (mg.pix_x, mg.pix_y)) 
	window.blit(watchman.face, (watchman.pix_x, watchman.pix_y)) 

	pygame.display.flip()