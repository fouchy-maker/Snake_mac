from .Body import Body

class Body2(Body):
    def lastPos(self):
        return self.giveLastPos(self.state.players[1])