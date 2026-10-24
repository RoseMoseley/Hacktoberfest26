import pygame
from copy import copy
from merger import merge_items

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
    "bg":(255,255,255), # Display window colour
    "bg2":(248,250,252), # Object bg colour
    "bg3":(241,245,249), # Sidebar colour
    "txt":(15,23,42), # text colour
    "out":(71,85,105), # Object outline
    "hi":(37,99,235), #highlight
    "hi2":(29,78,216) # second highlight
    }

#size of the bar containing all found items
SIDEBARSIZE = 205
SCROLLBARSIZE = 10

class Display():
    '''
    The main display
    
    Has a list of discorvered nodes to be able to add
    '''

    __known_item_spacing = 32

    def __init__(self, initial:list[str], goal: str):
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

        self.known_items = [] # list of all items that have been discovered
        self.placed_items = []
        self.current_dragged_item = None
        self.holding_left_click = False
        self.holding_scroll_bar = False
        self.goal = goal

        self.buttons = [Button(5,5,"Clear",lambda btn: self.clearItems())]
        for num, item_name in enumerate(initial):
            self.known_items.append(Button(self.screen.get_size()[0]-SIDEBARSIZE, num*20+5, item_name, lambda btn: self.add_item(btn.getItemName())))

        #set the scroll amount
        self.__scroll_count = 0
        self.__scroll_bar_rect = pygame.Rect(self.screen.get_size()[0]-SCROLLBARSIZE, 0, SCROLLBARSIZE, self.screen.get_size()[1])

        # goal text
        self.goalFont = pygame.font.Font("freesansbold.ttf", 24)
        self.hasGoal = False

    def clearItems(self):
        self.placed_items = []

    def isHoveringScrollbar(self, point) -> bool:
        '''
        Is the user hovering the scroll_bar
        '''
        x, y = self.__scroll_bar_rect.x, self.__scroll_bar_rect.y
        width, height = self.__scroll_bar_rect.width, self.__scroll_bar_rect.height
        xOverlap = point[0]>=x and point[0]<=x+width
        yOverlap = point[1]>=y and point[1]<=y+height
        return xOverlap and yOverlap

    def doLogic(self):
        '''
        This processes the logic of the game
        '''
        scroll_bar_height = max(min(self.screen.get_size()[1]/(len(self.known_items)*self.__known_item_spacing), 1), 0)*self.screen.get_size()[1]
        self.__scroll_bar_rect = pygame.Rect(
            self.screen.get_size()[0]-SCROLLBARSIZE, 
            (self.screen.get_size()[1]-scroll_bar_height)*self.__scroll_count/(len(self.known_items) - self.screen.get_size()[1] // self.__known_item_spacing), 
            SCROLLBARSIZE, 
            scroll_bar_height
            )

        mousePos = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0] and not self.holding_left_click:
            self.holding_left_click = True
            click = True
            if self.isHoveringScrollbar(mousePos):
                self.holding_scroll_bar = True
        elif not pygame.mouse.get_pressed()[0] and self.holding_left_click:
            self.holding_left_click = False
            self.holding_scroll_bar = False
        if self.holding_scroll_bar and self.screen.get_size()[1]-self.__scroll_bar_rect.height > 0:
            self.__scroll_bar_rect = pygame.Rect(self.__scroll_bar_rect.x, min(max(mousePos[1], 0), self.screen.get_size()[1]-self.__scroll_bar_rect.height), self.__scroll_bar_rect.width, self.__scroll_bar_rect.height)
            self.__scroll_count = (self.__scroll_bar_rect.y/(self.screen.get_size()[1]-self.__scroll_bar_rect.height))*(len(self.known_items) - self.screen.get_size()[1] // self.__known_item_spacing)
        elif click:
            if self.current_dragged_item is None:
                for button in self.buttons:
                    if button.isPointOverlappingObj(mousePos):
                        print(f"CLICKED {button.getItemName()}")
                        button.getAction()(button)
                        return # Upon pressing a button ignore the rest of the logic to prevent issues
                for button in self.known_items:
                    if button.isPointOverlappingObj(mousePos):
                        print(f"CLICKED {button.getItemName()}")
                        button.getAction()(button)
                        return # Upon pressing a button ignore the rest of the logic to prevent issues
                for item in self.placed_items:
                    if item.isPointOverlappingObj(mousePos):
                        self.current_dragged_item = item
                        break
            else:
                for item in self.placed_items:
                    if item == self.current_dragged_item:
                        continue
                    if item.isObjOverlappingObj(self.current_dragged_item):
                        merged_item_name = merge_items(item.getItemName(), self.current_dragged_item.getItemName())
                        new_item = Item(item.getPos()[0], item.getPos()[1], merged_item_name)
                        self.placed_items.append(new_item)
                        self.placed_items.remove(item)
                        self.placed_items.remove(self.current_dragged_item)
                        if merged_item_name == self.goal:
                            self.hasGoal = True
                        found = False
                        for known in self.known_items:
                            if known.getItemName() == merged_item_name:
                                found = True
                                break
                        if not found:
                            self.known_items.append(Button(self.screen.get_size()[0]-SIDEBARSIZE, 0, merged_item_name, lambda btn: self.add_item(btn.getItemName())))
                        break 
                if self.current_dragged_item.getPos()[0] > self.screen.get_size()[0]-SIDEBARSIZE:
                    print("Removed")
                    self.placed_items.remove(self.current_dragged_item)
                self.current_dragged_item = None
        if self.current_dragged_item is not None:
            self.current_dragged_item.setPos(mousePos[0], mousePos[1])

    def updateAll(self):
        '''
        redraw the entier screen and run pygame.display.update
        '''
        self.screen.fill(COLOURS["bg"])

        pygame.draw.rect(self.screen, COLOURS["bg3"], (self.screen.get_size()[0]-SIDEBARSIZE,0,SIDEBARSIZE,self.screen.get_size()[1]))
        
        for item in self.placed_items:
            item.drawItem(self.screen)

        for num, button in enumerate(self.known_items):
            button.setPos(self.screen.get_size()[0]-SIDEBARSIZE+5, (num-self.__scroll_count)*self.__known_item_spacing+5)
            button.drawItem(self.screen)

        for button in self.buttons:
            button.drawItem(self.screen)

        self.goalFont.set_strikethrough(self.hasGoal)
        render = self.goalFont.render(self.goal, True, COLOURS["txt"])
        render_rect = render.get_rect()
        render_rect.bottomleft = (0, self.screen.get_size()[1])
        self.screen.blit(render, render_rect)

        pygame.draw.rect(self.screen, COLOURS["out"], self.__scroll_bar_rect)

        pygame.display.update()

    def add_item(self, item_name):
        new_item = Item(0, 0, item_name)
        self.placed_items.append(new_item)
        self.current_dragged_item = new_item

    def scroll(self, event:pygame.event.Event):
        if event.type != pygame.MOUSEWHEEL:
            return

        if event.y == 1 and self.__scroll_count > 0:
            self.__scroll_count -= 1
        elif event.y == -1 and self.__scroll_count < len(self.known_items) - self.screen.get_size()[1] // self.__known_item_spacing:
            self.__scroll_count += 1

class Object():
    def __init__(self, pos_x: int, pos_y: int, item_name: str):
        self.__x: int = pos_x
        self.__y: int = pos_y
        self.__item_name: str = item_name
        self.__font = pygame.font.Font("freesansbold.ttf", 24)
        self.__textRender = self.__font.render(self.__item_name, True, COLOURS["txt"])
        self.__textRect = self.__textRender.get_rect()
        self.__width = self.__textRect.width
        self.__height = self.__textRect.height
        self.__background = pygame.Surface((self.__width+4, self.__height+4))

        self.__background.fill(COLOURS["out"])
        pygame.draw.rect(self.__background, COLOURS["bg2"], (1,1,self.__background.get_size()[0]-2, self.__background.get_size()[1]-2))
        self.__background.blit(self.__textRender, (2,2))

    def getPos(self) -> tuple[int, int]:
        '''
        Return a tuple of this item's position (x, y), this is the topleft of the text 
        '''
        return (self.__x, self.__y)

    def setPos(self, pos_x: int, pos_y: int):
        self.__x = pos_x
        self.__y = pos_y

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
        self.__textRect.topleft = (self.__x, self.__y)
        win.blit(self.__background, self.__textRect)

    def isObjOverlappingObj(self, otherItem) -> bool:
            '''
            Given another object, determins if the items are overlapping or not
            '''
            otherX, otherY = otherItem.getPos()
            otherWidth, otherHeight = otherItem.getBounds()
            xOverlap = self.__x+self.__width >= otherX and otherX+otherWidth >= self.__x
            yOverlap = self.__y+self.__height >= otherY and otherY+otherHeight >= self.__y
            return xOverlap and yOverlap 
    
    def isPointOverlappingObj(self, point: tuple[int, int]) -> bool:
        '''
        Returns if a point is overlapping the item (this should be used for checking if the mouse is on an item)
        '''
        xOverlap = point[0]>=self.__x and point[0]<=self.__x+self.__width
        yOverlap = point[1]>=self.__y and point[1]<=self.__y+self.__height
        return xOverlap and yOverlap

class Item(Object):
    def __init__(self, pos_x, pos_y, item_name):
        super().__init__(pos_x, pos_y, item_name)

class Button(Object):
    def __init__(self, pos_x, pos_y, item_name, action):
        '''
        action: any function that takes a single argument which is the button that was pressed
        '''
        super().__init__(pos_x, pos_y, item_name)
        self.__action = action

    def getAction(self):
        return self.__action

if __name__ == "__main__":
    disp = Display([str(x) for x in range(100)])
    disp.updateAll()
    input()