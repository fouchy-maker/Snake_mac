from .Snake import Snake
from .Body1 import Body1
from pygame.math import Vector2

class Snake1(Snake):
    def addBody(self):
        """
        Adds a new body to the snake
        """
        self.bodies.append(Body1(self.state, self.positionList[1], Vector2(1, 0)))