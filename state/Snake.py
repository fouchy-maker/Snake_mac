from .Unit import Unit

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
