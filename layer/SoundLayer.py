from .Layer import Layer
from .Layer import resource_path
import pygame

class SoundLayer(Layer):
    def __init__(self, foodCollideFile, impactFile, victoryFile):
        self.foodCollideSound = pygame.mixer.Sound(resource_path("assets/sounds/{}".format(foodCollideFile)))
        self.foodCollideSound.set_volume(0.5)
        self.impactSound = pygame.mixer.Sound(resource_path("assets/sounds/{}".format(impactFile)))
        self.impactSound.set_volume(0.5)
        self.victorySound = pygame.mixer.Sound(resource_path("assets/sounds/{}".format(victoryFile)))
        self.victorySound.set_volume(0.5)

    def foodCollide(self):
        self.foodCollideSound.play()

    def impact(self):
        self.impactSound.play()

    def levelComplete(self):
        self.victorySound.play()

    def render(self, surface):
        pass
