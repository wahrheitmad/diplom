import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Готовые массивы с координатами точек
x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 2, 3, 4, 5])
z = np.array([[2, 3, 4, 5, 6],
              [3, 5, 7, 9, 11],
              [4, 7, 10, 13, 16],
              [5, 9, 13, 17, 21],
              [6, 11, 16, 21, 26]])

# Строим поверхность
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
