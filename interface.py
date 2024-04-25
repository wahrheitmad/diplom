import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from main import Equation

import numpy as np


def _quit():
    root.quit()  # остановка цикла
    root.destroy()  # закрытие приложения


root = tkinter.Tk()
root.wm_title("Построение графика y=sin(x)")

g = Equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
x = g.x_values()
y = g.y_values()
fig = g.visual(x, y)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Выход", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()