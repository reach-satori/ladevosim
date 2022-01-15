import itertools
import random
from collections import OrderedDict, defaultdict
from util import randrange, reverse_dictgraph, traverse_with
from nodetypes import InputRandomNode, InputConstNode, InputOscillatorNode, HiddenNode,\
    OutputHorizontalMovementNode, OutputVerticalMovementNode

NODESET = [
    [
        InputRandomNode,
        InputConstNode,
        InputOscillatorNode
    ],
    [
        HiddenNode,
        HiddenNode,
        HiddenNode
    ],
    [
        OutputHorizontalMovementNode,
        OutputVerticalMovementNode,
    ]
]


class Geneset:
    def __init__(self, connections):
        self.starts, self.ends = zip(*connections)
        self.weights = [randrange(-1,1) for i in range(len(connections))]
        self.idxdict = dict()
        self.update_idxdict()

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

    def mutate(self):
        choice = random.randint(0,2)
        conns = get_viable_connections()

        if choice == 0:
            pass
            # mutate startpoint
        elif choice == 1:
            pass
            # mutate endpoint
        elif choice == 2:
            pass
            # mutate weight

    def get_conn(self):
        return (self.end, self.weight)

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

@memoize
def get_viable_connections(nodeset=NODESET):
    print("run")
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

    return [list(i) for i in [first, second, third]]


def gen_geneset(nodeset, numgenes):
    first, second, third = get_viable_connections(nodeset)
    all_conns = list(first) + list(second) + list(third)
    if len(all_conns) <= numgenes:
        raise ValueError("Too many genes requested for the given geneset")

    # randomly choose connections
    chosen = random.sample(all_conns, numgenes)
    # make geneset
    geneset = Geneset(chosen)
    # get all connections that don't connect to an input or output to prune
    to_be_pruned = set(geneset.get_pruned_pairs())
    # prune useless nodes
    chosen = [tup for tup in chosen if tup not in to_be_pruned]
    # get unique nodes
    chosen_uniq = list(zip(*chosen))
    chosen_uniq = set(chosen_uniq[0]) | set(chosen_uniq[1]) if chosen_uniq else set()

    all_nodetypes = [node for nodetype in nodeset for node in nodetype]  # flattened list

    # create objects, sorted so input nodes get forwarded first
    actual_nodes = OrderedDict({idx:all_nodetypes[idx]() for idx in sorted(chosen_uniq)})
    for startnode, endnode in chosen:
        actual_nodes[startnode].connections.append(
            (actual_nodes[endnode],
             geneset.get_conn_weight((startnode, endnode))))

    # prune useless nodes for performance
    # (any sub-networks that aren't connected to any input or output nodes)

    return actual_nodes, geneset
