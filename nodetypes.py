from util import randrange, clip
import random
import math

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
        randval = randrange(-1,1)
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

class InputOscillatorNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__()
        start = -1 if not random.randint(0,1) else 1
        self.curr = start

    def fwd(self):
        for node, w in self.connections:
            node.add_input(w * self.curr)
        self.curr *= -1

class OutputHorizontalMovementNode(Node):
    def fwd(self):
        movechance = clip(sum(self.inputs), -1, 1)
        move = math.copysign((abs(movechance) > random.random()), movechance)
        if move:
            self.owner.move(int(move), 0)
        self.inputs.clear()

class OutputVerticalMovementNode(Node):
    def fwd(self):
        movechance = clip(sum(self.inputs), -1, 1)
        move = math.copysign((abs(movechance) > random.random()), movechance)
        if move:
            self.owner.move(0, int(move))
        self.inputs.clear()

class HiddenNode(Node):
    def fwd(self):
        out = sum(self.inputs)
        self.inputs.clear()
        for node, w in self.connections:
            node.add_input(out * w)
