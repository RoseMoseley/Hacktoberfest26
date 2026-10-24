from gui import Display
from goal import get_goal
import pygame

def main():
    lines = []
    with open("common-words.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    starting = get_goal(4,7,lines)
    GUI = Display(starting[0], starting[1])
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                GUI.scroll(event)
        GUI.doLogic()
        GUI.updateAll()
    pygame.quit()

if __name__ == "__main__":
    main()