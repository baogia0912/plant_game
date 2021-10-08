import pygame, sys, time
from pygame.locals import *
from pygame import color, surface

screen_width = 1000
screen_height = 700
backgound_color = (102, 51, 0) #brown
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

acorn1 = pygame.image.load('graphics/stage 1.png')
acorn2 = pygame.image.load('graphics/stage 2.png')
acorn3 = pygame.image.load('graphics/stage 3.png')
acorn4 = pygame.image.load('graphics/stage 4.png')
acorn5 = pygame.image.load('graphics/stage 5.png')

water_droplet = pygame.image.load('graphics/water_droplet.png')

def main():
    pygame.display.set_caption('plant game')
    screen.fill(backgound_color)
    launch_game(True)

    
def launch_game(running):
    global screen_width, screen_height

    light_blue_box = pygame.Rect(screen_width/2 - 100, screen_height/2 - 100, 200, 200)
    pygame.draw.rect(screen, (0, 255, 255), light_blue_box)

    red_box = pygame.Rect(0, 0, 100, 100)
    pygame.draw.rect(screen, (255, 0, 0),red_box)

    blue_box = pygame.Rect(0, 100, 100, 100)
    pygame.draw.rect(screen, (0, 0, 255),blue_box)

    rectangle_draging = False
    while running:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen.fill(backgound_color)
                screen_width, screen_height = pygame.display.get_surface().get_size()
                light_blue_box = pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(screen_width/2 - 100, screen_height/2 - 100, 200, 200))
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if blue_box.collidepoint(event.pos):
                        rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = blue_box.x - mouse_x
                        offset_y = blue_box.y - mouse_y

                    if red_box.collidepoint(event.pos):
                        rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = red_box.x - mouse_x
                        offset_y = red_box.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if light_blue_box.colliderect(red_box):
                        red_box = None
                        growing = time.time()
                        index = 0
                    rectangle_draging = False

            elif event.type == pygame.MOUSEMOTION:

                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    blue_box.x = mouse_x + offset_x
                    blue_box.y = mouse_y + offset_y

                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    red_box.x = mouse_x + offset_x
                    red_box.y = mouse_y + offset_y

            if event.type == pygame.QUIT:
                running = False


        screen.fill(backgound_color)
        screen.blit(pygame.transform.scale(pygame.image.load('graphics/grass.jpeg'), (light_blue_box.width, light_blue_box.height)), (light_blue_box.x, light_blue_box.y))
        screen.blit(pygame.transform.scale(pygame.image.load('graphics/water_droplet.png'), (blue_box.width, blue_box.height)), (blue_box.x, blue_box.y))
        if red_box != None:
            screen.blit(pygame.transform.scale(pygame.image.load('graphics/acorn.png'), (red_box.width, red_box.height)), (red_box.x,red_box.y))
        else:
            if time.time() - growing > 3 and index < 4: 
                growing = time.time()
                index += 1
            screen.blit(pygame.transform.scale([acorn1, acorn2, acorn3, acorn4, acorn5][index],(light_blue_box.width, light_blue_box.height)), (light_blue_box.x,light_blue_box.y))

        pygame.display.flip()

if __name__ == '__main__':
    main()