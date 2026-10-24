import pygame

'''
main display -> pygame screen
    item nodes -> updateing only relevant part of the screen
    adding new things from options
    clearing screen of items
    init initial items
    return items to be merged <- only if they have been dropped on top of each other
    ^- can handlemoving over each other without merging
    side bar (scrollable) of all discovered item -> creates and distroys nodes

item node
    pygame surface
    text

'''

class display():
    '''
    The main display
    
    Has a list of discorvered nodes to be able to add
    '''
    #list of colours for the gui
    colours = {"bg":(255,255,255)}
    def __init__(self, initial:list[str]):
        '''
        initialisation of the dislay object
        
        args:
            initial list[str]: list of the words that are provided to start with
        '''
        #init pygame
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=(1028,512))

        self.known_items = initial # list of all items that have been discovered
        self.placed_items = []

    def update_all(self):
        '''
        redraw the entier screen and run pygame.display.update
        '''
        self.screen.fill(self.colours["bg"])
        for p_item in self.placed_items:
            self.screen.blit(p_item.get_screen(), p_item.get_location()) # update to matching getters

        for num, k_item in enumerate(self.known_items):
            this_item = item.init()

        pygame.display.update()