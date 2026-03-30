import pygame
import os
import random

from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameState():
    def __init__(self):
        # Define world size
        self.worldSize = pygame.math.Vector2(30, 20)

        # Define Player position
        self.playerPos = pygame.Vector2(5, 5)
        self.positionList = [self.playerPos]
        self.posIndex = -2

        # Define Player speed
        self.speed = 10
        self.speed_current = 0

        # Define player direction : right, left, up, down
        self.direction_dict = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        self.direction = "right"

        # Define opposites direction dictionary for Player move
        self.dir_opp = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

        # Define angle
        self.angleDict = {
            "up": 90,
            "down": 270,
            "left": 180,
            "right": 0
        }
        self.angle = 0

        # Define Food position and Moved food variable
        self.foodPos = pygame.Vector2(
            random.randint(0 , int(self.worldSize.x) - 1),
            random.randint(0 , int(self.worldSize.y) - 1)
        )
        self.foodMove = True

        # Define Body number and position
        self.body_number = 1
        self.bodyPos = pygame.Vector2(4, 5)

        # Define units list
        self.units = [
            Player(self, self.playerPos, pygame.Vector2(0,0)),
            Food(self, self.foodPos, pygame.Vector2(2,0)),
            Body(self,
                self.bodyPos,
                pygame.Vector2(1, 0))
        ]

        # Define game status : Play, Game Over
        self.gameStatus_dict = {
            "Play",
            "Game Over",
        }
        self.gameStatus = "Play"

        # Define the score
        self.score = 0

        # Define command list
        self.commandList = []

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

        # Recompute Food coordinates
        food = next(obj for obj in self.units if isinstance(obj, Food))
        food.move()

    # Set properties for world width and height
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    @property
    def worldHeight(self):
        return int(self.worldSize.y)

    def update(self):
        if self.speed_current >= self.speed:
            self.speed_current = 0

            # Update positions
            for unit in self.units:
                unit.move()
            self.posIndex = -2

        else:
            self.speed_current += 1

class Unit():
    def __init__(self, gamestate, position, tile):
        self.state = gamestate
        self.position = position
        self.tile = tile
        self.angle = None

    def move(self):
        raise NotImplementedError()

class Player(Unit):
    def move(self):
        # Process first command in commandList and remove it,
        # if it is not the direction or the opposite, save it to direction
        while len(self.state.commandList) > 0:
            cmd = self.state.commandList[0]
            if cmd == self.state.direction or cmd == self.state.dir_opp[self.state.direction]:
                del self.state.commandList[0]
            else:
                self.state.direction = self.state.commandList[0]
                del self.state.commandList[0]
                break

        # Compute new position using direction dictionary
        for direction, value in self.state.direction_dict.items():
            if direction == self.state.direction:
                new_pos = self.position + value

        # Compute angle using angle dictionary
        for direction, value in self.state.angleDict.items():
            if direction == self.state.direction:
                self.angle = value

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
        for unit in self.state.units:
            if isinstance(unit, Body):
                if new_pos == unit.position:
                    self.state.gameStatus = "Game Over"
                    return

        # If the player touches a wall, set game status to Game Over
        for y in range(self.state.worldHeight):
            for x in range(self.state.worldWidth):
                if self.state.walls[y][x] is not None and new_pos == Vector2(x, y):
                    self.state.gameStatus = "Game Over"
                    return

        # Save new position to attribute
        self.position = new_pos

        # Delete positions not used by player or bodies
        if len(self.state.positionList) > self.state.body_number + 2:
            del self.state.positionList[-self.state.body_number - 3]

        # Add the new position to the position List
        self.state.positionList.append(self.position)

        # Compute collision with Food
        food = next(obj for obj in self.state.units if isinstance(obj, Food))
        if self.position == food.position:
            # Add a Body to unit list
            self.state.body_number += 1
            self.state.units.append(Body(
                self.state,
                # Position : la position dans la liste à l'index "-body_number - 1"
                self.state.positionList[-self.state.body_number - 2],
                pygame.Vector2(1, 0)))
            self.state.foodMove = True
            self.state.score += 1
            # Speed up over 5 scores
            scoreMult = self.state.score / 5
            if scoreMult.is_integer() and self.state.speed >= 5:
                self.state.speed -= 1
                print("Speed Up !")

class Body(Unit):
    def move(self):
        self.position = self.state.positionList[self.state.posIndex]
        self.state.posIndex -= 1

class Food(Unit):
    def move(self):
        if self.state.foodMove:
            run = True
            while run:
                # If new position is equal to player, body or wall position, recompute position
                new_pos = pygame.Vector2(
                random.randint(0 , self.state.worldWidth - 1),
                random.randint(0 , self.state.worldHeight - 1)
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
                    self.position = new_pos
                    self.state.foodMove = False
                    run = False

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
                        self.state.commandList.append("up")
                elif event.key == pygame.K_DOWN:
                        self.state.commandList.append("down")
                elif event.key == pygame.K_LEFT:
                        self.state.commandList.append("left")
                elif event.key == pygame.K_RIGHT:
                        self.state.commandList.append("right")
                elif event.key == pygame.K_z:
                        self.state.commandList.append("up")
                elif event.key == pygame.K_s:
                        self.state.commandList.append("down")
                elif event.key == pygame.K_q:
                        self.state.commandList.append("left")
                elif event.key == pygame.K_d:
                        self.state.commandList.append("right")
                elif event.key == pygame.K_SPACE:
                    UserInterface.__init__(self)
                    self.state.gameStatus = "Play"

    def update(self):
        if self.state.gameStatus == "Play":
            self.state.update()

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
