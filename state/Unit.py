from pygame.math import Vector2

class Unit():
    def __init__(self, gameState, position, tile, angle=None):
        self.state = gameState
        self.position = position
        self.tile = tile
        self.angle = angle
        self.lastMoveEpoch = 0
        self.slidePos = Vector2(0, 0)
        self.status = "alive"
