import pygame
import os
import random
import tmx

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
        self.lastMoveEpoch = 0
        self.slidePos = Vector2(0, 0)

class Snake(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

        self.state.positionList.append(self.position)
        self.direction = "right"

    def lastPos(self):
        """
        Returns the penultimate position of the snake if there is one, or returns left to actual position.
        """
        try:
            return self.state.positionList[-2]
        except IndexError:
            return self.position + Vector2(-1, 0)

class Body(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

    def lastPos(self):
        """
        Returns the penultimate position of the body if there is one, or returns left to actual position.
        """
        for index, body in enumerate(self.state.bodies):
            if body.position == self.position:
                try:
                    lastPos = self.state.positionList[-index-3]
                except IndexError:
                    lastPos = self.position + Vector2(-1, 0)
        return lastPos

class Food(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

    def lastPos(self):
        """
        Returns the actual position of the food
        """
        return self.position

class GameState():
    def __init__(self):
        # Define time unit
        self.epoch = 0

        # Define world size
        self.worldSize = pygame.math.Vector2(30, 20)

        # Define move delay
        self.moveDelay = 10

        # Define game status : Play, Game Over
        self.gameStatus_dict = {
            "Play",
            "Game Over",
        }
        self.gameStatus = "Game Over"

        # Define the score
        self.score = 0

        # Define walls
        self.walls = []

        # Set attribute to move food when colliding with player
        self.foodMove = False

        # Define position List
        self.positionList = []

        # Define units list
        self.units = []

        # Define bodies list
        self.bodies = []

        # Define observers lists
        self.observers = []

    # Set properties for world width and height
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    @property
    def worldHeight(self):
        return int(self.worldSize.y)

    def addObserver(self, observer):
        """
        Add a game state observer.
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)

class GameStateObserver():
    pass

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
        self.unit.slidePos = Vector2(0,0)

        # Add the new position to the position List
        self.state.positionList.append(self.unit.position)

        # Compute bodies positions
        index = 0
        for body in self.state.bodies:
            try:
                new_pos = self.state.positionList[-index-2]
            except IndexError:
                new_pos = body.position
            body.position = new_pos
            body.slidePos = Vector2(0,0)
            index += 1

        # Delete positions not used by player or bodies
        if len(self.state.positionList) > len(self.state.bodies) + 3:
            del self.state.positionList[-(len(self.state.bodies) + 4)]

        # Compute collision with Food
        food = next(obj for obj in self.state.units if isinstance(obj, Food))
        if self.unit.position == food.position:
            self.state.foodMove = True
            # Add a Body to bodies list
            self.state.bodies.append(Body(self.state, self.state.positionList[1], Vector2(1, 0)))

            # Increment score
            self.state.score += 1

            # Speed up over 5 scores
            scoreMult = self.state.score / 5
            if scoreMult.is_integer() and self.state.moveDelay >= 5:
                self.state.moveDelay -= 1
                print("Speed Up ! ({})".format(self.state.moveDelay))

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

class SlideCommand(Command):
    def __init__(self, gameState, unit, cellSize):
        self.state = gameState
        self.unit = unit
        self.cellSize = cellSize

    def run(self):
        speed = self.cellSize.x / self.state.moveDelay
        value = self.unit.position - self.unit.lastPos()
        if value.x > 1 :
            value.x = -1
        elif value.x < -1:
            value.x = 1
        if value.y > 1:
            value.y = -1
        elif value.y < -1:
            value.y = 1
        self.unit.slidePos += value.elementwise() * speed

class LoadLevelCommand(Command):
    def __init__(self, ui, fileName):
        self.ui = ui
        self.fileName = fileName

    def decodeLayer(self, tileMap, layer):
        """
        Decode layer and check layer properties

        Returns the corresponding tileset
        """
        if not isinstance(layer, tmx.Layer):
            raise RuntimeError("Error in {}: invalid layer type".format(self.fileName))
        if len(layer.tiles) != tileMap.width * tileMap.height:
            raise RuntimeError("Error in {}: invalid tiles count".format(self.fileName))

        # Guess which tileset is used by this layer
        gid = None
        for tile in layer.tiles:
            if tile.gid != 0:
                gid = tile.gid
                break
        if gid is None:
            if len(tileMap.tilesets) == 0:
                raise RuntimeError("Error in {}: no tileset".format(self.fileName))
            tileset = tileMap.tilesets[0]
        else:
            tileset = None
            for t in tileMap.tilesets:
                if gid >= t.firstgid and gid < t.firstgid + t.tilecount:
                    tileset = t
                    break
            if tileset is None:
                raise RuntimeError("Error in {}: no corresponding tileset".format(self.fileName))

        # Check the tileset
        if tileset.columns <= 0:
            raise RuntimeError("Error in {}: invalid columns count".format(self.fileName))
        if tileset.image.data is not None:
            raise RuntimeError("Error in {}: embedded tileset image is not supported".format(self.fileName))

        return tileset

    def decodeArrayLayer(self, tileMap, layer):
        """
        Create an array from a tileMap layer
        """
        tileset = self.decodeLayer(tileMap, layer)

        array = [None] * tileMap.height
        for y in range(tileMap.height):
            array[y] = [None] * tileMap.width
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                array[y][x] = Vector2(tileX, tileY)

        return tileset, array

    def decodeUnitsLayer(self, state, tileMap, layer, flag):
        """
        Create a list from a tileMap layer
        """
        tileset = self.decodeLayer(tileMap, layer)

        units = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                if flag == "snake":
                    unit = Snake(state, Vector2(x, y), Vector2(tileX, tileY))
                elif flag == "body":
                    unit = Body(state, Vector2(x, y), Vector2(tileX, tileY))
                elif flag == "food":
                    unit = Food(state, Vector2(x, y), Vector2(tileX, tileY))
                else:
                    raise RuntimeError("Error in {}: unknown flag".format(self.fileName))
                units.append(unit)

        return tileset, units

    def run(self):
        # Load Map
        if not os.path.exists(self.fileName):
            raise RuntimeError("No file {}".format(self.fileName, self.fileName))
        tileMap = tmx.TileMap.load(self.fileName)

        # Check main properties
        if tileMap.orientation != ("orthogonal"):
            raise RuntimeError("Error in {}: invalid orientation".format(self.fileName))
        if len(tileMap.layers) != 4:
            raise RuntimeError("Error in {}: invalid number of layers".format(self.fileName))

        # World size
        state = self.ui.state
        state.worldSize = Vector2(tileMap.width, tileMap.height)

        # Walls Layer
        wallsTileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[0])
        cellSize = Vector2(wallsTileset.tilewidth, wallsTileset.tileheight)
        state.walls[:] = array
        imageFile = wallsTileset.image.source
        self.ui.layers[0].setTileset(cellSize, imageFile)

        # Units layer
        snakeTileset, snake = self.decodeUnitsLayer(state, tileMap, tileMap.layers[1], "snake")
        bodyTileset, bodies = self.decodeUnitsLayer(state, tileMap, tileMap.layers[2], "body")
        foodTileset, foods = self.decodeUnitsLayer(state, tileMap, tileMap.layers[3], "food")
        if snakeTileset != wallsTileset or bodyTileset != wallsTileset or foodTileset != wallsTileset:
            raise RuntimeError("Error in {}: tilesets must be the same for all layers".format(self.fileName))
        state.units[:] = snake + foods
        for food in foods:
            FoodCommand(state, food).run()
        state.bodies[:] = bodies
        self.ui.layers[1].setTileset(cellSize, imageFile)

        # Player unit
        self.ui.playerUnit = snake[0]

        # Window
        windowSize = state.worldSize.elementwise() * cellSize
        self.ui.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))

###############################################################################
#                                Rendering                                    #
###############################################################################

class Layer(GameStateObserver):
    def __init__(self, cellSize, imageFile):
        self.cellSize = cellSize
        if imageFile is not None:
            self.texture = pygame.image.load(imageFile).convert()
            self.texture.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)

    def setTileset(self, cellSize, imageFile):
        self.cellSize = cellSize
        self.texture = pygame.image.load(imageFile).convert()
        self.texture.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)

    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def renderTile(self, surface, position, tile, slidePos=Vector2(0,0), angle=None):
        # Location on screen
        spritePoint = position.elementwise() * self.cellSize + slidePos

        # Texture
        texturePoint = tile.elementwise() * self.cellSize
        textureRect = pygame.Rect(int(texturePoint.x), int(texturePoint.y), self.cellWidth, self.cellHeight)

        # Draw Tile
        if angle is None:
            surface.blit(self.texture, spritePoint, textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface((self.cellWidth, self.cellHeight), pygame.SRCALPHA)
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
    def __init__(self, ui, imageFile, state, array, surfaceFlags=pygame.SRCALPHA):
        super().__init__(ui, imageFile)
        self.state = state
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags

    def render(self, surface):
        if self.surface is None:
            self.surface = pygame.Surface(surface.get_size(), self.surfaceFlags)
            self.surface.fill((200, 150, 50))
            for y in range(self.state.worldHeight):
                for x in range(self.state.worldWidth):
                    tile = self.array[y][x]
                    if tile is not None:
                        self.renderTile(self.surface, Vector2(x, y), tile)
        surface.blit(self.surface, (0, 0))

class UnitLayer(Layer):
    def __init__(self, ui, imageFile, state, units):
        super().__init__(ui, imageFile)
        self.state = state
        self.units = units

    def render(self, surface):
        for body in self.state.bodies:
            self.renderTile(surface, body.lastPos(), body.tile, body.slidePos)
        for unit in self.units:
            self.renderTile(surface, unit.lastPos(), unit.tile, unit.slidePos, unit.angle)


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
        x = self.position.x * self.cellWidth - textSurface.get_width() - 5
        y = self.position.y * self.cellHeight
        textPos = Vector2(x, y)
        surface.blit(textSurface, textPos)

###############################################################################
#                             Game Modes                                      #
###############################################################################

class GameMode():
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self):
        raise NotImplementedError()

class MessageGameMode(GameMode):
    def __init__(self, ui, title, message):
        self.ui = ui

        self.font = pygame.font.Font("Winter_Draw.ttf", 70)
        self.fontScore = pygame.font.Font("Winter_Draw.ttf", 50)
        self.fontEspace = pygame.font.Font("Winter_Draw.ttf", 30)

        self.title = title
        self.message = message

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

class MenuGameMode(GameMode):
    def __init__(self, ui):
        self.ui = ui

class PlayGameMode(GameMode):
    def __init__(self, ui):
        pygame.init()

        self.ui = ui

        # Game State
        self.state = GameState()

        # Cell Size
        self.cellSize = Vector2(32, 32)

        # Window
        windowSize = self.state.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))

        # Rendering Properties
        self.textures = pygame.image.load("snake_fouchy32.png").convert()
        self.textures.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)
        self.fontScore = pygame.font.Font("Winter_Draw.ttf", 30)
        self.fontPos = Vector2(self.state.worldWidth, 0)

        # Layer List
        self.layers = [
            ArrayLayer(self.cellSize, "snake_fouchy32.png", self.state, self.state.walls, 0), # Walls
            UnitLayer(self.cellSize, "snake_fouchy32.png", self.state, self.state.units), # Units
            ScoreLayer(self.cellSize, None, self.state, self.fontScore, self.fontPos) # Score
        ]

        # All layers observe GameState
        for layer in self.layers:
            self.state.observers.append(layer)

        # Controls
        self.commands = []
        self.moveCommandList = []
        self.playerUnit = None

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
                elif event.key == pygame.K_1:
                    UserInterface.__init__(self)
                    self.state.gameStatus = "Play"
                    LoadLevelCommand(self, "levels/level_1.tmx").run()
                elif event.key == pygame.K_2:
                    UserInterface.__init__(self)
                    self.state.gameStatus = "Play"
                    LoadLevelCommand(self, "levels/level_2.tmx").run()
                elif event.key == pygame.K_3:
                    UserInterface.__init__(self)
                    self.state.gameStatus = "Play"
                    LoadLevelCommand(self, "levels/level_3.tmx").run()

    def update(self):
        if self.state.gameStatus == "Play":

            if self.state.epoch-self.playerUnit.lastMoveEpoch >= self.state.moveDelay:
                self.playerUnit.lastMoveEpoch = self.state.epoch
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
            SlideCommand(self.state, self.playerUnit, self.cellSize).run()
            for body in self.state.bodies:
                SlideCommand(self.state, body, self.cellSize).run()
            self.state.epoch += 1

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

###############################################################################
#                             User Interface                                  #
###############################################################################

class UserInterface():
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Snake")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        # Modes
        self.playGameMode = None
        self.overlayGameMode = MenuGameMode(self)
        self.currentActiveMode = 'Overlay'

        # Loop Properties
        self.clock = pygame.time.Clock()
        self.running = True

    def loadLevel(self, fileName):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode(self)
        self.playGameMode.commands.append(LoadLevelCommand(self.playGameMode, fileName))
        try :
            self.playGameMode.update()
            self.currentActiveMode = "Play"
        except Exception as ex:
            print(ex)
            self.playGameMode = None
            self.showMessage("Level loading failed :'(")

    def showGame(self):
        if self.playGameMode is None:
            self.currentActiveMode = "Play"

    def showMeny(self):
        self.overlayGameMode = MenuGameMode(self)
        self.currentActiveMode = "Overlay"

    def showMessage(self, title, message=None):
        self.overlayGameMode = MessageGameMode(self, title, message)
        self.currentActiveMode = "Overlay"
        
    def quitGame(self):
        self.running = False

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)x

game = UserInterface()
game.run()

with open("score.txt", "w") as file:
    file.write(str(game.state.score))
