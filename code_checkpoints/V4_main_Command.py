import pygame
import os
import random

from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'

###############################################################################
#                               Game State                                    #
###############################################################################

class Unit():
    def __init__(self, gameState, position, tile, angle=None):
        self.state = gameState
        self.position = position
        self.tile = tile
        self.angle = angle

class Snake(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

        self.state.positionList.append(self.position)
        self.direction = "right"

class Body(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

class Food(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

class GameState():
    def __init__(self):
        # Define time unit
        self.epoch = 0

        # Define world size
        self.worldSize = pygame.math.Vector2(30, 20)

        # Define update speed
        self.speed = 10
        self.speed_current = 0

        # Define game status : Play, Game Over
        self.gameStatus_dict = {
            "Play",
            "Game Over",
        }
        self.gameStatus = "Play"

        # Define the score
        self.score = 0

        # Define walls
        self.walls = [
            [ Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, Vector2(0, 1)],
            [ Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1), Vector2(0, 1)]
        ]

        # Set attribute to move food when colliding with player
        self.foodMove = False

        # Define position List
        self.positionList = []

        # Define units list
        self.units = []
        self.units.append(Snake(self, Vector2(5, 5), Vector2(0, 0)))
        self.units.append(Food(self, None, Vector2(2, 0)))

        # Define bodies list
        self.bodies = []
        self.bodies.append(Body(self, Vector2(4, 5), Vector2(1, 0)))

    # Set properties for world width and height
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    @property
    def worldHeight(self):
        return int(self.worldSize.y)

###############################################################################
#                                Commands                                     #
###############################################################################

class Command():
    def run(self):
        raise NotImplementedError()

class MoveCommand(Command):
    def __init__(self, gameState, unit, direction):
        self.state = gameState
        self.unit = unit
        self.direction = direction

    def run(self):
        # Compute new position using direction dictionary
        direction_dict = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        for direction, value in direction_dict.items():
            if direction == self.direction:
                new_pos = self.unit.position + value

        # Compute angle using angle dictionary
        angleDict = {"up": 90, "down": 270, "left": 180, "right": 0}
        for direction, value in angleDict.items():
            if direction == self.direction:
                self.unit.angle = value

        # If the player touches the window, he reappears on the other side
        if new_pos.x < 0:
            new_pos.x = self.state.worldWidth - 1
        elif new_pos.x > self.state.worldWidth - 1:
            new_pos.x = 0
        elif new_pos.y < 0:
            new_pos.y = self.state.worldHeight - 1
        elif new_pos.y > self.state.worldHeight - 1:
            new_pos.y = 0

        # If the player touches a body, set game status to Game Over
        for body in self.state.bodies:
            if new_pos == body.position:
                self.state.gameStatus = "Game Over"
                return

        # If the player touches a wall, set game status to Game Over
        for y in range(self.state.worldHeight):
            for x in range(self.state.worldWidth):
                if self.state.walls[y][x] is not None and new_pos == Vector2(x, y):
                    self.state.gameStatus = "Game Over"
                    return

        # Save new position and direction to unit
        self.unit.position = new_pos
        self.unit.direction = self.direction

        # Add the new position to the position List
        self.state.positionList.append(self.unit.position)

        # Compute bodies positions
        index = 0
        for body in self.state.bodies:
            body.position = self.state.positionList[-index-2]
            index += 1

        # Delete positions not used by player or bodies
        if len(self.state.positionList) > len(self.state.bodies) + 2:
            del self.state.positionList[-(len(self.state.bodies) + 3)]

        # Compute collision with Food
        food = next(obj for obj in self.state.units if isinstance(obj, Food))
        if self.unit.position == food.position:
            self.state.foodMove = True
            # Add a Body to bodies list
            self.state.bodies.append(Body(self.state, self.state.positionList[0], Vector2(1, 0)))

            # Increment score
            self.state.score += 1

            # Speed up over 5 scores
            scoreMult = self.state.score / 5
            if scoreMult.is_integer() and self.state.speed >= 5:
                self.state.speed -= 1
                print("Speed Up !")

class FoodCommand(Command):
    def __init__(self, gameState, unit):
        self.state = gameState
        self.unit = unit

    def run(self):
        # If new position is equal to player, body or wall position, recompute position
        run = True
        while run:
            new_pos = pygame.Vector2(
                random.randint(0, self.state.worldWidth - 1),
                random.randint(0, self.state.worldHeight - 1)
            )
            # Units position
            for pos in self.state.positionList:
                if new_pos == pos:
                    new_pos = None
                    print("Food Reposition !")
                    break

            # Wall position
            for y in range(self.state.worldHeight):
                for x in range(self.state.worldWidth):
                    if self.state.walls[y][x] is not None and new_pos == Vector2(x, y):
                        new_pos = None
                        print("Food Reposition !")
                        break

            if new_pos is not None:
                self.unit.position = new_pos
                run = False

###############################################################################
#                                Rendering                                    #
###############################################################################

class Layer():
    def __init__(self, ui, imageFile):
        self.ui = ui
        if imageFile is not None:
            self.texture = pygame.image.load(imageFile).convert()
            self.texture.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)

    def renderTile(self, surface, position, tile, angle=None):
        # Location on screen
        spritePoint = position.elementwise() * self.ui.cellSize

        # Texture
        texturePoint = tile.elementwise() * self.ui.cellSize
        textureRect = pygame.Rect(int(texturePoint.x), int(texturePoint.y), self.ui.cellWidth, self.ui.cellHeight)

        # Draw Tile
        if angle is None:
            surface.blit(self.texture, spritePoint, textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface((self.ui.cellWidth, self.ui.cellHeight), pygame.SRCALPHA)
            textureTile.blit(self.texture, (0, 0), textureRect)
            # Rotate the surface with the tile
            rotatedTile = pygame.transform.rotate(textureTile, angle)
            # Compute the new coordinate on the screen, knowing that we rotate around the center of the tile
            spritePoint.x -= (rotatedTile.get_width() - textureTile.get_width()) // 2
            spritePoint.y -= (rotatedTile.get_height() - textureTile.get_height()) // 2
            # Render the rotatedTile
            surface.blit(rotatedTile, spritePoint)

    def render(self, surface):
        raise NotImplementedError()

class ArrayLayer(Layer):
    def __init__(self, ui, imageFile, state, array):
        super().__init__(ui, imageFile)
        self.state = state
        self.array = array

    def render(self, surface):
        for y in range(self.state.worldHeight):
            for x in range(self.state.worldWidth):
                tile = self.array[y][x]
                if tile is not None:
                    self.renderTile(surface, Vector2(x, y), tile)

class UnitLayer(Layer):
    def __init__(self, ui, imageFile, state, units):
        super().__init__(ui, imageFile)
        self.state = state
        self.units = units

    def render(self, surface):
        for unit in self.units:
            self.renderTile(surface, unit.position, unit.tile, unit.angle)
        for body in self.state.bodies:
            self.renderTile(surface, body.position, body.tile)

class ScoreLayer(Layer):
    def __init__(self, ui, imageFile, state, font, position, color=(0, 0, 0)):
        super().__init__(ui, imageFile)
        self.state = state
        self.font = font
        self.position = position
        self.color = color

    def render(self, surface):
        text = "{}".format(self.state.score)
        textSurface = self.font.render(text, True, self.color)
        x = self.position.x * self.ui.cellWidth - textSurface.get_width() - 5
        y = self.position.y * self.ui.cellHeight
        textPos = Vector2(x, y)
        surface.blit(textSurface, textPos)

###############################################################################
#                             Game Modes                                      #
###############################################################################

class GameMode():
    def __init__(self, ui):
        self.ui = ui

    def render(self):
        raise NotImplementedError()

class GameOver(GameMode):
    def __init__(self, ui):
        super().__init__(ui)
        self.font = pygame.font.Font("Winter_Draw.ttf", 70)
        self.fontScore = pygame.font.Font("Winter_Draw.ttf", 50)
        self.fontEspace = pygame.font.Font("Winter_Draw.ttf", 30)

    def render(self):
        # Render Game Over text
        surface = self.font.render("Game Over !", True, (255, 0, 0))
        x = self.ui.window.get_width() // 2 - surface.get_width() // 2
        y = self.ui.window.get_height() // 3 - surface.get_height() // 2
        self.ui.window.blit(surface, (x, y))

        # Render Score text
        surface2 = self.fontScore.render("Score : {}".format(self.ui.state.score), True, (255, 0, 0))
        x2 = self.ui.window.get_width() // 2 - surface2.get_width() // 2
        y2 = y + surface2.get_height() * 2
        self.ui.window.blit(surface2, (x2, y2))

        # Render Espace text
        surface3 = self.fontEspace.render("Appuie sur Espace pour recommencer...".format(self.ui.state.score),
                                         True, (0, 0, 0))
        x3 = self.ui.window.get_width() // 2 - surface3.get_width() // 2
        y3 = y2 + surface3.get_height() * 2
        self.ui.window.blit(surface3, (x3, y3))

###############################################################################
#                             User Interface                                  #
###############################################################################

class UserInterface():
    def __init__(self):
        pygame.init()

        # Game State
        self.state = GameState()

        # Cell Size
        self.cellSize = pygame.math.Vector2(32, 32)

        # Window
        windowSize = self.state.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption("Snake")

        # Rendering Properties
        self.textures = pygame.image.load("snake_fouchy32.png").convert()
        self.textures.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)
        self.fontScore = pygame.font.Font("Winter_Draw.ttf", 30)
        self.fontPos = Vector2(self.state.worldWidth, 0)

        # Controls
        self.moveCommandList = []
        # Compute food position
        food = next(unit for unit in self.state.units if isinstance(unit, Food))
        FoodCommand(self.state, food).run()
        self.playerUnit = self.state.units[0]

        # Layer List
        self.layers = [
            ArrayLayer(self, "snake_fouchy32.png", self.state, self.state.walls), # Walls
            UnitLayer(self, "snake_fouchy32.png", self.state, self.state.units), # Units
            ScoreLayer(self, None, self.state, self.fontScore, self.fontPos) # Score
        ]

        # Loop Properties
        self.clock = pygame.time.Clock()
        self.running = True

    # Set properties for cell width and height
    @property
    def cellWidth(self):
        return int(self.cellSize.x)
    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "up"))
                elif event.key == pygame.K_DOWN:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "down"))
                elif event.key == pygame.K_LEFT:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "left"))
                elif event.key == pygame.K_RIGHT:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "right"))
                elif event.key == pygame.K_z:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "up"))
                elif event.key == pygame.K_s:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "down"))
                elif event.key == pygame.K_q:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "left"))
                elif event.key == pygame.K_d:
                        self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "right"))
                elif event.key == pygame.K_SPACE:
                    UserInterface.__init__(self)
                    self.state.gameStatus = "Play"

    def update(self):
        if self.state.gameStatus == "Play":
            if self.state.speed_current >= self.state.speed:
                self.state.speed_current = 0

                # Run Snake Command if the direction is different from player's or opposite
                while len(self.moveCommandList) > 0:
                    dir_opp = {"up": "down", "down": "up", "left": "right", "right": "left"}
                    firstCommand = self.moveCommandList[0]
                    if not (firstCommand.direction == self.playerUnit.direction
                            or firstCommand.direction == dir_opp[self.playerUnit.direction]):
                        firstCommand.run()
                        del self.moveCommandList[0]
                        break
                    del self.moveCommandList[0]
                # If Snake Command List is empty, run Command with snake position
                else:
                    MoveCommand(self.state, self.playerUnit, self.playerUnit.direction).run()

                # Run Food Command
                if self.state.foodMove:
                    for unit in self.state.units:
                        if isinstance(unit, Food):
                            command = FoodCommand(self.state, unit)
                            command.run()
                    self.state.foodMove = False

            else:
                self.state.speed_current += 1

    def render(self):
        self.window.fill((200, 150, 50))
        if self.state.gameStatus == "Play":
            # Render Layers
            for layer in self.layers:
                layer.render(self.window)

        elif self.state.gameStatus == "Game Over":
            gameOver = GameOver(self)
            gameOver.render()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

game = UserInterface()
game.run()

with open("score.txt", "w") as file:
    file.write(str(game.state.score))
