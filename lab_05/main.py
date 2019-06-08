import first_part
import second_part
from math import *

def main():
    p_beg = float(input("Введите P начальное: "))
    t_beg = float(input("Введите T начальное: "))
    t0 = float(input("Введите T0: "))
    tw = float(input("Введите Tw: "))
    m = float(input("Введите m: "))
    
    print("\nPart 1: ", first_part.find_p(p_beg, t_beg, t0, tw, m))
    print("Part 2: ", second_part.find_p(p_beg, t_beg, t0, tw, m))    
    #print([exp(x_global[i]) for i in range(0, 6)])
    
if __name__ == '__main__':
    main()
