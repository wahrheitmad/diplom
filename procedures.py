from main import Grid, Equation

def ready(n, x_, y_, s):
    x_min = x_.min()
    y_min = y_.min()
    for i in range(0, n):
        x_[i] = (x_[i] - x_min)/s
        y_[i] = (y_[i] - y_min)/s
    return x_, y_

if __name__ == '__main__':
    g = Equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
    # print(g.x_values())
    # print('\n\n\n')
    # print(g.y_values())
    # print('\n\n\n')
    # print(g.z_values("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)"))
    x = g.x_values()
    y = g.y_values()
    z = g.z_values(x, y)
    ready(g.len(), x, y, g.length)
