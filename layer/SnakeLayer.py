from .Layer import Layer

class SnakeLayer(Layer):
    def __init__(self, cellSize, imageFile, state, units):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.units = units

    def render(self, surface):
        for player in self.state.players:
            for body in player.bodies:
                self.renderTile(surface, body.lastPos(), body.tile, body.slidePos, body.borderPos)
        for unit in self.units:
            self.renderTile(surface, unit.lastPos(), unit.tile, unit.slidePos, unit.borderPos, unit.angle)
