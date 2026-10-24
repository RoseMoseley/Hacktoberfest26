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
    def update(self, ): pass


class Item:
    def __init__(self, pos_x: int, pos_y: int, item_name: str):
        self.__x: int = pos_x
        self.__y: int = pos_y
        self.__item_name: str = item_name
        self.__font = pygame.font.Font("freesansbold.ttf", 32)
        self.__textRender = self.__font.render(self.__item_name, True, (0, 0, 0), (255, 255, 255))
        self.__textRect = self.__textRender.get_rect()
        self.__width = self.__textRect.width
        self.__height = self.__textRect.height

    def getPos(self) -> tuple[int, int]:
        return (self.__x, self.__y)

    def getItemName(self) -> str:
        return self.__item_name

    def getBounds(self) -> tuple[int, int]:
        return (self.__width, self.__height)

    def isItemOverlappingItem(self, otherItem) -> bool:
        otherX, otherY = otherItem.getPos()
        otherWidth, otherHeight = otherItem.getBounds()
        xOverlap = self.__x+self.__width >= otherX and otherX+otherWidth >= self.__x
        yOverlap = self.__y+self.__height >= otherY and otherY+otherHeight >= self.__y
        return xOverlap and yOverlap 

    def drawItem(self, win: pygame.Surface):
        self.__textRect.center = (self.__x, self.__y)
        win.blit(self.__textRender, self.__textRect)