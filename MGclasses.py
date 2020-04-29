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
		wall = pygame.image.load(IMAGE_WALL)
		wallb = pygame.image.load(IMAGE_WALLB)
		floor = pygame.image.load(IMAGE_FLOOR)
		floorb = pygame.image.load(IMAGE_FLOORB)
		departure = pygame.image.load(IMAGE_DEPARTURE)
		arrival = pygame.image.load(IMAGE_ARRIVAL)

		# Browse the structure of the level
		num_line = 0
		count_floor = 0
		count_wall = 0
		for line in self.structure:
			num_case = 0
			for sprite in line:
				# Real position in pixel
				x = num_case * SPRITE_SIZE
				y = num_line * SPRITE_SIZE
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

	def move(self, direction):
		""" Method to allow the movement of the character """

		# Movement on the right
		if direction == 'right':
			# Can't move the character outside the screen
			if self.case_x < (NBR_SPRITE_SIDE - 1):
				# Destination case shouldn't be a wall
				if self.level.structure[self.case_y][self.case_x + 1] != 'm':
					# Movement +1 case
					self.case_x += 1
					# Determination of the real position in pixel
					self.x = self.case_x * SPRITE_SIZE

		# Movement on the left
		if direction == 'left':
			if self.case_x > 0:
				if self.level.structure[self.case_y][self.case_x - 1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * SPRITE_SIZE

		# Movement upward
		if direction == 'up':
			if self.case_y > 0:
				if self.level.structure[self.case_y - 1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * SPRITE_SIZE

		# Movement downward
		if direction == 'down':
			if self.case_y < (NBR_SPRITE_SIDE - 1):
				if self.level.structure[self.case_y + 1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * SPRITE_SIZE


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
		- Careful, only on the floor cases and not on the wall cases
		- Must add in main file, a condition to avoid that 
		the tools postion are on start and arrival cases """

		# For each tool generated:
		# - Give a random number, between 0 and the number of case floor-1
		hasard_case = randrange(self.level.count_floor)
		# print(self.level.count_floor, hasard_case)

		# Search and give the real position in the labyrinthe structure of 
		# the given random case floor.
		num_line = 0
		count = 0
		for line in self.level.structure:
			num_case = 0
			for sprite in line:
				x = num_case * SPRITE_SIZE
				y = num_line * SPRITE_SIZE

				if sprite == '0':
					if count == hasard_case:
						self.x = x
						self.y = y
					count += 1
				num_case += 1
			num_line += 1










