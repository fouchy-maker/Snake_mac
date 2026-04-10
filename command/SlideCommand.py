from .Command import Command

class SlideCommand(Command):
    def __init__(self, gameState, unit, cellSize):
        self.state = gameState
        self.unit = unit
        self.cellSize = cellSize

    def run(self):
        speed = self.cellSize.x / self.state.moveDelay
        value = self.unit.position - self.unit.lastPos()
        if value.x > 1 :
            value.x = -1
        elif value.x < -1:
            value.x = 1
        if value.y > 1:
            value.y = -1
        elif value.y < -1:
            value.y = 1
        self.unit.slidePos += value.elementwise() * speed
