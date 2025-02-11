from constants import *

class MainMode:
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.time:
            self.toggleMode()

    def toggleMode(self):
        if self.mode == SCATTER:
            self.chase()
        elif self.mode == CHASE:
            self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

class ModeController:
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self, dt: float):
        self.mainmode.update(dt)
        self.checkCurrentMode()

    def checkCurrentMode(self):
        if self.current == FREIGHT:
            self.handleFreightMode()
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current == SPAWN and self.entity.node == self.entity.spawnNode:
            self.entity.normalMode()
            self.current = self.mainmode.mode

    def handleFreightMode(self):
        self.timer += 1
        if self.timer >= self.time:
            self.time = None
            self.entity.normalMode()
            self.current = self.mainmode.mode

    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current == FREIGHT:
            self.timer = 0

    def setSpawnMode(self):
        if self.current == FREIGHT:
            self.current = SPAWN
