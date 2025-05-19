from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
import math
'''
We define a rate, specify the range of dimension for which we solve the system, and initialise the matrix and vector.
'''
l = 0.25
n_values = range(2, 40)  # Range of n values to observe growth
solutions = []
'''
Solve the system and plot the solution
'''
for n in n_values:
    b = np.array([1 / (2 * i * l + i + 1) if i <= math.floor((n - 1) / 2) else 1 / (2 * (n - i - 1) * l + i + 1) for i in range(n - 1)] + [1 / n])
    diagonals = [
        [-(i + 1) / (2 * min(i, n - i - 1) * l + i + 1) for i in range(1, n)],                      # Sub-diagonal
        [1] * n,                                                                                    # Main diagonal
        [-(2 * min(i, n - i - 1) * l) / (2 * min(i, n - i - 1) * l + i + 1) for i in range(n - 1)]  # Super-diagonal
    ]
    A = diags(diagonals, offsets=[-1, 0, 1], shape=(n, n)).toarray()
    A[-1, -2:] = [-1, 1] 
    r = spsolve(A, b)
    solutions.append(r[-1]) 
plt.plot(n_values, solutions)
plt.show()