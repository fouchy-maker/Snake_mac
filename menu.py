import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Menu():
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("FouchySnake")
        icon = pygame.image.load("icon.png").convert()
        icon.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)
        pygame.display.set_icon(icon)

        # Fonts
        self.titleFont = pygame.font.Font("Winter_Draw.ttf", 70)
        self.itemFont = pygame.font.Font("Winter_Draw.ttf", 50)

        # Menu Items
        self.menuItems = [
            {
                "title": "Level 1",
                "action": lambda: self.loadLevel("levels/level_1.tmx")
            },
            {
                "title": "Level 2",
                "action": lambda: self.loadLevel("levels/level_2.tmx")
            },
            {
                "title": "Level 3",
                "action": lambda: self.loadLevel("levels/level_3.tmx")
            },
            {
                "title": "Level 4",
                "action": lambda: self.loadLevel("levels/level_4.tmx")
            },
            {
                "title": "Quit",
                "action": lambda: self.exitMenu()
            }
        ]
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load("cursor.png").convert()

        # Loop Properties
        self.clock = pygame.time.Clock()
        self.running = True

    def loadLevel(self, levelName):
        print("Loading " + levelName)

    def exitMenu(self):
        self.running = False

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitMenu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exitMenu()
                elif event.key == pygame.K_DOWN:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                elif event.key == pygame.K_UP:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem["action"]()
                    except Exception as ex:
                        print(ex)

    def update(self):
        pass

    def render(self):
        self.window.fill((0, 0, 0))

        # Initial y
        y = 50

        # Title
        surface = self.titleFont.render("FouchySnake !", True, (0, 200, 0))
        x = (self.window.get_width() - surface.get_width()) // 2
        self.window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100

        # Compute Menu Width
        menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item["title"], True, (0, 150, 0))
            menuWidth = max(menuWidth, surface.get_width())
            item["surface"] = surface

        # Draw Menu Items
        x = (self.window.get_width() - menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            # Item text
            surface = item["surface"]
            self.window.blit(surface, (x, y))

            # Cursor
            if index == self.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                self.window.blit(self.menuCursor, (cursorX, cursorY))

            y += (120 * surface.get_height()) // 100

        pygame.display.flip()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

menu = Menu()
menu.run()