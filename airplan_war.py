# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display. set_caption('Airplane Wars') 
# Load the background map
background = pygame.image.load('resources/image/background.png')



# Load the picture of the plane
plane_img = pygame.image.load('resources/image/shoot.png')
# Select the position of the plane in the big picture, generate subsurface, and then initialize the position of the plane.
player_rect = pygame.Rect(0, 99, 102, 126)
player = plane_img.subsurface(player_rect)
player_pos = [200, 600]


clock = pygame.time.Clock()
running = True
while running:

    # Contrôlez la fréquence d'images maximale du jeu
    clock.tick(45)

    # Draw the background
    screen.fill (0)
    screen.blit (background, (0, 0))

    # Draw an airplane
    screen.blit (player, player_pos)

    # Update the screen
    pygame.display.update()

    # Process game exits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

