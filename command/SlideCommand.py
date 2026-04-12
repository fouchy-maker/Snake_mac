from .Command import Command
from pygame.math import Vector2

class SlideCommand(Command):
    def __init__(self, gameState, unit, cellSize):
        self.state = gameState
        self.unit = unit
        self.cellSize = cellSize

    def borderCollide(self, value):
        if value.x > 1 or value.y > 1 or value.x < -1 or value.y < -1:
            return True
        else:
            return False

    def run(self):
        speed = self.cellSize.x / self.state.moveDelay
        value = self.unit.position - self.unit.lastPos()
        valueBorder = self.unit.position - self.unit.lastPos()

        # Going through window borders
        if self.borderCollide(value):
            if value.x > 1 :
                value.x = -1
            elif value.x < -1:
                value.x = 1
            elif value.y > 1:
                value.y = -1
            elif value.y < -1:
                value.y = 1

        self.unit.slidePos += value.elementwise() * speed

        # Compute position for rendering out of the border
        if self.borderCollide(valueBorder):
            windowSize = self.state.worldSize.elementwise() * self.cellSize
            if valueBorder.x > 1:
                self.unit.borderPos.x = self.unit.slidePos.x + windowSize.x
            elif valueBorder.x < -1:
                self.unit.borderPos.x = self.unit.slidePos.x - windowSize.x
            elif valueBorder.y > 1:
                self.unit.borderPos.y = self.unit.slidePos.y + windowSize.y
            elif valueBorder.y < 1:
                self.unit.borderPos.y = self.unit.slidePos.y - windowSize.y
        else:
            self.unit.borderPos = Vector2(0, 0)
