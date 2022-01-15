from world import World
from lad import Lad
from gene import gen_geneset, NODESET
import random
# import cv2
# import numpy as np

def main():
    wsize = 50
    numlads = 100
    numgenes = 5
    sim_steps = 200
    mut_rate = 0.3
    print("Starting sim...")
    print(f"Generating world with size {wsize}x{wsize}...")
    world = World((wsize,wsize))
    lads = []

    # generating lads
    print(f"Generating {numlads} lads with {numgenes} genes each...")
    for i in range(numlads):
        nodes, geneset = gen_geneset(NODESET, numgenes)
        x, y = random.randint(0, wsize-1), random.randint(0, wsize-1)
        newlad = Lad(x, y, world, geneset, nodes)
        for node in newlad.nodes.values():
            node.owner = newlad
        lads.append(newlad)

    # cv2.namedWindow("sim", cv2.WINDOW_AUTOSIZE)
    # running simulation

    gen = 0
    while gen < 100:
        for i in range(sim_steps):
            # frame = np.array(world.map, dtype=bool).astype(np.uint8) * 255
            for lad in lads:
                for node in lad.nodes.values():
                    node.fwd()
            # cv2.imshow("sim", frame)
            # cv2.waitKey(00) == ord('k')
            # if cv2.waitKey(1) == ord('q'):
            #     break
        gen += 1
        if gen % 10 == 0:
            print(f"Generation {gen} done")


if __name__ == "__main__":
    main()
