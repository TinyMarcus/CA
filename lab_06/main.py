from math import e, log, cos, sin
from prettytable import PrettyTable

a0, a1, a2 = 1, 2, 3
table_data = PrettyTable()


def f(x):
    return (a0*x / (a1 + a2*x))
#    return cos(x) - 1

    
def f_det(x):
    return (a0*(a1+a2*x)-a0*a2*x)/((a1+a2*x)**2)
#    return (a0 * a1) / ((a1 + a2*x)**2)
#    return (-sin(x))
    
    
def etaksi(): # производная эта по кси
    return a1 / a0


def etay(y): # производная эта по у
    return 1 / (y*y)


def ksix(x): # производная кси по х
    return 1 / (x*x)


def get_table(x_beg, step, amount):
    x_tbl = [x_beg + step*i for i in range(amount)]
    y_tbl = [round(f(x), 5) for x in x_tbl]
    return x_tbl, y_tbl


def left_side_diff(y, h):
    y_left = [None] * x_amount
  
    for i in range(1, x_amount):
        y_left[i] = round((y[i] - y[i - 1]) / h, 5)      
    return y_left
    
'''
def right_side_diff(y, h):
    return [None if i == len(y) - 1
            else round(((y[i + 1] - y[i]) / h), 5)
            for i in range(len(y))]          
'''

def center_diff(y, h):
    y_center = [None] * x_amount
    
    for i in range(1, x_amount - 1):
        y_center[i] = round((y[i + 1] - y[i - 1]) / (2 * h), 5)
    return y_center
    
    
def accuracy(y, h):
    n = len(y)
    y_accuracy = [None] * n
    y_accuracy[0] = round((-3 * y[0] + 4 * y[1] - y[2]) / (2 * h), 5)
    y_accuracy[n - 1] = round((y[n - 3] - 4 * y[n - 2] + 3 * y[n - 1]) / (2 * h), 5)
    return y_accuracy


def runge_left_side(y, h):
    n = len(y)
    p = 1
    r = 2
    
    y_runge = [None] * n
    y_left_tmp = [None] * n
    y_left = left_side_diff(y, h)

    for i in range(2, n):
        y_left_tmp[i] = (y[i] - y[i - 2]) / (2 * h)
        y_runge[i] = round(y_left[i] + (y_left[i] - y_left_tmp[i]) / (r**p - 1), 5)
    return y_runge
    
    
def level(x, y):
    n = len(x)
    y_level = [None] * n
    
    for i in range(n):
        if x[i] != 0:
            y_level[i] = round((etaksi() * ksix(x[i])) / etay(y[i]), 5)
    return y_level
    

def add_to_table(text, res):
    table_data.add_column(text, res)


x_start = int(input("Введите начальное значение x: "))
x_h = float(input("Введите шаг: "))
x_amount = int(input("Введите количество значений x: "))
x, y = get_table(x_start, x_h, x_amount)


add_to_table("x:", x)
add_to_table("y:", y)
add_to_table("Левосторонняя разность:", left_side_diff(y, x_h))
add_to_table("Повышенного порядка:", accuracy(y, x_h))
add_to_table("Центральная разность:", center_diff(y, x_h))
add_to_table("Рунге (левостор.):", runge_left_side(y, x_h))
add_to_table("Выравнивающие", level(x, y))
add_to_table("Точный ответ:", [round(f_det(i), 5) for i in x])


print(table_data)
