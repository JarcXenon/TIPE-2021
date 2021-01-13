from sheets import values

for k in range(len(values[0])):
    x = values[0][k]
    a = x.index('[')
    b = x.index(']')
    x = x[a+1: b]
    values[0][k] = x