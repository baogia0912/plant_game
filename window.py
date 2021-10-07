import pygame, sys
from pygame.locals import *
#make the window bigger with fullscreen function
backgound_colour = (255, 255, 255)
screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
pygame.display.set_caption('plant game')
screen.fill((102, 51, 0))
pygame.display.flip()
running = True
while running:

    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            screen.fill((102, 51, 0))

        if event.type == pygame.QUIT:
            running = False
        
    pygame.display.update()



