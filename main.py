from gui import Display
import pygame

GUI = Display(["1", "2", "3", "4"])
running = True
clock = pygame.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    GUI.updateAll()
pygame.quit()