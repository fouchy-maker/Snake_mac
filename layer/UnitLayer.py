from .Layer import Layer

class UnitLayer(Layer):
    def __init__(self, cellSize, imageFile, state, units):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.units = units

    def render(self, surface):
        bodies = self.state.units[0].bodies + self.state.units[1].bodies
        for body in bodies:
            self.renderTile(surface, body.lastPos(), body.tile, body.slidePos, body.borderPos)
        for unit in self.units:
            self.renderTile(surface, unit.lastPos(), unit.tile, unit.slidePos, unit.borderPos, unit.angle)
