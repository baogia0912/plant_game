import pygame
from settings import *

class Grass(pygame.Rect):
    static_item_list = []

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.planted = False
        self.static_item_list.append(self)

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height)), (self.x, self.y))