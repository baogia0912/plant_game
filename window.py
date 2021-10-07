import pygame, sys
from pygame.locals import *
#make 2 boxes 1 big 1small big cant move small move with mouse

backgound_colour = (102, 51, 0) #brown

def main():
    screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
    pygame.display.set_caption('plant game')
    screen.fill(backgound_colour)
    launch_game(True)

    
def launch_game(running):

    while running:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen.fill(backgound_colour)

            if event.type == pygame.QUIT:
                running = False
            
        pygame.display.update()

if __name__ == '__main__':
    main()