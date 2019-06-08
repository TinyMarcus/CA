from math import cos, sin, pi
 
def find_start(table, x, n):
    start = -1
    for i in range(len(table[0])):
        if table[0][i] >= x:
            start = i - 1
            break
 
    if start == -1:
        start = len(table[0]) - n + 1
 
    if start <= (n + 1) // 2 - 1:
        start = 0
    else:
        start -= (n + 1) // 2 - 1
 
    if len(table[0]) - start < (n + 1) // 2:
        start = len(table[0]) - (n + 1) // 2
 
    return int(start)
  
def approximation(table, x, n):
    new_table = []
 
    for i in range(2 * n + 1):
        new_table.append([' '] * (n + 2))
 
    j = find_start(table, x, n)
    for i in range(0, len(new_table), 2):
        new_table[i][0] = table[0][j]
        new_table[i][1] = table[1][j]
        j += 1
 
    current = 2
    for j in range(2, len(new_table[0])):
        for i in range(1, len(new_table) - 1):
            if new_table[i - 1][j - 1] != ' ' and new_table[i + 1][j - 1] != ' ':
                new_table[i][j] = (new_table[i - 1][j - 1] - new_table[i + 1][j - 1]) /\
                                  (new_table[0][0] - new_table[current][0])
        current += 2
 
    return new_table
 
def generate_polinom(table, x):
    coeff = []
    j = 1
    for i in range(0, len(table) // 2 + 1):
        coeff.append(table[i][j])
        j += 1
 
    polinom = 'P' + str(len(table) // 2) + ' = '
    result = 0
    for i in range(len(coeff)):
        if i > 0:
            polinom += ' + '
 
        current = coeff[i]
        polinom += '{:.4f}'.format(coeff[i])
 
        for j in range(i):
            current *= x - table[j * 2][0]
            polinom += ' * (x - ' + '{:.4f}'.format(table[j * 2][0]) + ')'
 
        result += current
 
        if i < len(coeff) - 1:
            polinom += ' +\n'
    return result
