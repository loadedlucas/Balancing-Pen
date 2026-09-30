from sympy import *
import numpy as np
x = Matrix([1,2,3])
y = Matrix([3,2,1])
print(sqrt(x.T * x))
q = Matrix.vstack(x, y)
print(q)
print(x.T * y)
exit()
a,b,c = symbols('a, b, c')
eq1 = Eq(np.dot(np.array(a), np.array(b)), 3)
sol = solve([eq1], [a,b])
soln = [tuple(v.evalf() for v in s) for s in sol]
print(sol)
print(soln)

