from __future__ import print_function
import xpress as xp
import numpy as np

def cb_preintsol(prob, data, isheur=True, cutoff=0):
    '''Callback for checking if solution is acceptable
    '''

    n = data
    xsol = []
    prob.getlpsol(x=xsol)
    xsol = np.array(xsol).reshape(n,n)
    nextc = np.argmax(xsol, axis=1)

    i = 0
    ncities = 1

    # Scan cities in order until we get back to 0 or the solution is
    # wrong and we're diverging
    while nextc[i] != 0 and ncities < n:
        ncities += 1
        i = nextc[i]

    # If the cities visited before getting back to 0 is less than n-1,
    # we just closed a subtour, hence the solution is infeasible
    return (ncities < n-1, None)


def cb_optnode(prob, data):
    '''Callback used after LP solution is known at BB node. Add subtour elimination cuts
    '''

    n = data
    xsol=[]
    prob.getlpsol(x=xsol)

    xsolf = np.array(xsol)  # flattened
    xsol  = xsolf.reshape(n,n)  # matrix-shaped

    # Obtain an order by checking the maximum of the variable matrix
    # for each row
    nextc = np.argmax(xsol, axis=1)
    unchecked = np.zeros(n)
    ngroup = 0

    # Initialize the vectors to be passed to addcuts

    cut_mstart = [0]
    cut_ind = []
    cut_coe = []
    cut_rhs = []

    nnz = 0
    ncuts = 0

    while np.min(unchecked) == 0 and ngroup <= n:
        '''Seek a tour
        '''

        ngroup += 1

        firstcity = np.argmin(unchecked)

        assert (unchecked[firstcity] == 0)

        i = firstcity
        ncities = 0

        # Scan cities in order
        while True:

            unchecked[i] = ngroup  # mark city i with its new group, to be used in addcut
            ncities += 1
            i = nextc[i]

            if i == firstcity or ncities > n + 1:
                break

        if ncities == n and i == firstcity:
            return 0  # Nothing to add, solution is feasible

        # unchecked[unchecked == ngroup] marks nodes to be made part of subtour
        # elimination inequality

        # Find indices of current subtour. S is the set of nodes
        # traversed by the subtour, compS is its complement.
        S     = np.where(unchecked == ngroup)[0].tolist()
        compS = np.where(unchecked != ngroup)[0].tolist()

        indices = [i*n+j for i in S for j in compS]

        # Check if solution violates the cut, and if so add the cut to
        # the list.
        if sum(xsolf[i] for i in indices) < 1 - 1e-3:

            mcolsp, dvalp = [], []

            # Presolve cut in order to add it to the presolved problem
            # (the problem currently being solved by the
            # branch-and-bound).
            drhsp, status = prob.presolverow('G', indices, np.ones(len(indices)), 1,
                                             prob.attributes.cols,
                                             mcolsp, dvalp)

            nnz += len(mcolsp)
            ncuts += 1

            cut_ind.extend(mcolsp)
            cut_coe.extend(dvalp)
            cut_rhs.append(drhsp)
            cut_mstart.append(nnz)

    if ncuts > 0:

        assert (len(cut_mstart) == ncuts + 1)
        assert (len(cut_ind) == nnz)

        if status >= 0:
            prob.addcuts([0] * ncuts, ['G'] * ncuts, cut_rhs, cut_mstart, cut_ind, cut_coe)

    return 0


def print_sol(p, n):
    '''Print the solution: order of nodes and cost
    '''

    xsol = np.array(p.getSolution()).reshape(n,n)
    nextc = np.argmax(xsol, axis=1)

    i = 0

    # Scan cities in order
    while nextc[i] != 0:
        print (i, '->', end='', sep='')
        i = nextc[i]

    print('0; cost:', p.getObjVal())


def create_initial_tour(n):
    '''Returns a permuted trivial solution 0->1->2->...->(n-1)->0
    '''

    p = np.random.permutation(n)
    P = np.eye(n)[p]  # random permutation

    I = np.eye(n)
    S = np.vstack((I[1:,:],I[0,:]))  # Creates trivial tour
    return np.dot(P.T, S, P).flatten()  # Permutes the tour


def solve_opttour():
    '''Create a random TSP problem
    '''

    n = 100
    CITIES = range(n)  # set of cities: 0..n-1

    X = 100 * np.random.rand(n)
    Y = 100 * np.random.rand(n)

    np.random.seed(3)

    # Compute distance matrix
    dist = np.ceil(np.sqrt ((X.reshape(n,1) - X.reshape(1,n))**2 +
                            (Y.reshape(n,1) - Y.reshape(1,n))**2))

    # Create variables as a square matrix of binary variables
    fly = np.array([xp.var(vartype=xp.binary, name='x_{0}_{1}'.format(i,j)) for i in CITIES for j in CITIES]).reshape(n,n)

    p = xp.problem()
    p.addVariable(fly)

    # Degree constraints
    p.addConstraint(xp.Sum(fly[i,:]) - fly[i,i] == 1  for i in CITIES)
    p.addConstraint(xp.Sum(fly[:,i]) - fly[i,i] == 1  for i in CITIES)

    # Objective function
    p.setObjective (xp.Sum((dist * fly).flatten()))

    # Add callbacks
    p.addcbpreintsol(cb_preintsol, n)
    p.addcboptnode(cb_optnode, n)

    # Disable dual reductions (in order not to cut optimal solutions)
    # and nonlinear reductions, in order to be able to presolve the
    # cuts. Bits 1, 8, and 64 are for singleton column removal, dual
    # reductions, and duplicate column removal. Bit 1024 is to avoid
    # global domain change.

    p.controls.presolveops &= ~(1 | 8 | 64)
    p.controls.presolveops |= 1024

    p.controls.mippresolve &= ~16

    # Disable symmetry detection
    p.controls.symmetry = 0

    # Create 10 trivial solutions: simple tour 0->1->2...->n->0
    # randomly permuted
    for k in range(10):
        InitTour = create_initial_tour(n)
        p.addmipsol(mipsolval=InitTour, solname="InitTour_{}".format(k))

    # p.controls.maxtime=-2  # set a time limit
    p.solve()

    print_sol(p,n)  # print solution and cost


if __name__ == '__main__':
    solve_opttour()