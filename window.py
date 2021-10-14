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
mouse_busy = False

plant_item_list = []
movable_item_list = []
static_item_list = []

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
        movable_item_list.append(self)

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x, self.y))

    def update_offset(self, pos):
        self.offset_x = self.x - pos[0]
        self.offset_y = self.y - pos[1]

    def update_coord(self, pos):
        self.x = pos[0] + self.offset_x
        self.y = pos[1] + self.offset_y

class Plant(pygame.Rect):
    """
    an item with the ability to grow when planted
    """
    def __init__(self, x, y, width, height, image, cycle ,growth_period, reward ,draging = False, planted = False):
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
        self.reward = reward
        plant_item_list.append(self)

    def update_offset(self, pos):
        self.offset_x = self.x - pos[0]
        self.offset_y = self.y - pos[1]

    def update_coord(self, pos):
        self.x = pos[0] + self.offset_x
        self.y = pos[1] + self.offset_y

    def planted_on_grass(self, grass):
        if self.colliderect(grass):
            if not grass.planted:
                self.planted = True
                self.grass_x = grass.x 
                self.grass_y = grass.y
                self.grass_width = grass.width
                self.grass_height = grass.height
                grass.planted = True
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
            
            if self.stage == len(self.cycle) - 1 and self.reward != None:
                Item(self.x, self.y, self.width, self.height, self.reward)
                self.reward = None
                

        else:
            screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x,self.y))

class Grass(pygame.Rect):
    def __init__(self, x, y, width, height, image, draging = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.planted = False
        static_item_list.append(self)

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x, self.y))

    
def launch_game(running):

    #declare ingame variable
    global screen_width, screen_height, mouse_busy

    with open('game items/movable items.txt', "r") as movable_item_file:
        lines = movable_item_file.readlines()
        for line in lines:
            Item(int(line.split(', ')[1]), int(line.split(', ')[2]), int(line.split(', ')[3]), int(line.split(', ')[4]), 'graphics/movable items/'+line.split(', ')[0]+'.png')

    with open('game items/static items.txt',"r") as static_item_file:
        lines = static_item_file.readlines()
        for line in lines:
            Grass(int(line.split(', ')[1]), int(line.split(', ')[2]), int(line.split(', ')[3]), int(line.split(', ')[4]), 'graphics/static items/'+line.split(', ')[0]+'.png')

    with open('game items/plant items.txt',"r") as static_item_file:
        lines = static_item_file.readlines()
        for line in lines:
            Plant(int(line.split(', ')[1]), int(line.split(', ')[2]), int(line.split(', ')[3]), int(line.split(', ')[4]), int(line.split(', ')[5]), 'graphics/plant items/'+line.split(', ')[0]+'.png')


    #plants item
    acorn = Plant(0, 0, 100, 100, 'graphics/acorn.png', [acorn1, acorn2, acorn3, acorn4, acorn5], 2, 'graphics/wood sword.png')
    reverse_acorn = Plant(0, 0, 100, 100, 'graphics/acorn.png', [acorn5, acorn4, acorn3, acorn2, acorn1], 2, 'graphics/wood sword.png')

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
                        if not plant.planted and mouse_busy == False:
                            if plant.collidepoint(event.pos):
                                plant.draging = True
                                plant.update_offset(event.pos)
                                mouse_busy = True


                    #detect clicking on all movable items 
                    for item in movable_item_list:
                        if item.collidepoint(event.pos) and mouse_busy == False:
                            item.draging = True
                            item.update_offset(event.pos)
                            mouse_busy = True
                    

            #handle mouse up
            elif event.type == pygame.MOUSEBUTTONUP:
                #left click
                if event.button == 1:
                    
                    #handle stop moving plant items and check if planted on grass or is watered
                    for plant in plant_item_list:

                        if not plant.planted:
                            plant.planted_on_grass(static_item_list[0])
                        plant.draging = False

                        if not plant.watered:
                            if plant.colliderect(movable_item_list[0]):
                                plant.watered = True


                    #handle stop moving all movable items
                    for item in movable_item_list:
                        item.draging = False
                    
                    mouse_busy = False

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

        for grass in static_item_list:
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