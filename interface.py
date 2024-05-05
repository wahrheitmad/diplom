import tkinter
from tkinter import filedialog

import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from numpy import sin, cos

from main import Equation
from fromexcel import read_from_excel

is_closed = False

def make_equation(x_min, x_max, y_min, y_max, length, equation):
    # g = Equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
    g = Equation(x_min, x_max, y_min, y_max, length, equation)
    x = g.x_values()
    y = g.y_values()
    fig = g.visual(x, y)
    return fig


def open_file():
    filepath = filedialog.askopenfilename()
    read_from_excel(filepath)


def _hide(widget):
    widget.grid_remove()


def _show(widget):
    widget.grid()


def tool_options():
    global is_closed
    if is_closed:
        _show(toolbarFrame)
        is_closed = False
    else:
        _hide(toolbarFrame)
        is_closed = True


def _quit():
    root.quit()  # остановка цикла
    root.destroy()  # закрытие приложения


root = tkinter.Tk()
root.geometry("1300x700")
root.wm_title("Построение графика y=sin(x)")


mainmenu = tkinter.Menu(root)
root.config(menu=mainmenu)

filemenu = tkinter.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command=open_file)
filemenu.add_command(label="Новый")
filemenu.add_command(label="Сохранить...")
filemenu.add_command(label="Выход", command=_quit)

var1 = tkinter.BooleanVar()
var1.set(1)

toolsmenu = tkinter.Menu(mainmenu, tearoff=0)
toolsmenu.add_checkbutton(label="Показать тулбар", command=tool_options, variable=var1 )
toolsmenu.add_command(label="О программе")

helpmenu = tkinter.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь")
helpmenu.add_command(label="О программе")

mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)
mainmenu.add_cascade(label="Инструменты", menu=toolsmenu)

canvas0 = tkinter.Canvas(root, width=600, height=500,
                         bg='grey95',
                         borderwidth=10,
                         highlightthickness=10)
canvas0.grid(row=0, column=1, pady=0)

fig = make_equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
fig.set_size_inches(5.5, 4.5)


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=4, rowspan=1)
canvas.draw()


toolbarFrame = tkinter.Frame(master=root)
toolbarFrame.grid(row=2, column=4, sticky="NE", ipady=0)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

# toolbar_button = tkinter.Button(master=root, text="Скрыть тулбар", command=lambda: tool_options(), width=15, height=2)
# toolbar_button.grid(row=1, column=4, rowspan=1, sticky="E", pady=10)

quit_button = tkinter.Button(master=root, text="Выход", command=_quit, width=15, height=2)
quit_button.grid(row=4, column=4, sticky="E", pady=10)
root.mainloop()


