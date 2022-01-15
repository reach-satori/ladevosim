import random
from collections import defaultdict, deque

def clip(val, minv, maxv):
    return min(max(minv, val), maxv)

def randrange(low, hi):
    width = hi - low
    return (random.random() * width) + low

def reverse_dictgraph(graph):
    out = defaultdict(set)

    for k, vset in graph.items():
        for v in vset:
            out[v].add(k)
    return out

def traverse_with(graph, start):
    output = set()
    queue = deque([start])
    while queue:
        output.add(queue[0])
        nextnodes = graph.get(queue[0])
        if nextnodes:
            [queue.append(node) for node in nextnodes if node not in output]
        queue.popleft()
    return output

def get_viable_choices(start=None, end=None):
    if not (bool(start) ^ bool(end)):
        raise ValueError("No start or end point designated")
