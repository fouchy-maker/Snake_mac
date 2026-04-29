from .Unit import Unit
from pygame.math import Vector2

class Body2(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

    def lastPos(self):
        """
        Returns the penultimate position of the body if there is one, or returns left to actual position.
        """
        for index, body in enumerate(self.state.players[1].bodies):
            if body.position == self.position:
                try:
                    lastPos = self.state.players[1].positionList[-index-3]
                except IndexError:
                    lastPos = self.position + Vector2(-1, 0)
        return lastPos
