from main import Grid, Equation
import numpy as np

def ready(n, x_, y_, s):
    x_min = x_.min()
    y_min = y_.min()
    for i in range(0, n**2):
        x_[i] = (x_[i] - x_min)/s
        y_[i] = (y_[i] - y_min)/s
    return x_, y_


def number(y_):
    return int(y_.max()) + 1

def layer(n, y_, q):
    t_ = np.zeros(q+1)
    for i in range(0, n**2):
        temp = int(y_[i]) + 1
        t_[temp] += 1
    t_[0] = 1
    for j in range(1, q+1):
        t_[j] += t_[j-1]
    print(1)
    return t_


def order(n, t_, y_):
    a_ = np.zeros(n**2)
    for i in range(0, n**2):
        a_[i] = t_[int(y_[i])]
    print(1)





def osp(n, x_, y_, z_, r, lam):
    d_ = []
    g_ = []
    equation = "((1-x)**(r+1)*(1-y)**(r+1))/((1+lam*x)*(1+lam*y))"
    for i in range(0, n**2):
        w_temp = 0
        d_temp = 0
        g_temp = 0
        for j in range(0, n**2):
            x_current = x_[i] - x_[j]
            y_current = y_[i] - y_[j]
            x_current = x_current**2
            y_current = y_current**2
            if abs(x_current) < 1 and abs(y_current) < 1:
                w_temp = eval(equation, {"x": x_current, "y": y_current, "r": r, "lam": lam})
            else:
                w_temp = 0
            d_temp += z_[j] * w_temp
            g_temp += w_temp
        d_.append(d_temp)
        g_.append(g_temp)
    return d_, g_



if __name__ == '__main__':
    g = Equation(-8, 8, -8, 8, 5, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
    # print(g.x_values())
    # print('\n\n\n')
    # print(g.y_values())
    # print('\n\n\n')
    # print(g.z_values("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)"))
    # x = g.x_values()
    # y = g.y_values()
    # z = g.z_values(x, y)
    # ready(g.len(), x, y, g.length)
    # print(number(y))
    # q = number(y)
    # layer(g.len(), y, q)
    # d, g = osp(g.len(), x, y, z, 0, 1)
    x = [1, 2, 4, 6]
    x = np.array(x)
    y = [3, 3, 8, 4]
    y = np.array(y)
    ready(2, x, y, 1)
    print(number(y))
    q = number(y)
    t_ = layer(2, y, q)
    order(2, t_, y)

    print(1)
