import pygame, sys, time
from pygame import image
from pygame.locals import *
from pygame import color, init, surface

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

class item(pygame.Rect):
    def __init__(self, x, y, width, height, image, draging = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.draging = draging

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x, self.y))



# acorn = item(0,100,100,100,'graphics/acorn.png')

# acorn.draw()


def main():
    pygame.display.set_caption('plant game')
    screen.fill(backgound_color)
    launch_game(True)

    
def launch_game(running):
    global screen_width, screen_height

    grass = item(screen_width/2 - 100, screen_height/2 - 100, 200, 200, "graphics/grass.jpeg")

    red_box = pygame.Rect(0, 0, 100, 100)
    pygame.draw.rect(screen, (255, 0, 0),red_box)

    blue_box = pygame.Rect(0, 100, 100, 100)
    pygame.draw.rect(screen, (0, 0, 255),blue_box)

    acorn_draging = False
    water_draging = False
    while running:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen.fill(backgound_color)
                screen_width, screen_height = pygame.display.get_surface().get_size()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if blue_box.collidepoint(event.pos):
                        water_draging = True
                        mouse_x, mouse_y = event.pos
                        water_offset_x = blue_box.x - mouse_x
                        water_offset_y = blue_box.y - mouse_y

                    if red_box != None:
                        if red_box.collidepoint(event.pos):
                            acorn_draging = True
                            mouse_x, mouse_y = event.pos
                            acorn_offset_x = red_box.x - mouse_x
                            acorn_offset_y = red_box.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if red_box != None:
                        if grass.colliderect(red_box):
                            red_box = None
                            growing = time.time()
                            index = 0
                    acorn_draging = False
                    water_draging = False

            elif event.type == pygame.MOUSEMOTION:

                if acorn_draging:
                    mouse_x, mouse_y = event.pos
                    red_box.x = mouse_x + acorn_offset_x
                    red_box.y = mouse_y + acorn_offset_y

                if water_draging:
                    mouse_x, mouse_y = event.pos
                    blue_box.x = mouse_x + water_offset_x
                    blue_box.y = mouse_y + water_offset_y

            if event.type == pygame.QUIT:
                running = False


        screen.fill(backgound_color)
        grass.draw()
        if red_box != None:
            screen.blit(pygame.transform.scale(pygame.image.load('graphics/acorn.png'), (red_box.width, red_box.height)), (red_box.x,red_box.y))
        else:
            if time.time() - growing > 3 and index < 4: 
                growing = time.time()
                index += 1
            screen.blit(pygame.transform.scale([acorn1, acorn2, acorn3, acorn4, acorn5][index],(grass.width, grass.height)), (grass.x,grass.y))
        screen.blit(pygame.transform.scale(pygame.image.load('graphics/water_droplet.png'), (blue_box.width, blue_box.height)), (blue_box.x, blue_box.y))

        pygame.display.flip()

if __name__ == '__main__':
    main()