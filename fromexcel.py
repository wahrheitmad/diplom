import openpyxl
from aspose.cells import Workbook
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class Equation():
    def __init__(self, x_, y_, z_):
        self.x_ = x_
        self.y_ = y_
        self.z_ = z_


    # Визуализация поверхности
    def visual(self, x_, y_, z_):
        xgrid, ygrid = np.meshgrid(x_, y_)
        fig = plt.figure(figsize=(12, 7))
        # plt.figure(figsize=(12, 7))
        # surf = ax.plot_surface(xgrid, ygrid, zgrid, cmap='viridis')
        # surf1 = ax.plot_surface(xgrid, ygrid, zgrid1, cmap='viridis')

        # Добавляем метки
        # Первый график
        # ax1 = fig.add_subplot(121, projection='3d')
        # ax1.plot_surface(xgrid, ygrid, zgrid, cmap='viridis')
        # ax1.set_xlabel('X')
        # ax1.set_ylabel('Y')
        # ax1.set_zlabel('Z')

        # Второй график
        ax2 = fig.add_subplot(111, projection='3d')
        ax2.plot_surface(xgrid, ygrid, z_, cmap='viridis')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        # Отображаем график
        # plt.show()
        return fig


def read_from_excel(filepath):
    excel_data = pd.read_excel(filepath)
    data = pd.DataFrame(excel_data, columns=['x', 'y', 'z'])
    print("The content of the file is:\n", data)
    print()


if __name__ == '__main__':
    g = Equation()
    # print(g.x_values())
    # print('\n\n\n')
    # print(g.y_values())
    # print('\n\n\n')
    # print(g.z_values("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)"))
    # x = g.x_values()
    # y = g.y_values()
    fig = g.visual(g.x_, g.y_, g.z_)
    plt.show()