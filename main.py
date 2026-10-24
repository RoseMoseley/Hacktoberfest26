from gui import Display
import pygame

def main():
    GUI = Display([str(x) for x in range(100)])
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