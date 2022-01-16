from util import randrange, clip
import random
import math

class Node:
    def __init__(self):
        self.owner = None
        self.connections = []
        self.inputs = []

    def fwd(self):
        raise NotImplementedError("Base class")

class InputAgeNode(Node):
    def fwd(self):
        for node, w in self.connections:
            node.inputs.append(w * self.owner.world.get_age())

class InputRandomNode(Node):
    def fwd(self):
        for node, w in self.connections:
            node.inputs.append(w*randrange(-1,1))

class InputConstNode(Node):
    def fwd(self):
        for node, w in self.connections:
            node.inputs.append(w)

class InputHorizontalLocationNode(Node):
    def fwd(self):
        xval = self.owner.get_rel_x()
        for node, w in self.connections:
            node.inputs.append(w * xval)

class InputVerticalLocationNode(Node):
    def fwd(self):
        yval = self.owner.get_rel_y()
        for node, w in self.connections:
            node.inputs.append(w * yval)

class InputOscillatorNode(Node):
    def fwd(self):
        for node, w in self.connections:
            node.inputs.append(math.sin((math.pi * self.owner.world.simstep)/(10*w)))

class OutputHorizontalMovementNode(Node):
    def fwd(self):
        movechance = math.tanh(sum(self.inputs))
        move = math.copysign((abs(movechance) > random.random()), movechance)
        if move:
            self.owner.move(int(move), 0)
        self.inputs.clear()

class OutputVerticalMovementNode(Node):
    def fwd(self):
        movechance = math.tanh(sum(self.inputs))
        move = math.copysign((abs(movechance) > random.random()), movechance)
        if move:
            self.owner.move(0, int(move))
        self.inputs.clear()

class OutputDummy(Node):
    def fwd(self):
        self.inputs.clear()

class HiddenNode(Node):
    def fwd(self):
        out = clip(sum(self.inputs), -10, 10)
        self.inputs.clear()
        for node, w in self.connections:
            node.inputs.append(out * w)
