#
# Example: solving a min-cost-flow problem
# using the Xpress Python interface
#

from __future__ import print_function

try:
    import networkx as netx  # nice (di-)graph Python package
except ImportError:
    print("Install the NetworkX Python package to use this example")
    quit()

import numpy as np  # for matrix and vector products
import xpress as xp

# digraph definition

V = [1, 2, 3, 4, 5]                                   # vertices
E = [[1, 2], [1, 4], [2, 3], [3, 4], [4, 5], [5, 1]]  # arcs

n = len(V)  # number of nodes
m = len(E)  # number of arcs

G = netx.DiGraph(E)

# Get NumPy representation
A = (netx.incidence_matrix(G, oriented=True).toarray())

print("incidence matrix:\n", A)

# One (random) demand for each node
demand = np.random.randint(100, size=n)
# Balance demand at nodes
demand[0] = - sum(demand[1:])

cost = np.random.randint(20, size=m)  # (Random) costs

flow = np.array([xp.var() for i in E])  # flow variables declared on arcs

p = xp.problem('network flow')

p.addVariable(flow)
p.addConstraint(xp.Dot(A, flow) == - demand)
p.setObjective(xp.Dot(cost, flow))

p.solve()

for i in range(m):
    print('flow on', E[i], ':', p.getSolution(flow[i]))