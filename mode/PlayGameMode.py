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
        self.moveCommandList1 = []
        self.moveCommandList2 = []
        self.playerUnit = None
        self.player2Unit = None
        self.gameOver = False

    # Set properties for cell width and height
    @property
    def cellWidth(self):
        return int(self.cellSize.x)
    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def snakeCommand(self, moveCommandList, playerUnit):
        """
        Run Snake Command if the direction is different from player's or opposite.
        If command list is empty, run Command with current direction.
        """
        while len(moveCommandList) > 0:
            dir_opp = {"up": "down", "down": "up", "left": "right", "right": "left"}
            firstCommand = moveCommandList[0]
            if not (firstCommand.direction == playerUnit.direction
                    or firstCommand.direction == dir_opp[playerUnit.direction]):
                firstCommand.run()
                del moveCommandList[0]
                break
            del moveCommandList[0]
        else:
            MoveCommand(self.state, playerUnit, playerUnit.direction).run()

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
                    self.moveCommandList1.append(MoveCommand(self.state, self.playerUnit, "up"))
                elif event.key == pygame.K_DOWN:
                    self.moveCommandList1.append(MoveCommand(self.state, self.playerUnit, "down"))
                elif event.key == pygame.K_LEFT:
                    self.moveCommandList1.append(MoveCommand(self.state, self.playerUnit, "left"))
                elif event.key == pygame.K_RIGHT:
                    self.moveCommandList1.append(MoveCommand(self.state, self.playerUnit, "right"))
                elif event.key == pygame.K_z:
                    self.moveCommandList2.append(MoveCommand(self.state, self.player2Unit, "up"))
                elif event.key == pygame.K_s:
                    self.moveCommandList2.append(MoveCommand(self.state, self.player2Unit, "down"))
                elif event.key == pygame.K_q:
                    self.moveCommandList2.append(MoveCommand(self.state, self.player2Unit, "left"))
                elif event.key == pygame.K_d:
                    self.moveCommandList2.append(MoveCommand(self.state, self.player2Unit, "right"))


    def update(self):
        for command in self.commands:
            command.run()
            self.commands.clear()
        if self.state.epoch-self.playerUnit.lastMoveEpoch >= self.state.moveDelay:
            self.playerUnit.lastMoveEpoch = self.state.epoch

            # Run Snake Commands
            self.snakeCommand(self.moveCommandList1, self.playerUnit)
            self.snakeCommand(self.moveCommandList2, self.player2Unit)

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
                self.notifyPlayer2Win(self.state.score)
            elif self.player2Unit.status != "alive":
                self.gameOver = True
                self.notifyPlayer1Win(self.state.score)

            # Check Victory
            if self.state.score >= self.state.scoreVictory:
                self.gameOver = True
                self.notifyGameWon(self.state.level)

        # Run Slide Command
        SlideCommand(self.state, self.playerUnit, self.cellSize).run()
        SlideCommand(self.state, self.player2Unit, self.cellSize).run()
        for body in self.playerUnit.bodies:
            SlideCommand(self.state, body, self.cellSize).run()
        for body in self.player2Unit.bodies:
            SlideCommand(self.state, body, self.cellSize).run()

        self.state.epoch += 1

    def render(self, window):
        window.fill((200, 150, 50))
        # Render Layers
        for layer in self.layers:
            layer.render(window)
