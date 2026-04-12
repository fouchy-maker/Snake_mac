from .Command import Command
from pygame.math import Vector2
from state import Food, Body

class MoveCommand(Command):
    def __init__(self, gameState, unit, direction):
        self.state = gameState
        self.unit = unit
        self.direction = direction

    def gameOver(self):
        """
        Set unit status to destroyed and play Impact sound
        """
        self.unit.status = "destroyed"
        self.state.notifyImpact()

    def run(self):
        # Compute new position using direction dictionary
        direction_dict = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        for direction, value in direction_dict.items():
            if direction == self.direction:
                new_pos = self.unit.position + value

        # Compute angle using angle dictionary
        angleDict = {"up": 90, "down": 270, "left": 180, "right": 0}
        for direction, value in angleDict.items():
            if direction == self.direction:
                self.unit.angle = value

        # If the player touches the window, he reappears on the other side
        if new_pos.x < 0:
            new_pos.x = self.state.worldWidth - 1
        elif new_pos.x > self.state.worldWidth - 1:
            new_pos.x = 0
        elif new_pos.y < 0:
            new_pos.y = self.state.worldHeight - 1
        elif new_pos.y > self.state.worldHeight - 1:
            new_pos.y = 0

        # If the player touches a body, set game status to Game Over
        for body in self.state.bodies:
            if new_pos == body.position:
                self.gameOver()
                return

        # If the player touches a wall, set game status to Game Over
        for y in range(self.state.worldHeight):
            for x in range(self.state.worldWidth):
                if self.state.walls[y][x] is not None and new_pos == Vector2(x, y):
                    self.gameOver()
                    return

        # Save new position and direction to unit
        self.unit.position = new_pos
        self.unit.direction = self.direction
        self.unit.slidePos = Vector2(0,0)

        # Add the new position to the position List
        self.state.positionList.append(self.unit.position)

        # Compute bodies positions
        index = 0
        for body in self.state.bodies:
            try:
                new_pos = self.state.positionList[-index-2]
            except IndexError:
                new_pos = body.position
            body.position = new_pos
            body.slidePos = Vector2(0,0)
            index += 1

        # Delete positions not used by player or bodies
        if len(self.state.positionList) > len(self.state.bodies) + 3:
            del self.state.positionList[-(len(self.state.bodies) + 4)]

        # Compute collision with Food
        food = next(obj for obj in self.state.units if isinstance(obj, Food))
        if self.unit.position == food.position:
            # Increment score
            self.state.score += 1
            if self.state.score >= self.state.scoreVictory:
                self.state.notifyLevelComplete()
                return
            self.state.foodMove = True
            # Add a Body to bodies list
            self.state.bodies.append(Body(self.state, self.state.positionList[1], Vector2(1, 0)))

            # Speed up over 5 scores
            scoreMult = self.state.score / 5
            if scoreMult.is_integer() and self.state.moveDelay >= self.state.moveDelayMin:
                self.state.moveDelay -= 1
                print("Speed Up ! ({})".format(self.state.moveDelay))

            # Notify Sound Layer
            self.state.notifyFoodCollide()
