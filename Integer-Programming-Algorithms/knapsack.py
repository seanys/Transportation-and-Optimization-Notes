#
# Example of a knapsack problem formulated with the Xpress Python interface
#

import xpress as xp

S = range(5)          # that's the set {0,1,2,3,4}
value = [102, 512, 218, 332, 41]  # or just read them from file
weight = [21, 98, 44, 59, 9]

x = [xp.var(vartype=xp.binary) for i in S]
profit = xp.Sum(value[i] * x[i] for i in S)

p = xp.problem("knapsack")

p.addVariable(x)
p.addConstraint(xp.Sum(weight[i] * x[i] for i in S) <= 130)
p.setObjective(profit, sense=xp.maximize)

# A more compact (and equivalent) problem construction:
#
# p = xp.problem(x, xp.Sum(weight[i] * x[i] for i in S) <= 130, profit, sense=xp.maximize, name="knapsack")

p.solve()