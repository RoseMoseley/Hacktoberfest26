from gui import Display
import pygame

def main():
    lines = []
    with open("common-words.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    GUI = Display(lines)
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