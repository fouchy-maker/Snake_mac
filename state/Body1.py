from .Body import Body

class Body1(Body):
    def lastPos(self):
        return self.giveLastPos(self.state.players[0])