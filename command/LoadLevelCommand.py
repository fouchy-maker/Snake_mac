from .Command import Command
from command import FoodCommand
from state import Snake, Body, Food
from pygame.math import Vector2
import tmx
import os

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
