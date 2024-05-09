from numpy import copy

from main import Grid, Equation
import numpy as np


def ready(n, x_, y_, s):
    x_min = x_.min()
    y_min = y_.min()
    for i in range(0, n):
        x_[i] = (x_[i] - x_min) / s
        y_[i] = (y_[i] - y_min) / s
    return x_, y_


def number(y_, x_):
    return int(y_.max()) + 1, int(x_.max()) + 1,


def layer(n, y_, q):
    t_ = np.zeros(q + 1)
    for i in range(0, n):
        temp = int(y_[i]) + 1
        t_[temp] += 1
    t_[0] = 1
    for j in range(1, q + 1):
        t_[j] += t_[j - 1]
    return t_.astype(int)


def order(n, t_, y_, x_, q):
    a_ = np.zeros(n + 1).astype(int)
    l_ = copy(t_)
    for i in range(0, n):
        j = int(y_[i])
        a_[l_[j]] = i
        l_[j] += 1
    for k in range(0, q):
        count = t_[k+1] - t_[k]
        if count > 1:
            for o in range(count - 1):
                for l in range(t_[k], t_[k+1] - 1):
                    if x_[a_[l]] > x_[a_[l+1]]:
                        temp = a_[l]
                        a_[l] = a_[l+1]
                        a_[l+1] = temp
    print(1)
    return a_

def move(n, x_, y_, z_, a_):
    def mov(v_):
        u_ = copy(v_)
        for i in range(0, n):
            v_[i] = u_[a_[i+1]]
    mov(x_)
    mov(y_)
    mov(z_)
    return x_, y_, z_

def osp(n, x_, y_, z_, r, lam):
    d_ = []
    g_ = []
    l_ = []
    equation = "((1-x)**(r+1)*(1-y)**(r+1))/((1+lam*x)*(1+lam*y))"
    for i in range(0, n):
        w_temp = 0
        d_temp = 0
        g_temp = 0
        l_temp = 0
        for j in range(0, n):
            x_current = x_[i] - x_[j]
            y_current = y_[i] - y_[j]
            if abs(x_current) < 1 and abs(y_current) < 1:
                x_current = x_current ** 2
                y_current = y_current ** 2
                w_temp = eval(equation, {"x": x_current, "y": y_current, "r": r, "lam": lam})
            else:
                w_temp = 0
            d_temp += z_[j] * w_temp
            g_temp += w_temp
        d_.append(d_temp)
        g_.append(g_temp)
    return d_, g_

def lyambda(n):
    lyambda = np.zeros(n).astype(int)
    lyambda[1] = 100
    for i in range(2, n):
        lyambda[i] = lyambda[i-1]*3
    return lyambda



def coef(n, x_, y_, z_, e, r, m, lyambda, c, iks):
    f_o = []
    sigma = []
    def control(lam, el, z_):
        f1 = np.max(np.abs(z_))
        f2 = 0
        for j in range(0, n):
            f2 += z_[j]**2
        f2 = np.sqrt(f2/n)
        if el == 0:
            c1 = 0
            c2 = 0
        else:
            c1 = f1
            c2 = f2
        c1 = c1/f1
        c2 = c2/f2
        # if iks:
        #     return f1, c1
        # else:
        #     return f2, c2
        return f1, c1, f2, c2
        print("todo")

    el = 0
    iks = True
    f1, c1, f2, c2 = control(lyambda[0], el, z_)
    m0 = m
    for k in range(1, m0):
        lam = lyambda[k]
        sigma.append(z_)
        # sigma_current = sigma[k-1]
        el += 1
        d_, g_ = osp(n, x_, y_, z_, r, lam)
        for i in range(0, n):
            z_[i] = z_[i] - d_[i]/g_[i]
        f1, c1, f2, c2 = control(lam, el, z_)
        if f1 >= e or c1 >= c:
            for p in range(0, n):
                sigma[k-1][p] += z_[p]
        # перезаписать сигму
        if f1 <= e or k == m0:
            m = k
            return sigma, m
            break



def square(n, x_, y_, t_, p, q):
    m_ = np.zeros(p + 1)
    k_ = np.zeros(p*q + 1)
    k_[0] = 1
    for j in range (0, q-1):
        for l in range (t_[j], t_[j+1] - 1):
            i = int(x_[l])
            m_[i] = m_[i] + 1
        l = j * p
        for i in range(0, p-1):
            k_[i + l + 1] = k_[i + l] + m_[i]
    return  k_

def point(n, x, y, x_, y_, sigma, lyambda, m, r):
    f_z = 0
    equation = "((1-x)**(r+1)*(1-y)**(r+1))/((1+lam*x)*(1+lam*y))"
    for k in range(0, m):
        d_temp = 0
        g_temp = 0
        sigma_temp = sigma[k]
        lam = lyambda[k]
        for i in range(0, n):
            x_current = x - x_[i]
            y_current = y - y_[i]
            if x_current < 1 and y_current < 1:
                x_current = x_current ** 2
                y_current = y_current ** 2
                w_temp = eval(equation, {"x": x_current, "y": y_current, "r": r, "lam": lam})
            else:
                w_temp = 0
                continue
            d_temp += sigma_temp[i] * w_temp
            g_temp += w_temp
        f_z += d_temp/g_temp
    return f_z








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
    # g.x_, g.y_ = ready(g.count(), g.x_, g.y_, g.length)
    # q, p = number(g.y_, g.x_)
    # t_ = layer(g.count(), g.y_, q)
    # a_ = order(g.count(), t_, g.y_, g.x_, q)
    # g.x_, g.y_, g.z_ = move(g.count(), g.x_, g.y_, g.z_, a_)
    # lyambda1 = lyambda(10)
    # sigma, m = coef(g.count(), g.x_, g.y_, g.z_, 0.01, 3, 10, lyambda1, 1.2, iks=True)
    # x = [2, 1, 4, 6]
    x = [0.2, 0.5, 4, 3]
    x = np.array(x)
    # y = [3, 3, 8, 4]
    y = [0, 0, 0, 0]
    y = np.array(y)
    z = [617.16, 1101, 1649, 2597]
    z = np.array(z)
    ready(4, x, y, 1)
    q, p = number(y, x)
    t_ = layer(4, y, q)
    a_ = order(4, t_, y, x, q)
    x, y, z = move(4, x, y, z, a_)
    lyambda1 = lyambda(10)
    sigma, m = coef(4, x, y, z, 0.01, 3, 10, lyambda1, 1.2, iks = True)
    # square(4, x, y, t_, p, q)
    # fz = point(g.count(), 1, 1, g.x_, g.y_, sigma, lyambda1, m, 3)
    fz = point(4, 1, 1, x, y, sigma, lyambda1, m, 3)

    print(1)
