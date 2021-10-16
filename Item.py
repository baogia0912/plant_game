import pygame
from settings import *

class Item(pygame.Rect):
    """
    make an item that can draw itself and have option to move with mouse
    """
    movable_item_list = []

    def __init__(self, name, x, y, width, height, image, draging = False):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.draging = draging
        self.offset_x = 0 
        self.offset_y = 0
        self.movable_item_list.append(self)

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x, self.y))

    def update_offset(self, pos):
        self.offset_x = self.x - pos[0]
        self.offset_y = self.y - pos[1]

    def update_coord(self, pos):
        self.x = pos[0] + self.offset_x
        self.y = pos[1] + self.offset_y