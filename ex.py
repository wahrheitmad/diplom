import numpy as np
import pandas as pd
from scipy.interpolate import interp2d, bisplrep, bisplev

# Создание исходных двумерных данных
x = np.arange(0, 10, 1)
y = np.arange(0, 10, 1)
data = 1 - (x/8) ** 2 + 0.5 * np.sin(np.pi/4 * y)

excel_data = pd.read_excel('C:/Users/micha/Рабочий стол/example.xlsx')
data = pd.DataFrame(excel_data, columns=['x', 'y', 'z'])
print("The content of the file is:\n", data)
x = data['x'].to_numpy()
print('Numpy Array Datatype :', x.dtype)
y = data['y'].to_numpy()
data = data['z'].to_numpy()

# Создание объекта интерполяции с помощью interp2d
interpolator = bisplrep(x, y, data)

# Оценка значения функции в произвольных точках
new_x = 1
new_y = 1
new_data = bisplev(new_x, new_y, interpolator)


# Визуализация результатов (пример)
import matplotlib.pyplot as plt
plt.imshow(new_data, extent=(0, 9, 0, 9), origin='lower')
plt.colorbar()
plt.show()
