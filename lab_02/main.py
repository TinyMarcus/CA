from math import *

def function(x):
    return x * x

def get_values(x_a, x_s, quan):
    table_x = [x_a + x_s * i for i in range(quan)]
    table_y = [function(x) for x in table_x]
    return table_x, table_y

def output(x, y):
    len_dots = len(x)
    print("    X         Y    ")
    for i in range(len_dots):
        print("%+3.4f   %+3.4f" % (x[i], y[i]))
    print()

def spline(x, y, x_val):
    n = len(x)
    nearest_index = min(range(n), key = lambda i: abs(x[i] - x_val))

    h = [0 if not i else x[i] - x[i - 1] for i in range(n)]

    A = [0 if i < 2 else h[i - 1] for i in range(n)]
    B = [0 if i < 2 else -2 * (h[i - 1] + h[i]) for i in range(n)]
    D = [0 if i < 2 else h[i] for i in range(n)]
    function = [0 if i < 2 else -3 * ((y[i] - y[i - 1]) / h[i] - (y[i - 1] - y[i - 2]) / h[i - 1]) for i in range(n)]

    # прямой
    ksi = [0 for i in range(n + 1)]
    eta = [0 for i in range(n + 1)]
    for i in range(2, n):
        ksi[i + 1] = D[i] / (B[i] - A[i] * ksi[i])
        eta[i + 1] = (function[i] + A[i] * eta[i]) / (B[i] - A[i] * ksi[i])

    # обратный
    c = [0 for i in range(n + 1)]
    for i in range(n - 2, -1, -1):
        c[i] = ksi[i + 1] * c[i + 1] + eta[i + 1]

    a = [0 if i < 1 else y[i-1] for i in range(n)]
    b = [0 if i < 1 else (y[i] - y[i - 1]) / h[i] - h[i] / 3 * (c[i + 1] + 2 * c[i]) for i in range(n)]
    d = [0 if i < 1 else (c[i + 1] - c[i]) / (3 * h[i]) for i in range(n)]

    return a[nearest_index] + b[nearest_index] * (x_val - x[nearest_index - 1]) + c[nearest_index] * \
    ((x_val - x[nearest_index - 1]) ** 2) + d[nearest_index] * ((x_val - x[nearest_index - 1]) ** 3)

def main():
    print('''
Что вводится:
- координата x начальной точки
- шаг
- количество значений
- координата x\n''')
    x_a = float(input("Введите координату x начальной точки: "))
    x_s = float(input("Введите шаг: "))
    quan = int(input("Введите количество значений: "))

    table_x, table_y = get_values(x_a, x_s, quan)
    print("\nТаблица:")
    output(table_x, table_y)

    x = float(input("Введите x: "))

    result = spline(table_x, table_y, x)
    print("\nИнтерполяция : ", result)
    print("F(x)         : ", function(x))
    print("Погрешность  : ", abs((function(x) - result)), "\n")

if __name__ == '__main__':
    main()
