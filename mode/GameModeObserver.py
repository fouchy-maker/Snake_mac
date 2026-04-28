class GameModeObserver():
    def loadLevelRequested(self, fileName, level):
        pass
    def worldSizeChanged(self, worldSize):
        pass
    def showMenuRequested(self):
        pass
    def showGameRequested(self):
        pass
    def gameWon(self, level):
        pass
    def gameLost(self, score):
        pass
    def player1Win(self, score):
        pass
    def player2Win(self, score):
        pass
    def quitRequested(self):
        pass
    def musicChangedRequested(self, musicFile, volume, fadeOut=0):
        pass
