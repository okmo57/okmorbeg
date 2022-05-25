from data import graph, provinces, subgraphs
from copy import deepcopy

a = 0
for subgraph in subgraphs:
    if len(subgraph) > 2000:
        a = subgraph
print(a)
b = {x: 0 for x in a}
print(b)
