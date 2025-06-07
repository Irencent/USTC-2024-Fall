import numpy as np
def f(a):
    category = int(np.floor(np.log2(abs(a)))) + 1
    value = int(a)
    if value < 0:
        value = abs(value)
        value = (1 << category) - value - 1
    
    amplitude = format(value, f'0{category}b')
    return amplitude

def df(a):
    size = len(a)
    value = int(a, 2)
                
    if a[0] == '0': # If the first bit is 0, it's a negative value
        value = -(1 << size) + value + 1

    return value

print(f(-2))