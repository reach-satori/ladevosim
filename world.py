

class World:
    def __init__(self, size):
        self.map = [[None for i in range(size[1])] for j in range(size[0])]
        self.size = size

    def at(self, x, y):
        if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
            raise ValueError("Out of map bounds")
        return self.map[x][y]

    def __getitem__(self, val):
        return self.map[val]
