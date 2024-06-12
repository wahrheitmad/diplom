import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Создаем данные для поверхности
x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 2, 3, 4, 5])
X, Y = np.meshgrid(x, y)
Z = np.random.rand(len(x), len(y))  # Замените на ваш массив z

# Строим поверхность
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# Настройки отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()