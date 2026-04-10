from .GameMode import GameMode
from state import GameState, Food
from layer import UnitLayer, ScoreLayer, SoundLayer, ArrayLayer
from command import MoveCommand, FoodCommand, SlideCommand
import pygame
from pygame.math import Vector2

class PlayGameMode(GameMode):
    def __init__(self, level):
        super().__init__()
        # Game State
        self.state = GameState(level)

        # Cell Size
        self.cellSize = Vector2(32, 32)

        # Layer List
        self.layers = [
            ArrayLayer(self.cellSize, "snake_fouchy32.png", self.state, self.state.walls, 0), # Walls
            UnitLayer(self.cellSize, "snake_fouchy32.png", self.state, self.state.units), # Units
            ScoreLayer(self.cellSize, None, self.state), # Score
            SoundLayer("gotFood.wav", "impact.wav", "victory.wav") # Sounds
        ]

        # All layers observe GameState
        for layer in self.layers:
            self.state.observers.append(layer)

        # Controls
        self.commands = []
        self.moveCommandList = []
        self.playerUnit = None
        self.gameOver = False

    # Set properties for cell width and height
    @property
    def cellWidth(self):
        return int(self.cellSize.x)
    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):
        if self.gameOver:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                elif event.key == pygame.K_UP:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "up"))
                elif event.key == pygame.K_DOWN:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "down"))
                elif event.key == pygame.K_LEFT:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "left"))
                elif event.key == pygame.K_RIGHT:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "right"))
                elif event.key == pygame.K_z:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "up"))
                elif event.key == pygame.K_s:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "down"))
                elif event.key == pygame.K_q:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "left"))
                elif event.key == pygame.K_d:
                    self.moveCommandList.append(MoveCommand(self.state, self.playerUnit, "right"))


    def update(self):
        for command in self.commands:
            command.run()
            self.commands.clear()
        if self.state.epoch-self.playerUnit.lastMoveEpoch >= self.state.moveDelay:
            self.playerUnit.lastMoveEpoch = self.state.epoch
            # Run Snake Command if the direction is different from player's or opposite
            while len(self.moveCommandList) > 0:
                dir_opp = {"up": "down", "down": "up", "left": "right", "right": "left"}
                firstCommand = self.moveCommandList[0]
                if not (firstCommand.direction == self.playerUnit.direction
                        or firstCommand.direction == dir_opp[self.playerUnit.direction]):
                    firstCommand.run()
                    del self.moveCommandList[0]
                    break
                del self.moveCommandList[0]
            # If Snake Command List is empty, run Command with snake position
            else:
                MoveCommand(self.state, self.playerUnit, self.playerUnit.direction).run()

            # Run Food Command
            if self.state.foodMove:
                for unit in self.state.units:
                    if isinstance(unit, Food):
                        command = FoodCommand(self.state, unit)
                        command.run()
                self.state.foodMove = False

            # Check Game Over
            if self.playerUnit.status != "alive":
                self.gameOver = True
                self.notifyGameLost(self.state.score)

            # Check Victory
            if self.state.score >= self.state.scoreVictory:
                self.gameOver = True
                self.notifyGameWon(self.state.level)

        # Run Slide Command
        SlideCommand(self.state, self.playerUnit, self.cellSize).run()
        for body in self.state.bodies:
            SlideCommand(self.state, body, self.cellSize).run()

        self.state.epoch += 1

    def render(self, window):
        window.fill((200, 150, 50))
        # Render Layers
        for layer in self.layers:
            layer.render(window)
