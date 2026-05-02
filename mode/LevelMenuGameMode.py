from .MenuGameMode import MenuGameMode
import pygame

class LevelMenuGameMode(MenuGameMode):
    def __init__(self):
        # Menu Items
        self.menuItems = [
            {
                "title": "Level 1",
                "action": lambda: self.notifyLoadLevelRequested("level_1.tmx", 1)
            },
            {
                "title": "Level 2",
                "action": lambda: self.notifyLoadLevelRequested("level_2.tmx", 2)
            },
            {
                "title": "Level 3",
                "action": lambda: self.notifyLoadLevelRequested("level_3.tmx", 3)
            },
            {
                "title": "Level 4",
                "action": lambda: self.notifyLoadLevelRequested("level_4.tmx", 4)
            },
            {
                "title": "Back",
                "action": lambda: self.notifyShowPlayerMenuRequested()
            }
        ]
        super().__init__()

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    self.notifyShowPlayerMenuRequested()
                elif event.key == pygame.K_DOWN:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                    else:
                        self.currentMenuItem = 0
                elif event.key == pygame.K_UP:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                    else:
                        self.currentMenuItem = len(self.menuItems) - 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem["action"]()
                    except Exception as ex:
                        print(ex)
