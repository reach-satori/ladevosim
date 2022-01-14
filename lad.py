import math
from util import clip
import random


class Lad:
    def __init__(self, x, y, world):
        global worldsize
        self.x = x
        self.y = y
        self.world = world
        self.world[x][y] = self

    def act(self):
        pass

    def get_rel_x(self):
        # -1 on left, 1 on right, 0 in middle
        return 2*(self.x / self.world.size[0]) - 1

    def get_rel_y(self):
        return 2*(self.y / self.world.size[1]) - 1

    def move(self, x, y):
        self.world[self.x][self.y] = None
        self.x = clip(x + self.x, 0, self.world.size[0]-1)
        self.y = clip(y + self.y, 0, self.world.size[1]-1)
        self.world[self.x][self.y] = self



def encode(weights, inoutpair, all_nodetypes):
    pass


class Node:
    def __init__(self):
        self.owner = None
        self.connections = []
        self.inputs = []

    def add_input(self, val):
        self.inputs.append(val)

    def fwd(self):
        raise NotImplementedError("Base class")

class InputRandomNode(Node):
    def fwd(self):
        randval = (random.random() * 2) - 1
        for node, w in self.connections:
            node.add_input(w * randval)

class InputConstNode(Node):
    def fwd(self):
        for node, w in self.connections:
            node.add_input(w * 1.)

class InputHorizontalLocationNode(Node):
    def fwd(self):
        xval = self.owner.get_rel_x()
        for node, w in self.connections:
            node.add_input(w * xval)

class InputVerticalLocationNode(Node):
    def fwd(self):
        yval = self.owner.get_rel_y()
        for node, w in self.connections:
            node.add_input(w * yval)

class OutputHorizontalMovementNode(Node):
    def fwd(self):
        movechance = clip(sum(self.inputs), -1, 1)
        move = math.copysign((abs(movechance) > random.random()), movechance)
        self.owner.move(int(move), 0)

class OutputVerticalMovementNode(Node):
    def fwd(self):
        movechance = clip(sum(self.inputs), -1, 1)
        move = math.copysign((abs(movechance) > random.random()), movechance)
        self.owner.move(0, int(move))

class HiddenNode(Node):
    def fwd(self):
        out = sum(self.inputs)
        for node, w in self.connections:
            node.add_input(out * w)
