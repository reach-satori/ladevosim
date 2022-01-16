import random

class World:
    def __init__(self, size, maxsim):
        self.map = [[None for i in range(size[1])] for j in range(size[0])]
        self.size = size
        self.lads = []
        self.simstep = 0
        self.max_simstep = maxsim

    def at(self, x, y):
        if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
            raise ValueError("Out of map bounds")
        return self.map[x][y]

    def get_age(self):
        return self.simstep / self.max_simstep

    def kill_lads(self, killfunc):
        new = []
        for lad in self.lads:
            if killfunc(lad):
                self.map[lad.x][lad.y] = None
            else:
                new.append(lad)

        del self.lads
        self.lads = new

    def reset_map(self):
        self.map = [[None for i in range(self.size[1])] for j in range(self.size[0])]
        self.simstep = 0

    def randomize_lad_pos(self):
        x, y = [random.randint(0, self.size[0]-1) for i in range(2)]
        for lad in self.lads:
            x, y = [random.randint(0, self.size[0]-1) for i in range(2)]
            self.map[x][y] = lad
            lad.x, lad.y = x, y

    def __getitem__(self, val):
        return self.map[val]
