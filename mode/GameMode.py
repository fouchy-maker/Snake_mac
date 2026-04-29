class GameMode():
    def __init__(self):
        self.__observers = []
    def addObserver(self, observer):
        self.__observers.append(observer)
    def notifyLoadLevelRequested(self, fileName, level):
        for observer in self.__observers:
            observer.loadLevelRequested(fileName, level)
    def notifyWorldSizeChanged(self, worldSize):
        for observer in self.__observers:
            observer.worldSizeChanged(worldSize)
    def notifyShowPlayerMenuRequested(self):
        for observer in self.__observers:
            observer.showPlayerMenuRequested()
    def notifyShowOptionsMenuRequested(self):
        for observer in self.__observers:
            observer.showOptionsMenuRequested()
    def notifyShowLevelMenuRequested(self, playerNumber):
        for observer in self.__observers:
            observer.showLevelMenuRequested(playerNumber)
    def notifyShowMainMenuRequested(self):
        for observer in self.__observers:
            observer.showMainMenuRequested()
    def notifyShowGameRequested(self):
        for observer in self.__observers:
            observer.showGameRequested()
    def notifyGameWon(self, level):
        for observer in self.__observers:
            observer.gameWon(level)
    def notifyGameLost(self, score):
        for observer in self.__observers:
            observer.gameLost(score)
    def notifyPlayer1Win(self, score):
        for observer in self.__observers:
            observer.player1Win(score)
    def notifyPlayer2Win(self, score):
        for observer in self.__observers:
            observer.player2Win(score)
    def notifyQuitRequested(self):
        for observer in self.__observers:
            observer.quitRequested()
    def notifyMusicChangedRequested(self, musicFile, volume, fadeOut=0):
        for observer in self.__observers:
            observer.musicChangedRequested(musicFile, volume, fadeOut)

    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()
