""" Classes of the labyrinthe game: MacGyver's escape """

import pygame
from pygame.locals import *

import math
from random import randrange

from MGconstants import *


class Level:
	""" Class to create a level """

	def __init__(self, file):
		""" Initialisation """
		self.file = file
		self.structure = 0
		self.count_floor = 0

	def generate(self):
		""" Method to generate a level depending on an input file:
		Creation of a main list, including a list per line to display """

		# Open the file
		with open(self.file, 'r') as file:
			structure_level = []
			for line in file:
				line_level = []
				for sprite in line:
					if sprite != '\n':
						# Add each sprite at the line list
						line_level.append(sprite)
				# Add each row at the level list
				structure_level.append(line_level)
			# Save the structure
			self.structure = structure_level

	def display_level(self, window):
		""" Method to display the chosen level/file depending on
		the structure level given by the method generate() """

		# Load the images of the level
		wall = pygame.image.load(image_wall)
		wallb = pygame.image.load(image_wallb)
		floor = pygame.image.load(image_floor)
		floorb = pygame.image.load(image_floorb)
		departure = pygame.image.load(image_departure)
		arrival = pygame.image.load(image_arrival)

		# Browse the structure of the level
		num_line = 0
		count_floor = 0
		count_wall = 0
		for line in self.structure:
			num_case = 0
			for sprite in line:
				# Real position in pixel
				x = num_case * sprite_size
				y = num_line * sprite_size
				if sprite == 'm':
					if count_wall % 2 == 0:
						window.blit(wallb, (x, y))
					else:
						window.blit(wall, (x, y))
					count_wall += 1
				elif sprite == '0':
					if count_floor % 5 == 0:
						window.blit(floorb, (x, y))
					else:
						window.blit(floor, (x, y))
					count_floor += 1
				elif sprite == 'd':
					window.blit(departure, (x, y))
				elif sprite == 'a':
					window.blit(arrival, (x, y))
				num_case += 1
			num_line += 1

		self.count_floor = count_floor


class Person:
	""" Class to create a character """

	def __init__(self, face, level):
		""" Initialisation """

		# Sprite of the character
		self.face =pygame.image.load(face)
		# Position of the character, case and pixel
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		# Level of the labyrinthe
		self.level = level


class Tool:
	""" Class to create the survival items """

	def __init__(self, survival, level):
		""" Initialisation """

		# Sprite of the survival tool
		self.survival = pygame.image.load(survival)
		# Position of the tool, case and pixel
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		# Level of the labyrinthe
		self.level = level


	def random_pos(self):
		""" Method to assign a random position for each tool: 
		- Careful, only on the floor case and not wall case
		- Must add in main file, a condition to avoid that 
		the tools postion are on start and arrival case """

		# For each tool generate:
		# - Give a random number, between 0 and the number of case floor-1
		hasard_case = randrange(self.level.count_floor)
		print(self.level.count_floor, hasard_case)

		# Search and give the real position in the labyrinthe structure of 
		# the given random case floor.
		num_line = 0
		count = 0
		for line in self.level.structure:
			num_case = 0
			for sprite in line:
				x = num_case * sprite_size
				y = num_line * sprite_size

				if sprite == '0':
					if count == hasard_case:
						self.x = x
						self.y = y
					count += 1
				num_case += 1
			num_line += 1










