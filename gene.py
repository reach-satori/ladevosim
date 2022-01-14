import itertools
import random

class Gene:
    def __init__(self, startnode, endnode, weight):
        self.start = startnode
        self.end = endnode
        self.weight = weight

    def mutate(self):
        pass

    def get_conn(self):
        return (self.end, self.weight)

def gen_geneset(nodeset, numgenes):
    linputs, lhidden, loutputs = [len(i) for i in nodeset]

    # br for breakpoint
    br_1 = linputs
    br_2 = linputs + lhidden
    br_3 = linputs + lhidden + loutputs

    # first: all combinations of input and (hidden and output)
    first_connections = itertools.product(range(br_1), range(br_1, br_3))
    # second: all permutations of hidden pairs
    second_connections = itertools.product(range(br_1, br_2), repeat=2)
    # third: all combinations of hidden and outputs
    third_connections = itertools.product(range(br_1, br_2), range(br_2, br_3))

    all_conns = list(first_connections) + list(second_connections) + list(third_connections)
    if len(all_conns) <= numgenes:
        raise ValueError("Too many genes requested for the given geneset")

    chosen = random.sample(all_conns, numgenes)
    weights = [random.random()*2 - 1 for i in range(numgenes)]
    chosen_uniq = list(zip(*chosen))
    chosen_uniq = set(chosen_uniq[0]) | set(chosen_uniq[1])  # get unique nodes
    all_nodetypes = [node for nodetype in nodeset for node in nodetype]  # flattened list
    actual_nodes = {idx:all_nodetypes[idx]() for idx in chosen_uniq}  # create
    genes = []
    for weight, (startnode, endnode) in zip(weights, chosen):
        actual_nodes[startnode].connections.append((actual_nodes[endnode], weight))
        genes.append(Gene(startnode, endnode, weight))
