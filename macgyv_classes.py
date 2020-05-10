""" Classes of the labyrinth game: MacGyver's escape """

from random import randrange

import pygame
from pygame.locals import *

from macgyv_constants import WINDOW_SIDE, IMAGE_ICON, WINDOW_TITLE, \
IMAGE_WALL, IMAGE_WALLB, IMAGE_FLOOR, IMAGE_FLOORB, \
IMAGE_DEPARTURE, IMAGE_ARRIVAL, SPRITE_SIZE, NBR_SPRITE_SIDE, \
IMAGE_PERSO, IMAGE_ETHER, IMAGE_NEEDLE, IMAGE_TUBE, \
IMAGE_WIN, IMAGE_LOOSE

class GameManager:
    """ Class to manage the game """

    def __init__(self):
        """ Initialisation """
        pygame.init()
        # Open the window pygame (square)
        self.window = pygame.display.set_mode((WINDOW_SIDE, WINDOW_SIDE + 50))
        # Add icon
        icon = pygame.image.load(IMAGE_ICON)
        pygame.display.set_icon(icon)
        # Title
        pygame.display.set_caption(WINDOW_TITLE)

        # Creation of the labyrinth
        self.level = Level('n1')
        self.level.generate()
        self.level.display_level(self.window)

        # Creation of MacGyver
        self.macgy = Person(IMAGE_PERSO, self.level)

        # Creation of the survival items
        self.ether = Tool(IMAGE_ETHER, self.level)
        self.needle = Tool(IMAGE_NEEDLE, self.level)
        self.tube = Tool(IMAGE_TUBE, self.level)

        self.continue_main = 1
        self.continue_game = 1
        self.continue_over = 1
        self.count_survival = 0

    def choose_random(self):
        """Condition to avoid the survival items
        to be localised on the same case """
        while (self.needle.pix_x, self.needle.pix_y) == (self.ether.pix_x, self.ether.pix_y) or \
            (self.needle.pix_x, self.needle.pix_y) == (self.tube.pix_x, self.tube.pix_y) or \
            (self.ether.pix_x, self.ether.pix_y) == (self.tube.pix_x, self.tube.pix_y):

            self.needle.random_pos()
            self.ether.random_pos()
            self.tube.random_pos()

    def collect(self):
        """ If the character MacGyver moves on the same case than a tool:
        - The tool position changes to be out of the labyrinth
        - Variable count_survival to count the nb of items collected """
        if (self.macgy.pix_x, self.macgy.pix_y) == (self.needle.pix_x, self.needle.pix_y):
            (self.needle.pix_x, self.needle.pix_y) = (WINDOW_SIDE - 50, WINDOW_SIDE + 10)
            self.count_survival += 1
        elif (self.macgy.pix_x, self.macgy.pix_y) == (self.ether.pix_x, self.ether.pix_y):
            (self.ether.pix_x, self.ether.pix_y) = (WINDOW_SIDE - 100, WINDOW_SIDE + 10)
            self.count_survival += 1
        elif (self.macgy.pix_x, self.macgy.pix_y) == (self.tube.pix_x, self.tube.pix_y):
            (self.tube.pix_x, self.tube.pix_y) = (WINDOW_SIDE - 150, WINDOW_SIDE + 10)
            self.count_survival += 1

    def game_loop_play(self, window):
        """ GAME-PLAY LOOP
        All the instructions concerning the game before the final condition """
        while self.continue_game:
            pygame.time.Clock().tick(30)

            for event in pygame.event.get():
                # If the user wants to quit:
                # escape button or close window icon
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.continue_main = 0
                    self.continue_game = 0
                    self.continue_over = 0

                elif event.type == KEYDOWN:
                    # Move MacGyver with the arrow keys
                    if event.key == K_RIGHT:
                        self.macgy.move('right')
                    elif event.key == K_LEFT:
                        self.macgy.move('left')
                    elif event.key == K_UP:
                        self.macgy.move('up')
                    elif event.key == K_DOWN:
                        self.macgy.move('down')

                self.collect()

                # Indicate on window the number of survival tool collected
                # Text font choosen
                myfont = pygame.font.SysFont('Arial', 20)
                textsurface = myfont.render('COUNT SURVIVAL TOOL = {}'\
                    .format(self.count_survival), False, (255, 255, 255), (0, 0, 0))

                # Refreshing window
                self.level.display_level(window)
                window.blit(self.macgy.face, (self.macgy.pix_x, self.macgy.pix_y))
                window.blit(self.needle.survival, (self.needle.pix_x, self.needle.pix_y))
                window.blit(self.ether.survival, (self.ether.pix_x, self.ether.pix_y))
                window.blit(self.tube.survival, (self.tube.pix_x, self.tube.pix_y))
                window.blit(textsurface, (WINDOW_SIDE - 420, WINDOW_SIDE + 10))

                pygame.display.flip()

                # Close loop game and loop over will display a picture
                if self.level.structure[self.macgy.case_y][self.macgy.case_x] == 'a':
                    self.continue_game = 0

    def game_loop_over(self, window):
        """GAME-OVER LOOP
        Two possible options when MacGyver is at the arrival case: """
        mes = 0
        while self.continue_over:
            pygame.time.Clock().tick(30)

            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.continue_main = 0
                    self.continue_game = 0
                    self.continue_over = 0

            if self.count_survival == 3:
                message = \
                "Congratalutions, you win! MacGyver sedated the watchman and escaped."
                mes += 1
                win = pygame.image.load(IMAGE_WIN)
                window.blit(win, (0, 0))
                pygame.display.flip()
            else:
                message = \
                "Sorry, you loose... nothing good happened to MacGyver."
                mes += 1
                loose = pygame.image.load(IMAGE_LOOSE)
                window.blit(loose, (0, 0))
                pygame.display.flip()

            if mes == 1:
                print(message)

    def game_loop(self, window):
        """ Main loop of the game with
        the different possible actions and the final condition """
        pygame.key.set_repeat(400, 30)
        while self.continue_main:
            self.game_loop_play(window)
            self.game_loop_over(window)


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
                pix_x = num_case * SPRITE_SIZE
                pix_y = num_line * SPRITE_SIZE
                if sprite == 'w':
                    if count_wall % 2 == 0:
                        window.blit(wallb, (pix_x, pix_y))
                    else:
                        window.blit(wall, (pix_x, pix_y))
                    count_wall += 1
                elif sprite == '0':
                    if count_floor % 5 == 0:
                        window.blit(floorb, (pix_x, pix_y))
                    else:
                        window.blit(floor, (pix_x, pix_y))
                    count_floor += 1
                elif sprite == 'd':
                    window.blit(departure, (pix_x, pix_y))
                elif sprite == 'a':
                    window.blit(arrival, (pix_x, pix_y))
                num_case += 1
            num_line += 1

        self.count_floor = count_floor


class Person:
    """ Class to create a character """

    def __init__(self, face, level):
        """ Initialisation """

        # Sprite of the character
        self.face = pygame.image.load(face)
        # Position of the character, case and pixel
        self.case_x = 0
        self.case_y = 0
        self.pix_x = 0
        self.pix_y = 0
        # Level of the labyrinth
        self.level = level

    def move(self, direction):
        """ Method to allow the movement of the character """

        # Movement on the right
        if direction == 'right':
            # Can't move the character outside the screen
            if self.case_x < (NBR_SPRITE_SIDE - 1):
                # Destination case shouldn't be a wall
                if self.level.structure[self.case_y][self.case_x + 1] != 'w':
                    # Movement +1 case
                    self.case_x += 1
                    # Determination of the real position in pixel
                    self.pix_x = self.case_x * SPRITE_SIZE

        # Movement on the left
        if direction == 'left':
            if self.case_x > 0:
                if self.level.structure[self.case_y][self.case_x - 1] != 'w':
                    self.case_x -= 1
                    self.pix_x = self.case_x * SPRITE_SIZE

        # Movement upward
        if direction == 'up':
            if self.case_y > 0:
                if self.level.structure[self.case_y - 1][self.case_x] != 'w':
                    self.case_y -= 1
                    self.pix_y = self.case_y * SPRITE_SIZE

        # Movement downward
        if direction == 'down':
            if self.case_y < (NBR_SPRITE_SIDE - 1):
                if self.level.structure[self.case_y + 1][self.case_x] != 'w':
                    self.case_y += 1
                    self.pix_y = self.case_y * SPRITE_SIZE


class Tool:
    """ Class to create the survival items """

    def __init__(self, survival, level):
        """ Initialisation """

        # Sprite of the survival tool
        self.survival = pygame.image.load(survival)
        # Position of the tool, case and pixel
        self.case_x = 0
        self.case_y = 0
        self.pix_x = 0
        self.pix_y = 0
        # Level of the labyrinth
        self.level = level


    def random_pos(self):
        """ Method to assign a random position for each tool:
        - Careful, only on the floor cases and not on the wall cases
        - Must add in main file, a condition to avoid that
        the tools position are on start and arrival cases """

        # For each tool generated:
        # - Give a random number, between 0 and the number of case floor-1
        hasard_case = randrange(self.level.count_floor)
        # print(self.level.count_floor, hasard_case)

        # Search and give the real position in the labyrinth structure of
        # the given random case floor.
        num_line = 0
        count = 0
        for line in self.level.structure:
            num_case = 0
            for sprite in line:
                pix_x = num_case * SPRITE_SIZE
                pix_y = num_line * SPRITE_SIZE

                if sprite == '0':
                    if count == hasard_case:
                        self.pix_x = pix_x
                        self.pix_y = pix_y
                    count += 1
                num_case += 1
            num_line += 1
