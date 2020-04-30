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

# import macgyv_constants as mg_co
# import macgyv_classes as mg_cl
from macgyv_constants import *
from macgyv_classes import *

pygame.init()

# Open the window pygame (square)
window = pygame.display.set_mode((WINDOW_SIDE, WINDOW_SIDE))
# Add icon
icon = pygame.image.load(IMAGE_ICON)
pygame.display.set_icon(icon)
# Title
pygame.display.set_caption(WINDOW_TITLE)

level = Level('n1')
level.generate()
level.display_level(window)

# Creation of MacGyver
mg = Person(IMAGE_PERSO, level)
watchman = Person(IMAGE_ARRIVAL, level)
(watchman.pix_x, watchman.pix_y) = ((NBR_SPRITE_SIDE - 1) * SPRITE_SIZE, \
	(NBR_SPRITE_SIDE - 1) * SPRITE_SIZE)

# Creation of the survival items
ether = Tool(IMAGE_ETHER, level)
needle = Tool(IMAGE_NEEDLE, level)
tube = Tool(IMAGE_TUBE, level)

# Condition to avoid the survival items to be localised on
# start and arrival case
while (needle.pix_x, needle.pix_y) == (0, 0) or \
    (needle.pix_x, needle.pix_y) == ((NBR_SPRITE_SIDE - 1) * SPRITE_SIZE, \
        (NBR_SPRITE_SIDE - 1) * SPRITE_SIZE) or \
    (ether.pix_x, ether.pix_y) == (0, 0) or \
    (ether.pix_x, ether.pix_y) == ((NBR_SPRITE_SIDE - 1) * SPRITE_SIZE, \
        (NBR_SPRITE_SIDE - 1) * SPRITE_SIZE) or \
    (tube.pix_x, tube.pix_y) == (0, 0) or \
    (tube.pix_x, tube.pix_y) == ((NBR_SPRITE_SIDE - 1) * SPRITE_SIZE, \
        (NBR_SPRITE_SIDE - 1) * SPRITE_SIZE) or \
    (needle.pix_x, needle.pix_y) == (ether.pix_x, ether.pix_y) or \
    (needle.pix_x, needle.pix_y) == (tube.pix_x, tube.pix_y) or \
    (ether.pix_x, ether.pix_y) == (tube.pix_x, tube.pix_y):

    needle.random_pos()
    ether.random_pos()
    tube.random_pos()

# print((needle.pix_x, needle.pix_y))
# print((ether.pix_x, ether.pix_y))
# print((tube.pix_x, tube.pix_y))

window.blit(needle.survival, (needle.pix_x, needle.pix_y))
window.blit(ether.survival, (ether.pix_x, ether.pix_y))
window.blit(tube.survival, (tube.pix_x, tube.pix_y))

# Refreshing
pygame.display.flip()

# MAIN LOOP
CONTINUE_MAIN = 1
pygame.key.set_repeat(400, 30)

COUNT_SURVIVAL = 0

while CONTINUE_MAIN:
    CONTINUE_GAME = 1
    CONTINUE_OVER = 1

    while CONTINUE_GAME:
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():
            # If the user wants to quit: escape button or close window icon
            # variable CONTINUE_MAIN = 0
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                CONTINUE_MAIN = 0
                CONTINUE_GAME = 0
                CONTINUE_OVER = 0

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
        # - Variable COUNT_SURVIVAL to count the number of items collected
        if (mg.pix_x, mg.pix_y) == (needle.pix_x, needle.pix_y):
            (needle.pix_x, needle.pix_y) = ((len(level.structure) - 1) * SPRITE_SIZE, \
                (len(level.structure) - 1) * SPRITE_SIZE)
            COUNT_SURVIVAL += 1
        elif (mg.pix_x, mg.pix_y) == (ether.pix_x, ether.pix_y):
            (ether.pix_x, ether.pix_y) = ((len(level.structure) - 1) * SPRITE_SIZE, \
                (len(level.structure) - 1) * SPRITE_SIZE)
            COUNT_SURVIVAL += 1
        elif (mg.pix_x, mg.pix_y) == (tube.pix_x, tube.pix_y):
            (tube.pix_x, tube.pix_y) = ((len(level.structure) - 1) * SPRITE_SIZE, \
            (len(level.structure) - 1) * SPRITE_SIZE)
            COUNT_SURVIVAL += 1

        level.display_level(window)
        window.blit(mg.face, (mg.pix_x, mg.pix_y))
        window.blit(needle.survival, (needle.pix_x, needle.pix_y))
        window.blit(ether.survival, (ether.pix_x, ether.pix_y))
        window.blit(tube.survival, (tube.pix_x, tube.pix_y))
        # Blit the watchman after the survival tools to cover them
        # when their position changed to be on arrival case
        window.blit(watchman.face, (watchman.pix_x, watchman.pix_y))

        pygame.display.flip()

        # Two possible options when MacGyver arrived at the arrival case:
        # loop game closes and loop over will display a picture depending on the situation
        if level.structure[mg.case_y][mg.case_x] == 'a':
            CONTINUE_GAME = 0

    # GAME-OVER LOOP
    # Window's game closes when MacGyver meets the watchman, a new picture appears
    MES = 0
    while CONTINUE_OVER:
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                CONTINUE_MAIN = 0
                CONTINUE_GAME = 0
                CONTINUE_OVER = 0

        if COUNT_SURVIVAL == 4:
            MESSAGE = "Congratulations, you win! MacGyver sedated the watchman and escaped."
            MES += 1
            win = pygame.image.load(IMAGE_WIN)
            window.blit(win, (0, 0))
            pygame.display.flip()
        else:
            MESSAGE = "Sorry, you loose... and nothing good happened to MacGyver."
            MES += 1
            loose = pygame.image.load(IMAGE_LOOSE)
            window.blit(loose, (0, 0))
            pygame.display.flip()

        if MES == 1:
            print(MESSAGE)
