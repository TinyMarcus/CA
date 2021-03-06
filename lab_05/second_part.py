import interpolation
import first_part
from math import *

Q_table = [[2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000, 26000],
           [1, 1, 1, 1.0001, 1.0025, 1.0198, 1.0895, 1.2827, 1.6973, 2.4616, 3.6552, 5.3749, 7.6838],
           [4, 4, 4.1598, 4.3006, 4.4392, 4.5661, 4.6817, 4.7923, 4.9099, 5.0511, 5.2354, 5.4841, 5.8181],
           [5.5, 5.5, 5.5116, 5.9790, 6.4749, 6.9590, 7.4145, 7.8370, 8.2289, 8.5970, 8.9509, 9.3018, 9.6621],
           [11] * 13,
           [15] * 13]
           
E_table = [0, 12.13, 20.98, 31, 45]

global x_global
x_global = [-5, 3, -2, -15, -40, -70]

def Q(i, T):
    table = []
    table.append(Q_table[0])
    table.append(Q_table[i])
    new_table = interpolation.approximation(table, T, 8)
    return interpolation.generate_polinom(new_table, T)
    
def find_col(a_copy, i_col):
    n = len(a_copy)
    a = [[a_copy[i][j] for j in range(0, n)] for i in range(0, n)]
    col = [0 for i in range(0, n)]
    
    for i in range(0, n):
        a[i].append(float(i == i_col))
    for i in range(0, n):
        if a[i][i] == 0:
            for j in range(i + 1, n):
                if a[j][j] != 0:
                    a[i], a[j] = a[j], a[i]
        for j in range(i + 1, n):
            d = -a[j][i] / a[i][i]
            for k in range(0, n + 1):
                a[j][k] += d * a[i][k]
    for i in range(n - 1, -1, -1):
        res = 0
        for j in range(0, n):
            res += a[i][j] * col[j]
        col[i] = (a[i][n] - res) / a[i][i]
    return col
    
def get_inverse(matrix):
    n = len(matrix)
    res = [[0 for i in range(0, n)] for j in range(0, n)]
    for i in range(0, n):
        col = find_col(matrix, i)
        for j in range(0, n):
            res[j][i] = col[j];
    return res
    
def times_mat_vec(mat, vec):
    res = [0 for i in range(len(mat))]
    
    for i in range(len(mat)):
        for j in range(len(mat)):
            res[i] += mat[i][j] * vec[j]    
    return res
    
def gamma(g, t, val):
    a = 5.87e+10 / (t**3)
    ev = exp(val[0])
    e2 = exp(val[2])
    e3 = exp(val[3])
    e4 = exp(val[4])
    e5 = exp(val[5])
    summ = e2 / (1 + g / 2) + 4 * e3 / (1 + 2 * g) + 9 * e4 / (1 + 4.5 * g) + 16 * e5 / (1 + 8 * g)
    func = a * (ev / (1 + g / 2) + summ)
    return g ** 2 - func
    
def find_gamma(T, val):
    return first_part.dichotomy(lambda g: gamma(g, T, val), 0, 2, 1e-4)
    
def alpha(t, val):
    return 0.285e-11 * (find_gamma(t, val) * t) ** 3
    
def e(i, t, val):
    g = find_gamma(t, val)
    #print(g)
    z = i - 1
    div = (1 + (z + 1) ** 2 * (g / 2)) / (1 + z ** 2 * (g / 2)) * (1 + g / 2)
    return 8.61 * 10 ** (-5) * t * log(div)
    
def k(i, t, val):
    q1 = Q(i, t)
    q2 = Q(i + 1, t)
    result = 2 * 2.415 * 10 ** (-3) * q2 / q1 * t ** (3 / 2)
    result = result * exp(-((E_table[i] - e(i, t, val)) * 11603) / t)
    return result
    
def equations(x, t, p):
    return [
            x[0] + x[2] - x[1] - log(k(1, t, x)),
            x[0] + x[3] - x[2] - log(k(2, t, x)),
            x[0] + x[4] - x[3] - log(k(3, t, x)),
            x[0] + x[5] - x[4] - log(k(4, t, x)),
            exp(x[0]) - sum([(i - 1) * exp(x[i]) for i in range(1, 6)]),
            p * 7242 / t - exp(x[0]) - sum([exp(x[i]) for i in range(1, 6)]) + alpha(t, x)
            ]
            
def P(p_beg, t_beg, t0, t2, m, z, p):
    x_old = [1] * 6
    t = t0 + (t2 - t0) * z ** m
    global x_global
    while fabs((x_old[0] - x_global[0]) / x_old[0]) >= 1e-4:
        for i in range(len(x_global)):
            x_old[i] = x_global[i]
        mat = [[1, -1, 1, 0, 0, 0],
               [1, 0, -1, 1, 0, 0],
               [1, 0, 0, -1, 1, 0],
               [1, 0, 0, 0, -1, 1],
               [exp(x_old[0]), 0, -exp(x_old[2]), -2 * exp(x_old[3]), -3 * exp(x_old[4]), -4 * exp(x_old[5])],
               [-exp(x_old[0]), -exp(x_old[1]), -exp(x_old[2]), -exp(x_old[3]), -exp(x_old[4]), -exp(x_old[5])]]
               
        w = get_inverse(mat)
        fun = equations(x_old, t, p)
        res = times_mat_vec(w, fun)
        x_global = []
        for i in range(len(res)):
            x_global.append(x_old[i] - res[i])
            
    return sum([exp(x_global[i]) for i in range(1, 6)])
    
def find_p(p_beg, t_beg, t0, tw, m):
    left = 3
    right = 25

    f_1 = 7242 * p_beg / t_beg
    return first_part.dichotomy(lambda p: f_1 - first_part.integral(lambda z: 2 * z * P(p_beg, t_beg, t0, tw, m, z, p), 0, 1, 40), left, right, 1e-4)
