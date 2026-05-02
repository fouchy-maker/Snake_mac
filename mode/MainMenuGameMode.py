from .MenuGameMode import MenuGameMode
import pygame

class MainMenuGameMode(MenuGameMode):
    def __init__(self):
        # Menu Items
        self.menuItems = [
            {
                "title": "Play",
                "action": lambda: self.notifyShowPlayerMenuRequested()
            },
            {
                "title": "Options",
                "action": lambda: self.notifyShowOptionsMenuRequested()
            },
            {
                "title": "Quit",
                "action": lambda: self.notifyQuitRequested()
            }
        ]
        super().__init__()

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyQuitRequested()
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
