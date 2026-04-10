from .Layer import Layer, resource_path
import pygame
from pygame.math import Vector2

class ScoreLayer(Layer):
    def __init__(self, cellSize, imageFile, state, color=(0, 0, 0)):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.font = pygame.font.Font(resource_path("assets/fonts/Winter_Draw.ttf"), 30)
        self.position = Vector2(self.state.worldWidth, 0)
        self.color = color

    def render(self, surface):
        text = "{}".format(self.state.score)
        textSurface = self.font.render(text, True, self.color)
        x = self.position.x * self.cellWidth - textSurface.get_width() - 5
        y = self.position.y * self.cellHeight
        textPos = Vector2(x, y)
        surface.blit(textSurface, textPos)
