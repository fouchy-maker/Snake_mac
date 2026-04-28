import random
from pygame.math import Vector2
from .Command import Command

class FoodCommand(Command):
    def __init__(self, gameState, unit):
        self.state = gameState
        self.unit = unit

    def run(self):
        # If new position is equal to player, body or wall position, recompute position
        run = True
        while run:
            new_pos = Vector2(
                random.randint(0, self.state.worldWidth - 1),
                random.randint(0, self.state.worldHeight - 1)
            )

            # Units and bodies positions
            positions = self.state.units[0].positionList + self.state.units[1].positionList
            for pos in positions:
                if new_pos == pos:
                    new_pos = None
                    print("Food Reposition !")
                    break

            # Wall position
            for y in range(self.state.worldHeight):
                for x in range(self.state.worldWidth):
                    if self.state.walls[y][x] is not None and new_pos == Vector2(x, y):
                        new_pos = None
                        print("Food Reposition !")
                        break

            if new_pos is not None:
                self.unit.position = new_pos
                run = False
