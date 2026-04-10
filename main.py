import pygame
import os
from layer import resource_path
from mode import GameModeObserver, MenuGameMode, MessageGameMode, PlayGameMode
from command import LoadLevelCommand

os.environ['SDL_VIDEO_CENTERED'] = '1'

class UserInterface(GameModeObserver):
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Snake")
        pygame.display.set_icon(pygame.image.load(resource_path("assets/textures/icon.png")))

        # Modes
        self.playGameMode = None
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'

        # Loop Properties
        self.clock = pygame.time.Clock()
        self.running = True

        # Menu Music
        self.musicChangedRequested("Shadow_Dance.mp3", 0.5)

    def loadLevelRequested(self, fileName, level):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode(level)
            self.playGameMode.addObserver(self)
        else:
            self.playGameMode.__init__(level)
            self.playGameMode.addObserver(self)

        self.playGameMode.commands.append(LoadLevelCommand(self.playGameMode, resource_path("levels/{}".format(fileName))))
        try :
            self.playGameMode.update()
            self.currentActiveMode = "Play"
            levelMusics = ["Elephant_Walk_1.wav",
                           "Elephant_Walk_2.wav",
                           "Elephant_Walk_3.wav",
                           "Elephant_Walk_4.wav"
                           ]
            try :
                self.musicChangedRequested(levelMusics[level-1], 0.3, 2000)
            except IndexError as ex:
                print(ex)

        except Exception as ex:
            print(ex)
            self.playGameMode = None
            self.showMessage("Level loading failed :'(")

    def worldSizeChanged(self, worldSize):
        self.window = pygame.display.set_mode((int(worldSize.x),int(worldSize.y)))

    def showGameRequested(self):
        if self.playGameMode is not None and self.playGameMode.gameOver is False:
            self.currentActiveMode = "Play"

    def showMenuRequested(self):
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = "Overlay"

    def showMessage(self, title, message=None, flag="gameOver", level=1):
        self.overlayGameMode = MessageGameMode(title, message, flag, level)
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = "Overlay"

    def gameWon(self, level):
        self.showMessage("Well done !", None, "victory", level)
        pygame.mixer.music.stop()

    def gameLost(self, score):
        self.showMessage("Game Over", "Score : {}".format(score))
        pygame.mixer.music.stop()
        
    def quitRequested(self):
        self.running = False

    def musicChangedRequested(self, musicFile, volume, fadeOut=0):
        pygame.mixer.music.fadeout(fadeOut)
        pygame.mixer.music.load(resource_path("assets/music/{}".format(musicFile)))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)

    def run(self):
        while self.running:
            # Inputs and Updates are exclusives
            if self.currentActiveMode == "Overlay":
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            elif self.playGameMode is not None:
                self.playGameMode.processInput()
                try:
                    self.playGameMode.update()
                except Exception as ex:
                    print(ex)
                    self.playGameMode = None
                    self.showMessage("Error during the game update...")

            # Render the game (if any), and then the overlay (if active)
            if self.playGameMode is not None:
                self.playGameMode.render(self.window)
            else:
                self.window.fill((0, 0, 0))
            if self.currentActiveMode == "Overlay":
                darkSurface = pygame.Surface(self.window.get_size(), flags=pygame.SRCALPHA)
                pygame.draw.rect(darkSurface, (0, 0, 0, 150), darkSurface.get_rect())
                self.window.blit(darkSurface, (0, 0))
                self.overlayGameMode.render(self.window)

            # Update display
            pygame.display.update()
            self.clock.tick(60)

game = UserInterface()
game.run()

#with open("score.txt", "w") as file:
    #file.write(str(game.state.score))
