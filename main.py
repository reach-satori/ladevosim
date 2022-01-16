import random
from copy import deepcopy
from multiprocessing import Process, Queue
from queue import Empty
from os import mkdir


from world import World
from lad import Lad
from gene import gen_geneset, NODESET

import numpy as np

def main(numgenes):
    # numgenes = 3
    wsize = 100
    numlads = 300
    sim_steps = 200
    mut_rate = 0.3
    maxgen = 150
    save_vid_gens = [0, 5, 10, 40, 60, 100, 149]
    world = World((wsize,wsize), sim_steps)
    print("Starting sim...")
    print(f"Generating world with size {wsize}x{wsize}...")

    # generating lads
    print(f"Generating {numlads} lads with {numgenes} genes each...")
    for i in range(numlads):
        geneset = gen_geneset(NODESET, numgenes)
        newlad = Lad(world, geneset)
        world.lads.append(newlad)
    world.randomize_lad_pos()

    # running simulation

    if save_vid_gens:

        import cv2
        import numpy as np

        def image_recorder(queue):
            while True:
                try:
                    img, index, gen, genes = queue.get(timeout=100)
                except Empty:
                    break
                if img == "DONE":
                    break
                cv2.imwrite(f"vis/g{gen}_i{index}_genes{genes}.png", cv2.resize(img, dsize=(400,400)))


        imgqueue = Queue()
        proc = Process(target=image_recorder, args=(imgqueue,))
        proc.start()

    gen = 0
    deaths = []
    while gen < maxgen:
        print(f"Generation {gen} simulation starting...")
        for i in range(sim_steps):
            world.simstep = i
            for lad in world.lads:
                for node in lad.nodes.values():
                    node.fwd()

            if gen in save_vid_gens:
                imgqueue.put((np.array(world.map, dtype=bool).astype(np.uint8)*255, i, gen, numgenes))

            # mid_simulation kill
            # if i == 100:
            #     kill = lambda x: ((x.x <= wsize//2 and x.y <= wsize//2) or (x.x >= wsize//2 and x.y >= wsize//2))
                # world.kill_lads(kill)

        print("Simulation done. Killing old lads...")

        # KILL THEM !!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!! !

        # two quadrants kill
        kill = lambda x: ((x.x > wsize//2 and x.y <= wsize//2) or (x.x <= wsize//2 and x.y >= wsize//2))

        # first y edge kill, then x edge kill
        # if gen > 50:
        #     kill = lambda dude: (wsize//4 < dude.x < 3*wsize//4)
        # else:
        #     kill = lambda dude: (wsize//4 < dude.y < 3*wsize//4)

        # x edge strip kill
        # kill = lambda dude: (wsize//4 > dude.x or dude.x > 3*wsize//4)

        # x center strip kill
        # kill = lambda dude: (wsize//4 < dude.x < 3*wsize//4)

        # all edges kill
        # kill = lambda dude: any([wsize//3 > dude.x,
        #                          wsize//3 > dude.y,
        #                          2*wsize//3 < dude.x,
        #                          2*wsize//3 < dude.y])
        world.kill_lads(kill)
        deadlads = numlads - len(world.lads)
        print(f"Dead lads: {deadlads}, {(deadlads*100/numlads):.1f}% of the population. "
              "Reproducing and mutating...")
        deaths.append(deadlads/numlads)

        model_lads = random.choices(world.lads, k=deadlads)
        for model in model_lads:
            newgene = model.geneset.mutate() if random.random() > mut_rate else deepcopy(model.geneset)
            newlad = Lad(world, newgene)
            world.lads.append(newlad)
        world.reset_map()
        world.randomize_lad_pos()

        gen += 1

    tdir = "left_then_right"
    np.save(f"vis/{tdir}/{numgenes}genes_deaths", np.array(deaths))
    lads = random.sample(world.lads, 5)
    for i, lad in enumerate(lads):
        write_graph(lad,f"vis/{tdir}/{numgenes}_{i}.gv")

    if save_vid_gens:
        imgqueue.put(("DONE","DONE","DONE", "DONE"))
        proc.join()


def write_graph(lad, filename):
    import graphviz
    nodes = [node.__name__ for nodetype in NODESET for node in nodetype]  # flattened list
    first, second, third = (len(n) for n in NODESET)
    hiddennames = "abcdefghijklmnopqrstuvxwyz"
    i = 0
    for j, node in enumerate(nodes[:]):
        if node == "HiddenNode":
            nodes[j] += hiddennames[i]
            i += 1


    g = graphviz.Digraph(filename=filename, format="png",)
    purged = lad.geneset.get_pruned_pairs()
    gene = lad.geneset

    for start, end, weight in zip(gene.starts, gene.ends, gene.weights):
        if (start, end) in purged:
            continue

        if start < first:
            g.node(nodes[start], color="magenta")
        elif (first+second) > start >= first:
            g.node(nodes[start], color="blue")
        else:
            g.node(nodes[start], color="orange")

        if end < first:
            g.node(nodes[end], color="magenta")
        elif (first+second) > end >= first:
            g.node(nodes[end], color="blue")
        else:
            g.node(nodes[end], color="orange")

        edgethick = str(abs(weight))
        color = "red" if weight < 0 else "green"
        g.edge(nodes[start], nodes[end], color=color, penwidth=edgethick)
    g.view()




if __name__ == "__main__":
    for numgenes in [10, 15, 20]:
        main(numgenes)
