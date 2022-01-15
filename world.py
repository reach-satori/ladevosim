import random

class World:
    def __init__(self, size):
        self.map = [[None for i in range(size[1])] for j in range(size[0])]
        self.size = size
        self.lads = []

    def at(self, x, y):
        if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
            raise ValueError("Out of map bounds")
        return self.map[x][y]

    def reset_map(self):
        self.map = [[None for i in range(self.size[1])] for j in range(self.size[0])]

    def randomize_lad_pos(self):
        x, y = [random.randint(0, self.size[0]-1) for i in range(2)]
        for lad in self.lads:
            x, y = [random.randint(0, self.size[0]-1) for i in range(2)]
            lad.x, lad.y = x, y
            self.map[x][y] = lad

    def __getitem__(self, val):
        return self.map[val]
