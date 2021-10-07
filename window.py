import pygame
#make the window bigger with fullscreen function
backgound_colour = (255, 255, 255)
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('plant game')
screen.fill((102, 51, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

