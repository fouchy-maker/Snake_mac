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
        self.status = "alive"

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
    def __init__(self, level):
        # Define time unit
        self.epoch = 0

        # Define world size
        self.worldSize = Vector2(30, 20)

        # Store level
        self.level = level

        # Define move delay
        self.moveDelay = 10 - self.level

        # Define score
        self.score = 0

        # Define victory score
        self.scoreVictory = 20

        # Define walls
        self.walls = [ [None ] * int(self.worldSize.x) ] * int(self.worldSize.y)

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

    def notifyFoodCollide(self):
        for observer in self.observers:
            observer.FoodCollide()

    def notifyImpact(self):
        for observer in self.observers:
            observer.Impact()

class GameStateObserver():
    def FoodCollide(self):
        pass
    def Impact(self):
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

    def gameOver(self):
        """
        Set unit status to destroyed and play Impact sound
        """
        self.unit.status = "destroyed"
        self.state.notifyImpact()

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
                self.gameOver()
                return

        # If the player touches a wall, set game status to Game Over
        for y in range(self.state.worldHeight):
            for x in range(self.state.worldWidth):
                if self.state.walls[y][x] is not None and new_pos == Vector2(x, y):
                    self.gameOver()
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

            # Notify Sound Layer
            self.state.notifyFoodCollide()

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
    def __init__(self, gameMode, fileName):
        self.gameMode = gameMode
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
        state = self.gameMode.state
        state.worldSize = Vector2(tileMap.width, tileMap.height)

        # Walls Layer
        wallsTileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[0])
        cellSize = Vector2(wallsTileset.tilewidth, wallsTileset.tileheight)
        state.walls[:] = array
        imageFile = wallsTileset.image.source
        self.gameMode.layers[0].setTileset(cellSize, imageFile)

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
        self.gameMode.layers[1].setTileset(cellSize, imageFile)

        # Player unit
        self.gameMode.playerUnit = snake[0]

        # Window
        windowSize = state.worldSize.elementwise() * cellSize
        self.gameMode.notifyWorldSizeChanged(windowSize)

        # Resume game
        self.gameMode.gameOver = False

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
    def __init__(self, cellSize, imageFile, state, array, surfaceFlags=pygame.SRCALPHA):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags

    def setTileset(self,cellSize,imageFile):
        super().setTileset(cellSize,imageFile)
        self.surface = None

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
    def __init__(self, cellSize, imageFile, state, units):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.units = units

    def render(self, surface):
        for body in self.state.bodies:
            self.renderTile(surface, body.lastPos(), body.tile, body.slidePos)
        for unit in self.units:
            self.renderTile(surface, unit.lastPos(), unit.tile, unit.slidePos, unit.angle)


class ScoreLayer(Layer):
    def __init__(self, cellSize, imageFile, state, color=(0, 0, 0)):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.font = pygame.font.Font("Winter_Draw.ttf", 30)
        self.position = Vector2(self.state.worldWidth, 0)
        self.color = color

    def render(self, surface):
        text = "{}".format(self.state.score)
        textSurface = self.font.render(text, True, self.color)
        x = self.position.x * self.cellWidth - textSurface.get_width() - 5
        y = self.position.y * self.cellHeight
        textPos = Vector2(x, y)
        surface.blit(textSurface, textPos)

class SoundLayer(Layer):
    def __init__(self, foodCollideFile, impactFile):
        self.foodCollideSound = pygame.mixer.Sound(foodCollideFile)
        self.foodCollideSound.set_volume(0.5)
        self.impactSound = pygame.mixer.Sound(impactFile)
        self.impactSound.set_volume(0.5)

    def FoodCollide(self):
        self.foodCollideSound.play()

    def Impact(self):
        self.impactSound.play()

    def render(self, surface):
        pass


###############################################################################
#                             Game Modes                                      #
###############################################################################

class GameMode():
    def __init__(self):
        self.__observers = []
    def addObserver(self, observer):
        self.__observers.append(observer)
    def notifyLoadLevelRequested(self, fileName, level):
        for observer in self.__observers:
            observer.loadLevelRequested(fileName, level)
    def notifyWorldSizeChanged(self, worldSize):
        for observer in self.__observers:
            observer.worldSizeChanged(worldSize)
    def notifyShowMenuRequested(self):
        for observer in self.__observers:
            observer.showMenuRequested()
    def notifyShowGameRequested(self):
        for observer in self.__observers:
            observer.showGameRequested()
    def notifyGameWon(self, level):
        for observer in self.__observers:
            observer.gameWon(level)
    def notifyGameLost(self, score):
        for observer in self.__observers:
            observer.gameLost(score)
    def notifyQuitRequested(self):
        for observer in self.__observers:
            observer.quitRequested()
    def notifyMusicChangedRequested(self, musicFile, volume, fadeOut=0):
        for observer in self.__observers:
            observer.musicChangedRequested(musicFile, volume, fadeOut)

    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()

class GameModeObserver():
    def loadLevelRequested(self, fileName, level):
        pass
    def worldSizeChanged(self, worldSize):
        pass
    def showMenuRequested(self):
        pass
    def showGameRequested(self):
        pass
    def gameWon(self, level):
        pass
    def gameLost(self, score):
        pass
    def quitRequested(self):
        pass
    def musicChangedRequested(self, musicFile, volume, fadeOut=0):
        pass

class MessageGameMode(GameMode):
    def __init__(self, title, message, flag="gameOver", level=1):
        super().__init__()

        self.font = pygame.font.Font("Winter_Draw.ttf", 70)
        self.fontScore = pygame.font.Font("Winter_Draw.ttf", 50)
        self.fontEspace = pygame.font.Font("Winter_Draw.ttf", 30)

        self.title = title
        self.message = message
        self.flag = flag
        self.level = level

    def showMenu(self):
        self.notifyShowMenuRequested()
        self.notifyMusicChangedRequested("assets/music/Shadow_Dance.mp3", 0.5)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.showMenu()
                if event.key == pygame.K_RETURN \
                or event.key == pygame.K_SPACE:
                    if self.flag == "gameOver":
                        self.showMenu()
                    elif self.flag == "victory":
                        if self.level < 4:
                            self.level += 1
                            self.notifyLoadLevelRequested("levels/level_{}.tmx".format(self.level), self.level)
                        else:
                            self.showMenu()

    def update(self):
        pass

    def render(self, window):
        # Render title text
        surface = self.font.render(self.title, True, (255, 0, 0))
        x = window.get_width() // 2 - surface.get_width() // 2
        y = window.get_height() // 3 - surface.get_height() // 2
        window.blit(surface, (x, y))

        # Render Score text
        surface2 = self.fontScore.render(self.message, True, (255, 0, 0))
        x2 = window.get_width() // 2 - surface2.get_width() // 2
        y2 = y + surface2.get_height() * 2
        window.blit(surface2, (x2, y2))

        # Render Espace text
        surface3 = self.fontEspace.render("Appuie sur Espace pour continuer...",True, (0, 0, 0))
        x3 = window.get_width() // 2 - surface3.get_width() // 2
        y3 = y2 + surface3.get_height() * 2
        window.blit(surface3, (x3, y3))

class MenuGameMode(GameMode):
    def __init__(self):
        super().__init__()
        # Fonts
        self.titleFont = pygame.font.Font("Winter_Draw.ttf", 70)
        self.itemFont = pygame.font.Font("Winter_Draw.ttf", 50)

        # Menu Items
        self.menuItems = [
            {
                "title": "Level 1",
                "action": lambda: self.notifyLoadLevelRequested("levels/level_1.tmx", 1)
            },
            {
                "title": "Level 2",
                "action": lambda: self.notifyLoadLevelRequested("levels/level_2.tmx", 2)
            },
            {
                "title": "Level 3",
                "action": lambda: self.notifyLoadLevelRequested("levels/level_3.tmx", 3)
            },
            {
                "title": "Level 4",
                "action": lambda: self.notifyLoadLevelRequested("levels/level_4.tmx", 4)
            },
            {
                "title": "Quit",
                "action": lambda: self.notifyQuitRequested()
            }
        ]
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load("cursor.png").convert()
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

class PlayGameMode(GameMode):
    def __init__(self, level):
        super().__init__()
        # Game State
        self.state = GameState(level)

        # Cell Size
        self.cellSize = Vector2(32, 32)

        # Layer List
        self.layers = [
            ArrayLayer(self.cellSize, "snake_fouchy32.png", self.state, self.state.walls, 0), # Walls
            UnitLayer(self.cellSize, "snake_fouchy32.png", self.state, self.state.units), # Units
            ScoreLayer(self.cellSize, None, self.state), # Score
            SoundLayer("assets/sounds/gotFood.wav", "assets/sounds/impact.wav") # Sounds
        ]

        # All layers observe GameState
        for layer in self.layers:
            self.state.observers.append(layer)

        # Controls
        self.commands = []
        self.moveCommandList = []
        self.playerUnit = None
        self.gameOver = False

    # Set properties for cell width and height
    @property
    def cellWidth(self):
        return int(self.cellSize.x)
    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):
        if self.gameOver:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
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


    def update(self):
        for command in self.commands:
            command.run()
            self.commands.clear()
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

        # Check Game Over
        if self.playerUnit.status != "alive":
            self.gameOver = True
            self.notifyGameLost(self.state.score)

        # Check Victory
        if self.state.score >= self.state.scoreVictory:
            self.gameOver = True
            self.notifyGameWon(self.state.level)

    def render(self, window):
        window.fill((200, 150, 50))
        # Render Layers
        for layer in self.layers:
            layer.render(window)


###############################################################################
#                             User Interface                                  #
###############################################################################

class UserInterface(GameModeObserver):
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Snake")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        # Modes
        self.playGameMode = None
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'

        # Loop Properties
        self.clock = pygame.time.Clock()
        self.running = True

        # Menu Music
        self.musicChangedRequested("assets/music/Shadow_Dance.mp3", 0.5)

    def loadLevelRequested(self, fileName, level):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode(level)
            self.playGameMode.addObserver(self)
        else:
            self.playGameMode.__init__(level)
            self.playGameMode.addObserver(self)

        self.playGameMode.commands.append(LoadLevelCommand(self.playGameMode, fileName))
        try :
            self.playGameMode.update()
            self.currentActiveMode = "Play"
            self.musicChangedRequested("assets/music/Elephant_Walk.wav", 0.3, 2000)

        except Exception as ex:
            print(ex)
            self.playGameMode = None
            self.showMessage("Level loading failed :'(")

    def worldSizeChanged(self, worldSize):
        self.window = pygame.display.set_mode((int(worldSize.x),int(worldSize.y)))

    def showGameRequested(self):
        if self.playGameMode is not None:
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
        pygame.mixer.music.load(musicFile)
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
