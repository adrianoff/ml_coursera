import scipy.linalg
from numpy import sin, exp

f_x = lambda x: sin(x / 5.0) * exp(x / 10.0) + 5 * exp(-x / 2.0)

polynom_rank = 1
A_1 = [
    [1 ** n for n in range(0, polynom_rank + 1)],
    [15 ** n for n in range(0, polynom_rank + 1)]
]

#print A_1
b_1 = [f_x(1), f_x(15)]
#print b_1

#print scipy.linalg.solve(A_1, b_1)

polynom_rank = 3
A_4 = [
    [1.0 ** n for n in range(0, polynom_rank + 1)],
    [4.0 ** n for n in range(0, polynom_rank + 1)],
    [10.0 ** n for n in range(0, polynom_rank + 1)],
    [15.0 ** n for n in range(0, polynom_rank + 1)]
]
print A_4
b_4 = [f_x(1.0), f_x(4.0), f_x(10.0),f_x(15.0)]
answer = scipy.linalg.solve(A_4, b_4)
#map(lambda x: x.round(2), answer)

for item in answer:
    print round(item, 7)
