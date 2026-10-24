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

#list of colours for the gui
COLOURS = {
    "bg":(255,255,255),
    "text_bg":(200,200,200),
    "text_clr":(0, 0, 0)
}

class Display():
    '''
    The main display
    
    Has a list of discorvered nodes to be able to add
    '''

    def __init__(self, initial:list[str]):
        '''
        initialisation of the dislay object
        
        args:
            initial list[str]: list of the words that are provided to start with
        '''
        #init pygame
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(size=(1028,512))

        self.known_items = initial # list of all items that have been discovered
        self.placed_items = []

        clear = lambda x : []
        self.buttons = [Button(5,5,"Clear",clear)]

    def updateAll(self):
        '''
        redraw the entier screen and run pygame.display.update
        '''
        self.screen.fill(COLOURS["bg"])
        for item in self.placed_items:
            item.drawItem(self.screen)

        for num, item_name in enumerate(self.known_items):
            item = Item(self.screen.get_size()[0]-100, num*20+5, item_name)
            item.drawItem(self.screen)

        for button in self.buttons:
            button.drawItem(self.screen)

        pygame.display.update()

class Object():
    def __init__(self, pos_x: int, pos_y: int, item_name: str):
        self.__x: int = pos_x
        self.__y: int = pos_y
        self.__item_name: str = item_name
        self.__font = pygame.font.Font("freesansbold.ttf", 32)
        self.__textRender = self.__font.render(self.__item_name, True, COLOURS["text_clr"], COLOURS["text_bg"])
        self.__textRect = self.__textRender.get_rect()
        self.__width = self.__textRect.width
        self.__height = self.__textRect.height

    def getPos(self) -> tuple[int, int]:
        '''
        Return a tuple of this item's position (x, y), this is the centre of the text 
        '''
        return (self.__x, self.__y)

    def getItemName(self) -> str:
        '''
        Get the item's name, this is what should be fed into the merger
        '''
        return self.__item_name

    def getBounds(self) -> tuple[int, int]:
        '''
        Return a tuple of this item's bounds (width, height)
        '''
        return (self.__width, self.__height)

    def drawItem(self, win: pygame.Surface):
        '''
        Given a pygame screen this will render the item box to it
        '''
        self.__textRect.center = (self.__x, self.__y)
        win.blit(self.__textRender, self.__textRect)

class Item(Object):
    def __init__(self, pos_x, pos_y, item_name):
        super().__init__(pos_x, pos_y, item_name)

    def isItemOverlappingItem(self, otherItem) -> bool:
        '''
        Given another item, determins if the items are overlapping or not
        '''
        otherX, otherY = otherItem.getPos()
        otherWidth, otherHeight = otherItem.getBounds()
        xOverlap = self.__x+self.__width//2 >= otherX-otherWidth//2 and otherX+otherWidth//2 >= self.__x-self.__width//2
        yOverlap = self.__y+self.__height//2 >= otherY-otherHeight//2 and otherY+otherHeight//2 >= self.__y-self.__height//2
        return xOverlap and yOverlap 

    def isPointOverlappingItem(self, point: tuple[int, int]) -> bool:
        '''
        Returns if a point is overlapping the item (this should be used for checking if the mouse is on an item)
        '''
        xOverlap = point[0]>=self.__x-self.__width//2 and point[0]<=self.__x+self.__width//2
        yOverlap = point[1]>=self.__y-self.__height//2 and point[1]<=self.__y+self.__height//2
        return xOverlap and yOverlap

class Button(Object):
    def __init__(self, pos_x, pos_y, item_name, action):
        super().__init__(pos_x, pos_y, item_name)
        self.__action = action

    def getAction(self):
        return self.__action

if __name__ == "__main__":
    disp = Display(["a","b","c"])
    disp.updateAll()
    input()