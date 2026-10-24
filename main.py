from gui import display
import pygame

GUI = display(["1", "2", "3", "4"])
running = True
clock = pygame.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
    GUI.updateAll()