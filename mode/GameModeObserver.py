class GameModeObserver():
    def loadLevelRequested(self, fileName, level):
        pass
    def restartLevelRequested(self):
        pass
    def worldSizeChanged(self, worldSize):
        pass
    def showPlayerMenuRequested(self):
        pass
    def showOptionsMenuRequested(self):
        pass
    def showLevelMenuRequested(self, playerNumber):
        pass
    def showMainMenuRequested(self):
        pass
    def showGameRequested(self):
        pass
    def showRestartMenuRequested(self):
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
