from sympy import symbols, Rational
import sympy.plotting as spp
from sympy.matrices import Matrix
'''
We define a sympy symbol, specify the dimension of the system, and initialise the matrix and vector.
'''
l = symbols("l")
n = 5
b = [1/(2*l + i + 1) for i in range(n - 1)] + [Rational(1, n)]
A = []
for i in range(n - 1):
    A.append([-(i + 1)/(2*l + i + 1) if i == j + 1 else 1 if i == j else -(2 * l)/(2*l + i + 1) if i == j - 1 else 0 for j in range(n)])
A.append([0 for _ in range(n-2)] + [-1, 1])
'''
We solve the system, and plot the result.
'''
r = Matrix(A).LUsolve(Matrix(b))
p1 = spp.plot(r[-1], (l, 0, 3), show=False)
p1.show()