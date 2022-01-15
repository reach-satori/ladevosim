from world import World
from lad import Lad
from copy import deepcopy
from gene import gen_geneset, NODESET
import random
import cv2
import numpy as np

def main():
    wsize = 100
    numlads = 100
    numgenes = 5
    sim_steps = 200
    mut_rate = 1
    print("Starting sim...")
    print(f"Generating world with size {wsize}x{wsize}...")
    world = World((wsize,wsize))
    lads = []

    # generating lads
    print(f"Generating {numlads} lads with {numgenes} genes each...")
    for i in range(numlads):
        geneset = gen_geneset(NODESET, numgenes)
        x, y = random.randint(0, wsize-1), random.randint(0, wsize-1)
        newlad = Lad(x, y, world, geneset)
        lads.append(newlad)

    cv2.namedWindow("sim", cv2.WINDOW_AUTOSIZE)
    # running simulation

    gen = 0
    while gen < 100:
        for i in range(sim_steps):
            for lad in lads:
                for node in lad.nodes.values():
                    node.fwd()
            frame = np.array(world.map, dtype=bool).astype(np.uint8) * 255
            cv2.imshow("sim", frame)
            cv2.waitKey(00) == ord('k')
            if cv2.waitKey(1) == ord('q'):
                break

        # kill them
        world.reset()
        for lad in lads[:]:
            if wsize//4 < lad.x < 3*wsize//4:
                lads.remove(lad)
                del lad
            else:
                x, y = random.randint(0, wsize-1), random.randint(0, wsize-1)
                world.map[x][y] = lad
                lad.x = x
                lad.y = y

        print(len(lads))
        print(np.sum(np.array(world.map, dtype=bool)))

        model_lads = random.choices(lads, k=numlads-len(lads))
        for model in model_lads:
            x, y = random.randint(0, wsize-1), random.randint(0, wsize-1)

            newgene = model.geneset.mutate() if random.random() > mut_rate else deepcopy(model.geneset)

            newlad = Lad(x, y, world, newgene)
            lads.append(newlad)

        gen += 1
        if gen % 1 == 0:
            print(f"Generation {gen} done")




if __name__ == "__main__":
    main()
