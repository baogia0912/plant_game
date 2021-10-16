#get needed libraries
import pygame, sys, time, os
from pygame import image
from pygame.locals import *
from pygame import color, init, surface
from settings import *
from Item import Item
from Plant import Plant
from Grass import Grass

    
def launch_game(running):

    #declare ingame variable
    mouse_busy = False

    with open('game items/movable items.txt', "r") as movable_item_file:
        lines = movable_item_file.readlines()
        for line in lines:
            if line.split(', ')[0]+'.png' not in os.listdir('graphics/movable items/'):
                open('graphics/movable items/'+line.split(', ')[0]+'.png', 'wb')
            else:
                Item(line.split(', ')[0],
                    int(line.split(', ')[1]), 
                    int(line.split(', ')[2]), 
                    int(line.split(', ')[3]), 
                    int(line.split(', ')[4]), 
                    'graphics/movable items/'+line.split(', ')[0]+'.png'
                )
    watering_can = Item.movable_item_list[0]

    with open('game items/static items.txt',"r") as static_item_file:
        lines = static_item_file.readlines()
        for line in lines:
            Grass(int(line.split(', ')[1]), 
                int(line.split(', ')[2]), 
                int(line.split(', ')[3]), 
                int(line.split(', ')[4]), 
                'graphics/static items/'+line.split(', ')[0]+'.png'
            )

    with open('game items/plant items.txt',"r") as static_item_file:
        lines = static_item_file.readlines()
        for line in lines:
            if line.split(', ')[0] not in os.listdir('graphics/plant items/'):
                os.mkdir('graphics/plant items/'+line.split(', ')[0])
                f=open('graphics/plant items/'+line.split(', ')[0]+'/'+line.split(', ')[0]+'.png', 'wb')
                f.write((0, 0, 0, 0))
                os.mkdir('graphics/plant items/'+line.split(', ')[0]+'/cycle/')
                open('graphics/plant items/'+line.split(', ')[0]+'/cycle/stage 1.png', 'wb')
                os.mkdir('graphics/plant items/'+line.split(', ')[0]+'/reward/')
                open('graphics/plant items/'+line.split(', ')[0]+'/reward/reward.png', 'wb')

            else:  
                Plant(line.split(', ')[0], 
                    int(line.split(', ')[1]), 
                    int(line.split(', ')[2]), 
                    int(line.split(', ')[3]), 
                    int(line.split(', ')[4]), 
                    'graphics/plant items/'+line.split(', ')[0]+'/'+line.split(', ')[0]+'.png', 
                    ['graphics/plant items/'+line.split(', ')[0]+'/cycle/'+stage for stage in sorted(os.listdir('graphics/plant items/'+line.split(', ')[0]+'/cycle/'))],
                    int(line.split(', ')[5]),
                    os.listdir('graphics/plant items/'+line.split(', ')[0]+'/reward/')
                )

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
                    for plant in Plant.plant_item_list:
                        if not plant.planted and mouse_busy == False:
                            if plant.collidepoint(event.pos):
                                plant.draging = True
                                plant.update_offset(event.pos)
                                mouse_busy = True


                    #detect clicking on all movable items 
                    for item in Item.movable_item_list:
                        if item.collidepoint(event.pos) and mouse_busy == False:
                            item.draging = True
                            item.update_offset(event.pos)
                            mouse_busy = True
                    

            #handle mouse up
            elif event.type == pygame.MOUSEBUTTONUP:
                #left click
                if event.button == 1:
                    
                    #handle stop moving plant items and check if planted on grass or is watered
                    for plant in Plant.plant_item_list:

                        if not plant.planted:
                            plant.planted_on_grass(Grass.static_item_list[0])
                        plant.draging = False

                        if not plant.watered:
                            if plant.colliderect(watering_can):
                                plant.watered = True


                    #handle stop moving all movable items
                    for item in Item.movable_item_list:
                        item.draging = False
                    
                    mouse_busy = False

            #handle mouse motion
            elif event.type == pygame.MOUSEMOTION:

                #handle move all plant items
                for plant in Plant.plant_item_list:
                    if plant.draging:
                        plant.update_coord(event.pos)

                #handle move all normal items
                for item in Item.movable_item_list:
                    if item.draging:
                        item.update_coord(event.pos)
            
            #close window
            if event.type == pygame.QUIT:
                running = False

        #refill background with color
        screen.fill(backgound_color)

        for grass in Grass.static_item_list:
            grass.draw()

        for plant in Plant.plant_item_list:
            plant.draw()
        
        for item in Item.movable_item_list:
            item.draw()

        #update everything on screen 
        pygame.display.flip()

def main():
    #game window caption
    pygame.display.set_caption('plant game')
    launch_game(True)

if __name__ == '__main__':
    main()