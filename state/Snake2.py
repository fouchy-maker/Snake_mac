from .Unit import Unit
from .Body2 import Body2
from pygame.math import Vector2

class Snake2(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

        self.positionList = [self.position]
        self.direction = "right"
        self.bodies = []

    def lastPos(self):
        """
        Returns the penultimate position of the snake if there is one, or returns left to actual position.
        """
        try:
            return self.positionList[-2]
        except IndexError:
            return self.position + Vector2(-1, 0)

    def addBody(self):
        """
        Adds a new body to the snake
        """
        self.bodies.append(Body2(self.state, self.positionList[1], Vector2(1, 2)))