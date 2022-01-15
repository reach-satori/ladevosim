import math
from util import clip, randrange
import random


class Lad:
    def __init__(self, x, y, world, genes):
        global worldsize
        self.x = x
        self.y = y
        self.world = world
        self.world[x][y] = self
        self.geneset = genes
        self.geneset.owner = self
        self.nodes = genes.get_final_connections()
        for node in self.nodes.values():
            node.owner = self

    def act(self):
        pass

    def get_rel_x(self):
        # -1 on left, 1 on right, 0 in middle
        return 2*(self.x / self.world.size[0]) - 1

    def get_rel_y(self):
        return 2*(self.y / self.world.size[1]) - 1

    def move(self, x, y):
        newx = clip(x + self.x, 0, self.world.size[0]-1)
        newy = clip(y + self.y, 0, self.world.size[1]-1)
        if not self.world[newx][newy]:
            self.world[self.x][self.y] = None
            self.x = newx
            self.y = newy
            # print(f"moving to {self.x}, {self.y}")
            self.world[self.x][self.y] = self
