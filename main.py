# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify

class Grid:
    def __init__(self, x_min, x_max, y_min, y_max, length):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.length = length
        print("Создана сетка [{0}, {1}] x [{2}, {3}], сторона квадрата: {4}".format(x_min, x_max, y_min, y_max, length))

    def len(self):
        return abs(self.x_min) + abs(self.x_max)

class Equation(Grid):
    def __init__(self, x_min, x_max, y_min, y_max, length):
        super().__init__(x_min, x_max, y_min, y_max, length)


    def x_values(self):
        return np.random.uniform(self.x_min, self.x_max, self.len() ** 2)

    def y_values(self):
        return np.random.uniform(self.y_min, self.y_max, self.len() ** 2)

    def calculate_equation(self, equation, x_value, y_value, pi_value=np.pi):
        x, y, pi = symbols('x y pi')
        expr = sympify(equation)  # Преобразование строки уравнения в символьное выражение
        result = expr.subs({x: x_value, y: y_value, pi: pi_value})  # Подстановка значений переменных в уравнение
        return result

    def z_values(self, equation):
        z = np.zeros((self.len() + 1, self.len() + 1))
        for i in range(1, self.len()):
            for j in range(1, self.len()):
                z[i][j] = self.calculate_equation(equation, self.x_values()[i], self.y_values()[j])
        return z


    def visual(self, equation):
        # Визуализация результата
        x = np.linspace(0, 1, self.len() + 1)
        y = np.linspace(0, 1, self.len() + 1)
        x_, y_ = np.meshgrid(x, y)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_, y_, self.z_values(equation).T, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('U')
        plt.show()










# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Equation(-8, 8, -8, 8, 1)
    g.visual("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
