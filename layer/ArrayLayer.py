from .Layer import Layer
import pygame
from pygame.math import Vector2

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
