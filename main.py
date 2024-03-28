# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import random
import matplotlib.pyplot as plt
from sympy import symbols, sympify

# Класс сетки
class Grid:
    def __init__(self, x_min, x_max, y_min, y_max, length):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.length = length
        print("Создана сетка [{0}, {1}] x [{2}, {3}], сторона квадрата: {4}".format(x_min, x_max, y_min, y_max, length))

    # Длина = ширина сетки
    def len(self):
        return abs(self.x_min) + abs(self.x_max)


    # Инициализация сетки
    def grid_init(self):
        x = np.linspace(self.x_min, self.x_max, self.len())
        y = np.linspace(self.y_min, self.y_max, self.len())
        return x, y


# Класс уравнения
class Equation(Grid):
    def __init__(self, x_min, x_max, y_min, y_max, length):
        super().__init__(x_min, x_max, y_min, y_max, length)


    # Массив значений X
    def x_values(self):
        x = []
        for i in range(self.y_min, self.y_max):
            for j in range(self.x_min, self.x_max):
                x.append(np.round(j + np.random.sample(), 4))
        return np.array(x)

    # Массив значений Y
    def y_values(self):
        y = []
        for i in range(self.y_min, self.y_max):
            for j in range(self.x_min, self.x_max):
                y.append(np.round(i + np.random.sample(), 4))
        return np.array(y)

    # Преобразование строки уравнения для вычислений
    def calculate_equation(self, equation, x_value, y_value, pi_value=np.pi):
        x, y, pi = symbols('x y pi')
        expr = sympify(equation)  # Преобразование строки уравнения в символьное выражение
        result = expr.subs({x: x_value, y: y_value, pi: pi_value})  # Подстановка значений переменных в уравнение
        return result

    # Массив значений Z
    def z_values(self, equation):
        z = []
        x = self.x_values()
        y = self.y_values()
        for i in range(0, self.len()**2):
            z[i] = self.calculate_equation(equation, x[i], y[i])
        return x, y, z

    # Визуализация поверхности
    def visual(self, equation):
        x, y, z = self.z_values(equation)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(x, y, z, cmap='viridis')

        # Добавляем метки и цветовую шкалу
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        fig.colorbar(surf)

        # Отображаем график
        plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Equation(-8, 8, -8, 8, 1)
    print(g.x_values())
    print('\n\n\n')
    print(g.y_values())
    print('\n\n\n')
    print(g.z_values("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)"))
    g.visual("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
