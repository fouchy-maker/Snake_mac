from .GameMode import GameMode
from layer import resource_path
import pygame

class MenuGameMode(GameMode):
    def __init__(self):
        super().__init__()
        # Fonts
        self.titleFont = pygame.font.Font(resource_path("assets/fonts/Winter_Draw.ttf"), 70)
        self.itemFont = pygame.font.Font(resource_path("assets/fonts/Winter_Draw.ttf"), 50)

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
                "title": "Quit",
                "action": lambda: self.notifyQuitRequested()
            }
        ]
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load(resource_path("assets/textures/cursor.png")).convert()
        self.menuCursor.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)

        # Compute Menu Width
        self.menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item["title"], True, (0, 150, 0))
            self.menuWidth = max(self.menuWidth, surface.get_width())
            item["surface"] = surface

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowGameRequested()
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

    def update(self):
        pass

    def render(self, window):
        # Initial y
        y = 50

        # Title
        surface = self.titleFont.render("FouchySnake !", True, (0, 200, 0))
        x = (window.get_width() - surface.get_width()) // 2
        window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100

        # Draw Menu Items
        x = (window.get_width() - self.menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            # Item text
            surface = item["surface"]
            window.blit(surface, (x, y))

            # Cursor
            if index == self.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                window.blit(self.menuCursor, (cursorX, cursorY))

            y += (120 * surface.get_height()) // 100
