from .Layer import Layer

class FoodLayer(Layer):
    def __init__(self, cellSize, imageFile, state, units):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.units = units

    def render(self, surface):
        for unit in self.units:
            self.renderTile(surface, unit.lastPos(), unit.tile, unit.slidePos, unit.borderPos, unit.angle)
