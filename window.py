import pygame, sys
from pygame.locals import *
from pygame import color, surface
#make 2 boxes 1 big 1small big cant move small move with mouse
screen_width = 1000
screen_height = 700
backgound_color = (102, 51, 0) #brown
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

def main():
    pygame.display.set_caption('plant game')
    screen.fill(backgound_color)
    launch_game(True)


    
def launch_game(running):
    global screen_width, screen_height
    light_blue_box = pygame.Rect(screen_width/2 - 100, screen_height/2 - 100, 200, 200)
    pygame.draw.rect(screen, (0, 255, 255), light_blue_box)
    red_box =  pygame.Rect(0, 0, 100, 100)
    pygame.draw.rect(screen, (255, 0, 0),red_box)
    rectangle_draging = False
    while running:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen.fill(backgound_color)
                screen_width, screen_height = pygame.display.get_surface().get_size()
                light_blue_box = pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(screen_width/2 - 100, screen_height/2 - 100, 200, 200))
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    if red_box.collidepoint(event.pos):
                        rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = red_box.x - mouse_x
                        offset_y = red_box.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    rectangle_draging = False

            elif event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    red_box.x = mouse_x + offset_x
                    red_box.y = mouse_y + offset_y

            if event.type == pygame.QUIT:
                running = False


        screen.fill(backgound_color)
        pygame.draw.rect(screen, (0, 255, 255), light_blue_box)
        pygame.draw.rect(screen, (255, 0, 0), red_box)
       
        pygame.display.flip()

if __name__ == '__main__':
    main()