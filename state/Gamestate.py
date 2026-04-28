from pygame.math import Vector2

class GameState():
    def __init__(self, level):
        # Define time unit
        self.epoch = 0

        # Define world size
        self.worldSize = Vector2(30, 20)

        # Store level
        self.level = level

        # Define move delay depending on level
        self.moveDelays = [10, 10, 9, 8]
        self.moveDelay = self.moveDelays[self.level - 1]
        self.moveDelayMin = 7

        # Define score
        self.score = 0

        # Define victory score
        self.scoreVictory = 50

        # Define walls
        self.walls = [ [None ] * int(self.worldSize.x) ] * int(self.worldSize.y)

        # Set attribute to move food when colliding with player
        self.foodMove = False

        # Define units list
        self.units = []

        # Define observers lists
        self.observers = []

    # Set properties for world width and height
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    @property
    def worldHeight(self):
        return int(self.worldSize.y)

    def addObserver(self, observer):
        """
        Add a game state observer.
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)

    def notifyFoodCollide(self):
        for observer in self.observers:
            observer.foodCollide()

    def notifyImpact(self):
        for observer in self.observers:
            observer.impact()

    def notifyLevelComplete(self):
        for observer in self.observers:
            observer.levelComplete()
