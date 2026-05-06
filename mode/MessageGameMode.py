from .GameMode import GameMode
from layer import resource_path
import pygame

class MessageGameMode(GameMode):
    def __init__(self, title, message, flag=None, level=1):
        super().__init__()

        self.fontTitle = pygame.font.Font(resource_path("assets/fonts/Winter_Draw.ttf"), 70)
        self.fontMessage = pygame.font.Font(resource_path("assets/fonts/Winter_Draw.ttf"), 50)
        self.fontEspace = pygame.font.Font(resource_path("assets/fonts/Winter_Draw.ttf"), 30)

        self.title = title
        self.message = message
        self.flag = flag
        self.level = level

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMainMenuRequested()
                if event.key == pygame.K_RETURN \
                or event.key == pygame.K_SPACE:
                    if self.flag == "gameOver":
                        self.notifyShowRestartMenuRequested()
                    elif self.flag == "victory":
                        if self.level < 4:
                            self.level += 1
                            self.notifyLoadLevelRequested("level_{}.tmx".format(self.level), self.level)
                        else:
                            self.notifyShowMainMenuRequested()
                    else:
                        self.notifyShowMainMenuRequested()

    def update(self):
        pass

    def render(self, window):
        # Render title text
        surface = self.fontTitle.render(self.title, True, (255, 0, 0))
        x = window.get_width() // 2 - surface.get_width() // 2
        y = window.get_height() // 3 - surface.get_height() // 2
        window.blit(surface, (x, y))

        # Render message text
        surface2 = self.fontMessage.render(self.message, True, (255, 0, 0))
        x2 = window.get_width() // 2 - surface2.get_width() // 2
        y2 = y + surface2.get_height() * 2
        window.blit(surface2, (x2, y2))

        # Render espace text
        surface3 = self.fontEspace.render("Appuie sur Espace pour continuer...",True, (0, 0, 0))
        x3 = window.get_width() // 2 - surface3.get_width() // 2
        y3 = y2 + surface3.get_height() * 2
        window.blit(surface3, (x3, y3))
