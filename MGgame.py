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
(watchman.x, watchman.y) = ((nbr_sprite_side - 1) * sprite_size, (nbr_sprite_side - 1) * sprite_size)

# Creation of the survival items
ether = Tool(image_ether, level)
needle = Tool(image_needle, level)
tube = Tool(image_tube, level)

# Condition to avoid the survival items to be localised on
# start and arrival case
while (needle.x, needle.y) == (0, 0) or \
	(needle.x, needle.y) == ((nbr_sprite_side - 1) * sprite_size, (nbr_sprite_side - 1) * sprite_size) or \
	(ether.x, ether.y) == (0, 0) or \
	(ether.x, ether.y) == ((nbr_sprite_side - 1) * sprite_size, (nbr_sprite_side - 1) * sprite_size) or \
	(tube.x,tube.y) == (0, 0) or \
	(tube.x, tube.y) == ((nbr_sprite_side - 1) * sprite_size, (nbr_sprite_side - 1) * sprite_size) or \
	(needle.x, needle.y) == (ether.x, ether.y) or \
	(needle.x, needle.y) == (tube.x, tube.y) or \
	(ether.x, ether.y) == (tube.x, tube.y):

	needle.random_pos()
	ether.random_pos()
	tube.random_pos()

# print((needle.x, needle.y))
# print((ether.x, ether.y))
# print((tube.x, tube.y))

window.blit(needle.survival, (needle.x, needle.y))
window.blit(ether.survival, (ether.x, ether.y))
window.blit(tube.survival, (tube.x, tube.y))

# Refreshing
pygame.display.flip()

# MAIN LOOP
continue_main = 1
pygame.key.set_repeat(400,30)

count_survival = 0

while continue_main:
	continue_game = 1
	continue_over = 1

	while continue_game:
		pygame.time.Clock().tick(30)

		for event in pygame.event.get():
			# If the user wants to quit: escape button or close window icon
			# variable continue_main = 0
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continue_main = 0
				continue_game = 0
				continue_over = 0

			elif event.type == KEYDOWN:
					# Move MacGyver with the arrow keys
					if event.key == K_RIGHT:
						mg.move('right')
					elif event.key == K_LEFT:
						mg.move('left')
					elif event.key == K_UP:
						mg.move('up')
					elif event.key == K_DOWN:
						mg.move('down')	

		# If the character MacGyver moves on the same case than a tool:
		# - The tool position changes to be on the arrival case
		# - Variable count_survival to count the number of items collected
		if (mg.x, mg.y) == (needle.x, needle.y):
			(needle.x, needle.y) = ((len(level.structure)-1) * sprite_size, (len(level.structure)-1) * sprite_size)
			count_survival += 1
		elif (mg.x, mg.y) == (ether.x, ether.y):
			(ether.x, ether.y) = ((len(level.structure)-1) * sprite_size, (len(level.structure)-1) * sprite_size)
			count_survival += 1
		elif (mg.x, mg.y) == (tube.x, tube.y):
			(tube.x, tube.y) = ((len(level.structure)-1) * sprite_size, (len(level.structure)-1) * sprite_size)
			count_survival += 1
		
		level.display_level(window)
		window.blit(mg.face, (mg.x, mg.y)) 
		window.blit(needle.survival, (needle.x, needle.y))
		window.blit(ether.survival, (ether.x, ether.y))
		window.blit(tube.survival, (tube.x, tube.y))
		# Blit the watchman after the survival tools to cover them
		# when their position changed to be on arrival case
		window.blit(watchman.face, (watchman.x, watchman.y)) 

		pygame.display.flip()

		# Two possible options when MacGyver arrived at the arrival case:
		# loop game closes and loop over will display a picture depending on the situation
		if level.structure[mg.case_y][mg.case_x] == 'a':
				continue_game = 0

	# GAME-OVER LOOP
	# Window's game closes when MacGyver meets the watchman, a new picture appears
	while continue_over:
		pygame.time.Clock().tick(30)

		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continue_main = 0
				continue_game = 0
				continue_over = 0

		if count_survival == 4:
			message = "Congratulations, you win! MacGyver sedated the watchman and escaped. "
			win = pygame.image.load(image_win)
			window.blit(win, (0,0))
			pygame.display.flip()
		else:
			message = "Sorry, you loose... and nothing good happened to MacGyver."
			loose = pygame.image.load(image_loose)
			window.blit(loose, (0,0))
			pygame.display.flip()

		print(message)

	
	