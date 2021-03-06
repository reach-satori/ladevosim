import itertools
import random
from copy import deepcopy
from collections import defaultdict
from util import randrange, reverse_dictgraph, traverse_with
from nodetypes import InputRandomNode, InputConstNode, InputOscillatorNode, InputAgeNode,\
    InputHorizontalLocationNode, InputVerticalLocationNode,\
    HiddenNode,\
    OutputHorizontalMovementNode, OutputVerticalMovementNode, OutputDummy

NODESET = [
    [
        InputRandomNode,
        InputConstNode,
        InputOscillatorNode,
        InputAgeNode,
        InputHorizontalLocationNode,
        InputVerticalLocationNode
    ],
    [
        HiddenNode,
        HiddenNode,
        HiddenNode
    ],
    [
        OutputHorizontalMovementNode,
        OutputVerticalMovementNode,
        OutputDummy
    ]
]


class Geneset:
    weightrange = (-4, 4)

    def __init__(self, connections):
        # geneset represents connections as such:
        # starts, ends and weights are lists of equal length. so at index 0, you know there's a connection
        # between starts[0] and ends[0] with weight weights[0]
        self.starts, self.ends = (list(i) for i in zip(*connections))
        self.weights = [randrange(*self.weightrange) for i in range(len(connections))]
        self.idxdict = dict()
        self.update_idxdict()
        self.owner = None

    def __len__(self):
        return len(self.starts)

    # defining this severely speeds up deep copying operations which are a major part of
    # mutation and reproduction
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        result.starts, result.ends = self.starts.copy(), self.ends.copy()
        result.weights = self.weights.copy()
        result.idxdict = self.idxdict.copy()
        result.owner = self.owner
        return result

    def update_idxdict(self):
        tups = zip(self.starts, self.ends)
        self.idxdict = {tup: i for i, tup in enumerate(tups)}

    def get_conn_weight(self, pair):
        return self.weights[self.idxdict[pair]]

    def get_pruned_pairs(self):
        chosen = list(zip(self.starts, self.ends))
        # make graphs and traverse them to find which genes(connections)
        # don't contribute to behaviour
        first, second, third = get_viable_connections()
        graph = defaultdict(set)
        for n_in, n_out in chosen:
            graph[n_in].add(n_out)

        inputs = set(list(zip(*first))[0])
        outputs = set(list(zip(*third))[1])

        input_visited = set()
        for inp in inputs:
            input_visited = input_visited | set(traverse_with(graph, inp))

        graph = reverse_dictgraph(graph)

        output_visited = set()
        for out in outputs:
            output_visited = output_visited | set(traverse_with(graph, out))

        # useful graphs are only those where both inputs and outputs are present
        good_nodes = input_visited & output_visited

        # returns the tuples that are supposed to be pruned
        bad_connections = [(i, j) for i, j in chosen if (i not in good_nodes or j not in good_nodes)]
        return bad_connections

    def get_final_connections(self):
        chosen = zip(self.starts, self.ends)
        # get all connections that don't connect to an input or output to prune
        to_be_pruned = set(self.get_pruned_pairs())
        # prune useless nodes
        chosen = [tup for tup in chosen if tup not in to_be_pruned]
        # get unique nodes
        chosen_uniq = list(zip(*chosen))
        chosen_uniq = set(chosen_uniq[0]) | set(chosen_uniq[1]) if chosen_uniq else set()

        all_nodetypes = [node for nodetype in NODESET for node in nodetype]  # flattened list

        # create objects, sorted so input nodes get forwarded first
        actual_nodes = dict({idx:all_nodetypes[idx]() for idx in sorted(chosen_uniq)})
        for startnode, endnode in chosen:
            actual_nodes[startnode].connections.append(
                (actual_nodes[endnode],
                 self.get_conn_weight((startnode, endnode))))

        return actual_nodes

    def mutate(self):
        newgene = deepcopy(self)
        newgene.owner = None

        choice = random.randint(0,3)
        conns = get_viable_connections()
        conns = [conn for sublist in conns for conn in sublist]  # flattened list
        mutgene = random.randint(0, len(newgene)-1)

        if choice == 0:
            # mutate startpoint
            possibilities = set([conn[0] for conn in conns if conn[1] == newgene.ends[mutgene]])
            possibilities.remove(newgene.starts[mutgene])
            chosen = random.sample(possibilities, 1)[0]
            newgene.starts[mutgene] = chosen
        elif choice == 1:
            # mutate endpoint
            possibilities = set([conn[1] for conn in conns if conn[0] == newgene.starts[mutgene]])
            possibilities.remove(newgene.ends[mutgene])
            chosen = random.sample(possibilities, 1)[0]
            newgene.ends[mutgene] = chosen
        elif choice == 2:
            # mutate weight
            newgene.weights[mutgene] = randrange(*self.weightrange)
        elif choice == 3:
            # mutate entire connection
            chosen = random.sample(conns, 1)[0]
            newgene.starts[mutgene] = chosen[0]
            newgene.ends[mutgene] = chosen[1]

        # reset all nodes if mutation happened
        if choice in [0, 1, 3]:
            newgene.update_idxdict()
            newgene.nodes = newgene.get_final_connections()
            for node in newgene.nodes.values():
                node.owner = newgene
        return newgene

def memoize(func):
    memo = None

    def wrapper(*args, **kwargs):
        nonlocal memo
        if memo:
            return memo
        else:
            rv = func(*args, **kwargs)
            memo = rv
            return rv
    return wrapper

# this is the equivalent of a c++ static function so we memoize the output
@memoize
def get_viable_connections(nodeset=NODESET):
    linputs, lhidden, loutputs = [len(i) for i in nodeset]

    # br for breakpoint
    br_1 = linputs
    br_2 = linputs + lhidden
    br_3 = linputs + lhidden + loutputs

    # first: all combinations of input and (hidden and output)
    first = itertools.product(range(br_1), range(br_1, br_3))
    # second: all permutations of hidden pairs
    second = itertools.product(range(br_1, br_2), repeat=2)
    # third: all combinations of hidden and outputs
    third = itertools.product(range(br_1, br_2), range(br_2, br_3))

    out = [list(i) for i in [first, second, third]]
    print("Number of viable connections:", sum(len(i) for i in out))
    return out


def gen_geneset(nodeset, numgenes):
    first, second, third = get_viable_connections(nodeset)
    all_conns = list(first) + list(second) + list(third)
    if len(all_conns) <= numgenes:
        raise ValueError("Too many genes requested for the given geneset")

    # randomly choose connections
    chosen = random.sample(all_conns, numgenes)
    # make geneset
    geneset = Geneset(chosen)
    return geneset
