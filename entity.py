import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity:
    def __init__(self, node):
        self.name = None
        self.directions = {UP: Vector2(0, -1), DOWN: Vector2(0, 1),
                           LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0), STOP: Vector2()}
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal and self.node.neighbors.get(PORTAL):
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def validDirection(self, direction):
        if direction != STOP and self.name in self.node.access.get(direction, []) and self.node.neighbors.get(direction):
            return True
        return False

    def getNewTarget(self, direction):
        return self.node.neighbors[direction] if self.validDirection(direction) else self.node

    def overshotTarget(self):
        if self.target:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            return vec2.magnitudeSquared() >= vec1.magnitudeSquared()
        return False

    def reverseDirection(self):
        self.direction *= -1
        self.node, self.target = self.target, self.node

    def oppositeDirection(self, direction):
        return direction != STOP and direction == self.direction * -1

    def validDirections(self):
        directions = [key for key in [UP, DOWN, LEFT, RIGHT] if self.validDirection(key) and key != self.direction * -1]
        return directions if directions else [self.direction * -1]

    def randomDirection(self, directions):
        return directions[randint(0, len(directions) - 1)]

    def goalDirection(self, directions):
        distances = [(self.node.position + self.directions[direction] * TILEWIDTH - self.goal).magnitudeSquared() for direction in directions]
        return directions[distances.index(min(distances))]

    def setStartNode(self, node):
        self.node = self.startNode = self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        if self.node.neighbors.get(direction):
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        if self.visible:
            if self.image:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                screen.blit(self.image, (self.position - adjust).asTuple())
            else:
                pygame.draw.circle(screen, self.color, self.position.asInt(), self.radius)
