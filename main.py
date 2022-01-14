from world import World
from lad import Lad
from sim_globals import full_nodeset
from gene import gen_geneset

# import numpy as np

def main():
    world = World((10,10))
    lad = Lad(3,5,world)

    gen_geneset(full_nodeset, 4)
    exit()


if __name__ == "__main__":
    main()
