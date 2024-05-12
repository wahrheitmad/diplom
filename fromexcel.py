import openpyxl
from aspose.cells import Workbook
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, cm
from scipy.interpolate import griddata


class Equation():
    def __init__(self, x_, y_, z_):
        self.x_ = np.array(x_)
        self.y_ = np.array(y_)
        self.z_ = np.array(z_)


    # Визуализация поверхности
    def visual(self, x_, y_, z_):
        xgrid, ygrid = np.meshgrid(x_, y_)
        zgrid = 1 - (xgrid / 8) ** 2 + 0.5 * np.sin(np.pi / 4 * ygrid)

        fig = plt.figure(figsize=(12, 7))

        # Второй график
        ax2 = fig.add_subplot(111, projection='3d')
        ax2.plot_surface(xgrid, ygrid, zgrid, cmap='viridis')
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
    x = data['x'].to_numpy()
    print('Numpy Array Datatype :', x.dtype)
    y = data['y'].to_numpy()
    z = data['z'].to_numpy()
    print()
    return x, y, z


if __name__ == '__main__':
    x_, y_, z_ = read_from_excel('C:/Users/micha/Рабочий стол/example.xlsx')
    g = Equation(x_, y_, z_)

    # print(g.x_values())
    # print('\n\n\n')
    # print(g.y_values())
    # print('\n\n\n')
    # print(g.z_values("1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)"))
    # x = g.x_values()
    # y = g.y_values()
    # fig = g.visual(g.x_, g.y_, g.z_)
    # plt.show()