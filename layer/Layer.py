from state import GameStateObserver
import sys
import os
import pygame
from pygame.math import Vector2

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # dossier temporaire PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Layer(GameStateObserver):
    def __init__(self, cellSize, imageFile):
        self.cellSize = cellSize
        if imageFile is not None:
            self.texture = pygame.image.load(resource_path("assets/textures/{}".format(imageFile))).convert()
            self.texture.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)

    def setTileset(self, cellSize, imageFile):
        self.cellSize = cellSize
        self.texture = pygame.image.load(resource_path(imageFile)).convert()
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
