from .Unit import Unit

class Food(Unit):
    def __init__(self, gameState, position, tile):
        super().__init__(gameState, position, tile)

    def lastPos(self):
        """
        Returns the actual position of the food
        """
        return self.position