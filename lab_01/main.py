from math import *
from prettytable import PrettyTable
# def f(x):
#     #return cos(x) - x
#     return x*x

# def newton_polynomial(x, degree, beginning, table_x, table_y):
    # result = table_y[beginning]
    # for i in range((beginning + 1), beginning + degree):
    #     divided = 0
    #     for j in range(beginning, i + 1):
    #         difference = 1
    #         for k in range(beginning, i + 1):
    #             if (k != j):
    #                 difference *= (table_x[j] - table_x[k])
    #         divided += (table_y[j] / difference)
    #     for k in range(beginning, i):
    #         divided *= (x - table_x[k])
    #     result += divided
    # return result

# def main():
#     table_x = []
#     table_y = []
#     left_limit = float(input('Enter value of right limit: \n'))
#     right_limit = float(input('Enter value of left limit: \n'))
#     step = float(input('Enter step value: \n'))
#
#     while left_limit <= right_limit:
#         table_x.append(left_limit)
#         left_limit += step
#
#     for i in range(len(table_x)):
#         table_y.append(f(table_x[i]))
#
#     table_data = PrettyTable()
#     table_data.add_column('x', table_x)
#     table_data.add_column('y(x)', table_y)
#     print(table_data)
#
#     degree = int(input('Enter degree of Newton\'s polynomial: \n'))
#     x = float(input('Enter value of x: \n'))
#
#     first_y = nearest_value(x, table_x, len(table_x))
#     beginning = find_begin(x, table_x, len(table_x), first_y, degree)
#
#     print('\nResults: \n')
#     print('Interpolation: ', newton_polynomial(x, degree, int(beginning), table_x, table_y))
#     print('Exact value: ', f(x))

def f(x):
    return cos(radians(x)) - x
    # return cos(radians(90*x))
    # return cos(x)

def get_roots_array(x_a, x_s, x_quan):
    table_x = [x_a + x_s * i for i in range(x_quan)]
    table_y = [f(x) for x in table_x]
    return table_x, table_y

def get_matrix(table, n):
    for i in range(n):
        temp = []
        for j in range(n - i):
            temp.append(round(((table[i+1][j] - table[i+1][j+1]) / \
                        (table[0][j] - table[0][i+j+1])), 3))
        table.append(temp)
    return table

def take_values(table, n, x):
    table_len = len(table[0])
    nearest_index = min(range(table_len), key = lambda i: abs(table[0][i] - x))
    needed_space = ceil(n / 2)

    if (nearest_index + needed_space + 1 > table_len):
        end_index = table_len
        start_index = table_len - n
    elif (nearest_index < needed_space):
        start_index = 0
        end_index = n
    else:
        start_index = nearest_index - needed_space + 1
        end_index = start_index + n
    #print()
    #print(start_index, end_index)
    #print(nearest_index)
    #print()
    return [table[0][start_index:end_index], table[1][start_index:end_index]]

def output(x, y):
    len_dots = len(x)
    print("    X         Y    ")
    for i in range(len_dots):
        print("%+3.4f   %+3.4f" % (x[i], y[i]))
    print()

def newton_polynomial(table, n, x):
    table, ind = take_values(table, n + 1, x)
    matrix = get_matrix(table, n)
    #print(matrix)
    matrix[2].append(" - ")
    for i in range(2):
        matrix[3].append(" - ")
    for i in range(3):
        matrix[4].append(" - ")
    for i in range(4):
        matrix[5].append(" - ")
    table_data = PrettyTable()
    table_data.add_column('m[0]', matrix[0])
    table_data.add_column('m[1]', matrix[1])
    table_data.add_column('m[2]', matrix[2])
    table_data.add_column('m[3]', matrix[3])
    table_data.add_column('m[4]', matrix[4])
    table_data.add_column('m[5]', matrix[5])
#    table_data.add_column('Y(X)', y_table)
    print(table_data)
    temp = 1
    result = 0
    for i in range(n + 1):
        result = result + temp * matrix[i+1][0]
        temp = temp * (x - matrix[0][i])
    return result, ind

def main():
    print('''
Что вводится:
- координата x начальной точки
- шаг
- количество значений
- степень полинома
- координата x''')
    x_a = float(input("\nВведите координату x начальной точки: "))
    x_s = float(input("Введите шаг: "))
    x_quan = int(input("Введите количество значений: "))

    table_x, table_y = get_roots_array(x_a, x_s, x_quan)
    print("\nТаблица:")
    output(table_x, table_y)

    x = float(input("Введите x: "))
    n = int(input("Введите степень полинома n: "))

    result, ind = newton_polynomial([table_x, table_y], n, x)
    #print("\nИнтервал     : [", table_x[ind], ',', table_x[ind+1], "]")
    print("\nИнтерполяция : ", result)
    print("F(x)         : ", f(x))
    print("Погрешность  : ", abs((f(x) - result)), "\n")
    root, index = newton_polynomial([table_y, table_x], n, 0)
    print("Корень =", root)

if __name__ == '__main__':
    main()
