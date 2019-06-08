from math import *

def integral(func, a, b, quan):
    step = (b - a) / quan
    res = 0.5 * (func(a) + func(b))
    
    for i in range(1, quan):
        res = res + func(a + i * step)
    res = res * step
    return res
    
def find_p(p_beg, t_beg, t0, tw, m):
    pt_1 = 7242 * p_beg / t_beg
    pt_2 = 2 * integral(lambda z: (z * 7242) / (t0 + (tw - t0) * z ** m), 0, 1, 40)
    
    return dichotomy(lambda x: pt_1 - pt_2 * x, 3, 25, 1e-4)
    
def dichotomy(func, beg, end, eps):
    if (beg > end):
        beg, end = end, beg
    left_edge = beg
    right_edge = end
    left_func = func(left_edge)
    middle = (right_edge + left_edge) / 2
    
    while fabs((right_edge - left_edge) / middle) >= eps:
        middle = (right_edge + left_edge) / 2
        middle_func = func(middle)
        
        if left_func * middle_func <= 0:
            right_edge = middle
            continue
            
        left_edge = middle
        left_func = middle_func
    
    return middle
