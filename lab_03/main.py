from math import *

def f(x, y):
    return x**2 + y**2

def matrix(x_a, x_s, x_n, y_a, y_s, y_n):
    x = [x_a + i * x_s for i in range(x_n)]
    y = [y_a + i * y_s for i in range(y_n)]
    z = [[f(i, j) for i in x] for j in y]

    return x, y, z

def output(x, y, z):
    print("   y\\x ", end = '')
    for i in x:
        print("{:6}".format(i), end = ' ')

    for i in range(len(y)):
        print("\n{:6}".format(y[i]), end = ' ')
        for j in z[i]:
            print("{:6}".format(j), end = ' ')
    print('\n')

def dots(a, n, x):
    a_l = len(a)
    i_near = min(range(a_l), key = lambda i: abs(a[i] - x))
    space_needed = ceil(n / 2)

    if (i_near + space_needed + 1 > a_l):
        i_end = a_l
        i_start = a_l - n
    elif (i_near < space_needed):
        i_start = 0
        i_end = n
    else:
        i_start = i_near - space_needed + 1
        i_end = i_start + n

    return i_start, i_end

def get_diff_matr(table, n):
    for i in range(n):
        tmp = []
        for j in range(n-i):
            tmp.append((table[i+1][j] - table[i+1][j+1]) / (table[0][j] - table[0][i+j+1]))
        table.append(tmp)
    return table

def newtons_interpolation(table, n, x):
    matr = get_diff_matr(table, n)
    res = 0
    tmp = 1
    for i in range(n + 1):
        res += tmp * matr[i+1][0]
        tmp *= (x - matr[0][i])
    # print('\n\n\n', res, '\n\n\n')
    return res

def multi_interpolation(x, y, z, x_val, y_val, x_n, y_n):
    ix_beg, ix_end = dots(x, x_n + 1, x_val)
    iy_beg, iy_end = dots(y, y_n + 1, y_val)

    x = x[ix_beg : ix_end]
    y = y[iy_beg : iy_end]
    z = z[iy_beg : iy_end]
    for i in range(y_n + 1):
        z[i] = z[i][ix_beg : ix_end]

    print("\nВыбранные точки:")
    output(x, y, z)

    res = [newtons_interpolation([x, z[i]], x_n, x_val) for i in range(y_n + 1)]
    return newtons_interpolation([y, res], y_n, y_val)

def main():
    x_a = float(input("\nВведите начальную координату x: "))
    x_s = float(input("Введите шаг для координаты x: "))
    x_quan = int(input("Введите количество точек: "))

    y_a = float(input("\nВведите начальную координату y: "))
    y_s = float(input("Введите шаг для координаты y: "))
    y_quan = int(input("Введите количество точек: "))

    x, y, z = matrix(x_a, x_s, x_quan, y_a, y_s, y_quan)
    print("\nМатрица:")
    output(x, y, z)
    x_n = int(input("\nВведите n(x): "))
    x_find = float(input("Введите x: "))

    y_n = int(input("Введите n(y): "))
    y_find = float(input("Введите y: "))

    # Results
    found = multi_interpolation(x, y, z, x_find, y_find, x_n, y_n)
    print("\nИнтерполяция   : ", found)
    print("F(x, y)        : ", f(x_find, y_find))
    print("Погрешность    : ", abs(f(x_find, y_find) - found), "\n")

if __name__ == "__main__":
    main()
