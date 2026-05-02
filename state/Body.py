from .Unit import Unit
from pygame.math import Vector2

class Body(Unit):
    def giveLastPos(self, player):
        """
        Returns the penultimate position of the body if there is one, or returns left to actual position.
        """
        for index, body in enumerate(player.bodies):
            if body.position == self.position:
                try:
                    lastPos = player.positionList[-index-3]
                except IndexError:
                    lastPos = self.position + Vector2(-1, 0)
        return lastPos

    def lastPos(self):
        raise NotImplementedError
