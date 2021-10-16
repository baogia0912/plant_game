import pygame, time
from settings import *
from Item import Item

class Plant(pygame.Rect):
    """
    an item with the ability to grow when planted
    """
    water_drop = pygame.image.load('graphics/water drop.png')
    plant_item_list = []

    def __init__(self, name, x, y, width, height, image, cycle ,growth_period, rewards ,draging = False, planted = False):
        self.name = name
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
        self.rewards = rewards
        self.plant_item_list.append(self)

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
                self.grass_x = self.x = grass.x 
                self.grass_y = self.y = grass.y
                self.grass_width = self.width = grass.width
                self.grass_height = self.height = grass.height
                grass.planted = True
                return True
        return False


    def draw(self):
        if self.planted:
            screen.blit(pygame.transform.scale(pygame.image.load(self.cycle[self.stage]),(self.grass_width, self.grass_height)), (self.grass_x,self.grass_y))
            if not self.watered and self.stage < len(self.cycle) - 1: 
                
                screen.blit(pygame.transform.scale(self.water_drop, (int(self.water_drop.get_width()/10), int(self.water_drop.get_height()/10))), (self.grass_x+(self.grass_width/2)-(self.water_drop.get_width()/20),self.y-80))

                self.planted_time = time.time()
            
            if time.time() - self.planted_time > self.growth_period and self.stage < len(self.cycle) - 1:

                self.stage += 1
                self.planted_time = time.time()
                self.watered = False
            
            if self.stage == len(self.cycle) - 1 and self.rewards != None:
                for reward in self.rewards:
                    Item(reward, self.x, self.y, self.width, self.height, 'graphics/plant items/'+ self.name + '/reward/' +reward)
                self.rewards = None
                
        else:
            screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x,self.y))