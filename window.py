#get needed libraries
import pygame, sys, time
from pygame import image
from pygame.locals import *
from pygame import color, init, surface

#declare global variable
screen_width = 1000
screen_height = 700
backgound_color = (102, 51, 0) #brown
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

acorn1 = pygame.image.load('graphics/stage 1.png')
acorn2 = pygame.image.load('graphics/stage 2.png')
acorn3 = pygame.image.load('graphics/stage 3.png')
acorn4 = pygame.image.load('graphics/stage 4.png')
acorn5 = pygame.image.load('graphics/stage 5.png')

water_drop = pygame.image.load('graphics/water drop.png')

#making classes
class Item(pygame.Rect):
    """
    make an item that can draw itself and have option to move with mouse
    """
    def __init__(self, x, y, width, height, image, draging = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.draging = draging
        self.offset_x = 0 
        self.offset_y = 0

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x, self.y))

    def update_offset(self, pos):
        self.offset_x = self.x - pos[0]
        self.offset_y = self.y - pos[1]

    def update_coord(self, pos):
        self.x = pos[0] + self.offset_x
        self.y = pos[1] + self.offset_y

class Plant(Item):
    """
    an item with the ability to grow when planted
    """
    def __init__(self, x, y, width, height, image, cycle ,growth_period ,draging = False, planted = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.cycle = cycle
        self.draging = draging
        self.offset_x = 0 
        self.offset_y = 0
        self.planted = planted
        self.planted_time = 0
        self.grass_x = None
        self.grass_y = None
        self.grass_width = None
        self.grass_height = None
        self.stage = 0
        self.growth_period = growth_period
        self.watered = False

    def planted_on_grass(self, grass):
        if self.colliderect(grass):
            self.planted = True
            self.grass_x = grass.x 
            self.grass_y = grass.y
            self.grass_width = grass.width
            self.grass_height = grass.height
            return True
        return False


    def draw(self):
        if self.planted:
            screen.blit(pygame.transform.scale(self.cycle[self.stage],(self.grass_width, self.grass_height)), (self.grass_x,self.grass_y))
            if not self.watered and self.stage < len(self.cycle) - 1: 
                
                screen.blit(pygame.transform.scale(water_drop, (int(water_drop.get_width()/10), int(water_drop.get_height()/10))), (self.grass_x+(self.grass_width/2)-(water_drop.get_width()/20),self.y-80))

                self.planted_time = time.time()
            
            if time.time() - self.planted_time > self.growth_period and self.stage < len(self.cycle) - 1:

                self.stage += 1
                self.planted_time = time.time()
                self.watered = False
                    
            

        else:
            screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x,self.y))




    
def launch_game(running):

    #declare ingame variable
    global screen_width, screen_height

    #static item
    grass = Item(screen_width/2 - 100, screen_height/2 - 100, 200, 200, "graphics/grass.jpeg")

    #plants item
    acorn = Plant(0, 0, 100, 100, 'graphics/acorn.png', [acorn1, acorn2, acorn3, acorn4, acorn5], 5)
    reversed_acorn = Plant(0, 200, 100, 100, 'graphics/acorn.png', [acorn5, acorn4, acorn3, acorn2, acorn1], 2)

    #movable item
    water = Item(0, 100, 100, 100, "graphics/watering can.png")

    #lists to seperate item types
    plant_item_list = [acorn, reversed_acorn]
    movable_item_list = [water]
    static_item_list = [grass]


    #game starts here
    while running:

        #hadle ingame events (mouse and keyboard input)
        for event in pygame.event.get():
            
            #resize window
            if event.type == VIDEORESIZE:
                screen.fill(backgound_color)
                screen_width, screen_height = pygame.display.get_surface().get_size()
            
            #handle mouse down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if event.button == 1:
                    
                    #detect clicking on all plant items 
                    for plant in plant_item_list:
                        if not plant.planted:
                            if plant.collidepoint(event.pos):
                                plant.draging = True
                                plant.update_offset(event.pos)

                        
                    
                    #detect clicking on all movable items 
                    for item in movable_item_list:
                        if item.collidepoint(event.pos):
                            item.draging = True
                            item.update_offset(event.pos)

            #handle mouse up
            elif event.type == pygame.MOUSEBUTTONUP:
                #left click
                if event.button == 1:
                    
                    #handle stop moving plant items and check if planted on grass or is watered
                    for plant in plant_item_list:

                        if not plant.planted:
                            plant.planted_on_grass(grass)
                        plant.draging = False

                        if not plant.watered:
                            if plant.colliderect(water):
                                plant.watered = True

                    #handle stop moving all movable items
                    for item in movable_item_list:
                        item.draging = False

            #handle mouse motion
            elif event.type == pygame.MOUSEMOTION:

                #handle move all plant items
                for plant in plant_item_list:
                    if plant.draging:
                        plant.update_coord(event.pos)

                #handle move all normal items
                for item in movable_item_list:
                    if item.draging:
                        item.update_coord(event.pos)
            
            #close window
            if event.type == pygame.QUIT:
                running = False

        #refill background with color
        screen.fill(backgound_color)

        # draw all items in list
        grass.draw()

        for plant in plant_item_list:
            plant.draw()
        
        for item in movable_item_list:
            item.draw()

        #update everything on screen 
        pygame.display.flip()

def main():
    #game window caption
    pygame.display.set_caption('plant game')
    launch_game(True)

if __name__ == '__main__':
    main()