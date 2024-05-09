import tkinter
from idlelib.tooltip import Hovertip
from tkinter import filedialog

import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from numpy import sin, cos
from tktooltip import ToolTip

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


def get_equation():
    equation = equation_entry.get()
    return str(equation)


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
root.geometry("1400x900")
root.wm_title("Сглаживание функций")
root.configure(bg='gray76')


mainmenu = tkinter.Menu(root)
root.config(menu=mainmenu)

filemenu = tkinter.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command=open_file, font=("", 14))
filemenu.add_command(label="Новый", font=("", 14))
filemenu.add_command(label="Сохранить...", font=("", 14))
filemenu.add_command(label="Выход", command=_quit, font=("", 14))

var1 = tkinter.BooleanVar()
var1.set(1)

toolsmenu = tkinter.Menu(mainmenu, tearoff=0)
toolsmenu.add_checkbutton(label="Показать тулбар", command=tool_options, variable=var1, font=("", 14))
toolsmenu.add_command(label="О программе", font=("", 14))

helpmenu = tkinter.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", font=("", 14))
helpmenu.add_command(label="О программе", font=("", 14))

mainmenu.add_cascade(label="Файл", menu=filemenu, font=("", 14))
mainmenu.add_cascade(label="Справка", menu=helpmenu, font=("", 14))
mainmenu.add_cascade(label="Инструменты", menu=toolsmenu, font=("", 14))

equation_label = tkinter.Label(text="Введите уравнение:", font=("Arial", 14), bg='gray76')
equation_label.grid(row=0, column=0, sticky="NW", pady=30, padx=15)
ToolTip(equation_label, msg="Например: 1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

equation_entry = tkinter.Entry(width=50, font=("", 14))
equation_entry.grid(row=0, column=0, sticky="NW", pady=70, padx=15)

grid_label = tkinter.Label(text="Параметры сетки.", font=("Arial", 14), bg='gray76', foreground="forest green")
grid_label.grid(row=0, column=0, sticky="NW", pady=110, padx=15)

gridx_label = tkinter.Label(text="Параметры оси Х:", font=("Arial", 14), bg='gray76')
gridx_label.grid(row=0, column=0, sticky="NW", pady=150, padx=15)
# myTip = Hovertip(gridx_label, 'Введите в текстбоксы ограничения левой и правой \nграницы оси X', fontsize)
ToolTip(gridx_label, msg="Введите в текстбоксы ограничения оси X", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridx_min_entry = tkinter.Entry(width=10, font=("", 14))
gridx_min_entry.grid(row=0, column=0, sticky="NW", pady=190, padx=15)
ToolTip(gridx_min_entry, msg="Например: -8", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridx_max_entry = tkinter.Entry(width=10, font=("", 14))
gridx_max_entry.grid(row=0, column=0, sticky="NW", pady=190, padx=155)
ToolTip(gridx_max_entry, msg="Например: 8", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridy_label = tkinter.Label(text="Параметры оси Y:", font=("Arial", 14), bg='gray76')
gridy_label.grid(row=0, column=0, sticky="NW", pady=240, padx=15)
# myTip = Hovertip(gridy_label, 'Введите в текстбоксы ограничения левой и правой \nграницы оси Y')
ToolTip(gridy_label, msg="Введите в текстбоксы ограничения оси Y", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)



gridy_min_entry = tkinter.Entry(width=10, font=("", 14))
gridy_min_entry.grid(row=0, column=0, sticky="NW", pady=290, padx=15)
ToolTip(gridy_min_entry, msg="Например: -7", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridy_max_entry = tkinter.Entry(width=10, font=("", 14))
gridy_max_entry.grid(row=0, column=0, sticky="NW", pady=290, padx=155)
ToolTip(gridy_max_entry, msg="Например: 7", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

canvas0 = tkinter.Canvas(root, width=600, height=500,
                         bg='grey95',
                         borderwidth=10,
                         highlightthickness=10)
canvas0.grid(row=0, column=1, sticky="N", pady=50)

fig = make_equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
fig.set_size_inches(5.5, 4.5)


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=1, rowspan=1, padx=200)
canvas.draw()


toolbarFrame = tkinter.Frame(master=root)
toolbarFrame.grid(row=2, column=1, sticky="SW", ipady=0, padx=200)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

# toolbar_button = tkinter.Button(master=root, text="Скрыть тулбар", command=lambda: tool_options(), width=15, height=2)
# toolbar_button.grid(row=1, column=4, rowspan=1, sticky="E", pady=10)

quit_button = tkinter.Button(master=root, text="Выход", command=_quit, width=15, height=2)
quit_button.grid(row=4, column=1, sticky="SE", pady=100, padx=160)

ok_button = tkinter.Button(master=root, text="OK", command=get_equation, width=15, height=2)
ok_button.grid(row=4, column=0, sticky="SW", pady=100, padx=50)

root.mainloop()


