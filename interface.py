import tkinter
from idlelib.tooltip import Hovertip
from tkinter import filedialog, messagebox

import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from numpy import sin, cos
from tktooltip import ToolTip
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication)

from main import Equation
from procedures import *
from fromexcel import read_from_excel

is_closed = False
g = Equation
lyambda1 = 0
lamcoef = 0
r = 0
c = 0
e = 0
s = 0
sigma = []
m = 0

def get_equation():
    global g
    equation = equation_entry.get()
    x_min = int(gridx_min_entry.get())
    x_max = int(gridx_max_entry.get())
    y_min = int(gridy_min_entry.get())
    y_max = int(gridy_max_entry.get())
    length = int(grid_s_entry.get())/2
    g = Equation(x_min, x_max, y_min, y_max, length, equation)
    messagebox.showinfo(title="Успешно", message="Создана сетка [{0}, {1}] x [{2}, {3}], сторона квадрата: {4}. Уравнение: {5}".format(x_min, x_max, y_min, y_max, length, equation))
    return equation, x_min, x_max, y_min, y_max, length

def make_equation(x_min, x_max, y_min, y_max, length, equation):
    global g
    # # g = Equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
    g = Equation(x_min, x_max, y_min, y_max, length, equation)
    x = g.x_values()
    y = g.y_values()
    fig = g.visual(x, y)
    return fig

def save_params():
    global lyambda1, lamcoef, r, c, e
    lyambda1 = int(lyambda1_entry.get())
    lamcoef = int(lamcoef_entry.get())
    r = int(r_entry.get())
    c = float(speed_entry.get())
    e = float(e_entry.get())
    messagebox.showinfo(title="Успешно", message="Сохранены параметры λ1: {0}, Коэффициент увеличения λ: {1}, r: {2}, c: {3}, e: {4}".format(lyambda1, lamcoef, r, c, e))


def main_algorithm():
    global lyambda1, lamcoef, r, c, e, sigma, m, lyambda0, g
    # equation, x_min, x_max, y_min, y_max, length = get_equation()
    # g = Equation(x_min, x_max, y_min, y_max, length, equation)
    g.x_, g.y_ = ready(g.count, g.x_, g.y_, g.length)
    q, p = number(g.y_, g.x_)
    t_ = layer(g.count, g.y_, q)
    a_ = order(g.count, t_, g.y_, g.x_, q)
    g.x_, g.y_, g.z_ = move(g.count, g.x_, g.y_, g.z_, a_)
    lyambda0 = lyambda(10, lyambda1, lamcoef)
    sigma, m = coef(g.count, g.x_, g.y_, g.z_, e, r, 10, lyambda0, c, iks=True)
    # fz = point(g.count, 1, 1, g.x_, g.y_, sigma, lyambda1, m, 3)
    messagebox.showinfo(title="Успешно", message="Массив коэффициентов σ сохранен")

def save_point():
    y = float(point_y_entry.get())
    x = float(point_x_entry.get())
    messagebox.showinfo(title="Успешно", message="Точка сохранена")
    fz = find_point(x, y)
    messagebox.showinfo(title="Успешно", message="Значения найдены")
    result_f_entry.insert(0, fz)
    result_dx_entry.insert(0, fz)
    result_dy_entry.insert(0, fz)


def find_point(x, y):
    global lyambda0
    fz = point(g.count, x, y, g.x_, g.y_, sigma, lyambda0, m, 3)
    return fz



def open_file():
    global s
    def check():
        global s
        s = int(entry.get())/2
        root1.destroy()
    global g
    filepath = filedialog.askopenfilename()
    x, y, z = read_from_excel(filepath)
    root1 = tkinter.Tk()
    label = tkinter.Label(root1, text="Введите параметр s:", font=("Arial", 14), bg='gray76')
    label.grid()
    entry = tkinter.Entry(root1)
    entry.grid(pady=10)
    button = tkinter.Button(root1, text='Передать', command=check)
    button.grid()
    root1.mainloop()
    # length = int(grid_s_entry.get()) / 2
    g = Equation(x=x, y=y, z=z, length=s)
    # root1.quit()  # остановка цикла

print(0)


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

def guide():
    messagebox.showinfo(title="Информация", message="Здравствуйте! Для эффективного использования модуля следуйте алгоритму:\n"
                                                 "1. Введите необходимые данные в окно Параметры (выделено черным прямоугольником)\n"
                                                 "2. Введите уравнение, параметры сетки и сторону длины квадрата s (далее - пункт 5)\n"
                                                 "3. Если необходимо загрузить данные из Excel, в верхнем меню выберите\n Файл - Открыть и выберите файл.\n"
                                                 "4. Система предложит вам ввести параметр s, пожалуйста, не пропускайте этот этап. (далее - пункт 6)\n"
                                                 "5. Нажмите кнопку Сгенерировать. Дождитесь появления всплывающего окна.\n"
                                                 "6. Нажмите кнопку Запустить алгоритм. Дождитесь появления всплывающего \n окна с информацией об успешном сохранении коэффициентов.\n"
                                                 "7. Введите точку в окне ввода координат (оно расположено под кнопкой запуска алгоритма).\n"
                                                 "8. Дождитесь появления всплывающих окн.\n"
                                                 "9. Вычисленные значеняи появятся справа от окна ввода координат.\n"
                                                    "Если необходимо очистить все поля для ввода, воспользуйтесь командой \nФайл - Новый в верхнем меню.\n"
                                                 "Спасибо, что используете данный модуль.")


def function_info():
    messagebox.showinfo(title="Информация", message="Программный модуль обладает следующими функциями:\n"
                                                    "1. Загрузка данных из файла Excel\n"
                                                    "2. Генерирование данных на основе функции и заданной сетки\n"
                                                    "3. Сохранение сгенерированных данных в формате Excel\n"
                                                    "4. Построение поверхности на основе введеннных данных\n"
                                                    "5. Управление параметрами сглаживания функции\n"
                                                    "6. Нахождение значения функции и ее частных производных\nв заданной точке.")


def clean_all():
    widgets = [root, frame, frame1]
    for widget in widgets:
        for child in widget.winfo_children():
            if isinstance(child, tkinter.Entry):
                child.delete(0, tkinter.END)

def _quit():
    root.quit()  # остановка цикла
    root.destroy()  # закрытие приложения


root = tkinter.Tk()
# root.geometry("1400x900")
root.state('zoomed')
root.wm_title("Сглаживание функций")
root.configure(bg='gray76')


mainmenu = tkinter.Menu(root)
root.config(menu=mainmenu)

filemenu = tkinter.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command=open_file, font=("", 14))
filemenu.add_command(label="Новый", font=("", 14), command=clean_all)
filemenu.add_command(label="Сохранить...", font=("", 14))
filemenu.add_separator()
filemenu.add_command(label="Выход", command=_quit, font=("", 14))

var1 = tkinter.BooleanVar()
var1.set(1)

toolsmenu = tkinter.Menu(mainmenu, tearoff=0)
toolsmenu.add_checkbutton(label="Показать тулбар", command=tool_options, variable=var1, font=("", 14))

helpmenu = tkinter.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Руководство пользователя", font=("", 14), command=guide)
helpmenu.add_command(label="Функции модуля", font=("", 14), command=function_info)
helpmenu.add_command(label="Ввод уравнений", font=("", 14), command=function_info)
helpmenu.add_command(label="О программе", font=("", 14))

mainmenu.add_cascade(label="Файл", menu=filemenu, font=("", 14))
mainmenu.add_cascade(label="Инструменты", menu=toolsmenu, font=("", 14))
mainmenu.add_cascade(label="Справка", menu=helpmenu, font=("", 14))

equation_label = tkinter.Label(text="Введите уравнение:", font=("Arial", 14), bg='gray76')
equation_label.grid(row=0, column=0, sticky="NW", pady=30, padx=15)
ToolTip(equation_label, msg="Например: 1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

equation_entry = tkinter.Entry(width=50, font=("", 14))
equation_entry.grid(row=0, column=0, sticky="NW", pady=60, padx=15)

grid_label = tkinter.Label(text="Параметры сетки.", font=("Arial", 14), bg='gray76', foreground="forest green")
grid_label.grid(row=0, column=0, sticky="NW", pady=90, padx=15)

gridx_label = tkinter.Label(text="Параметры оси Х:", font=("Arial", 14), bg='gray76')
gridx_label.grid(row=0, column=0, sticky="NW", pady=120, padx=15)
# myTip = Hovertip(gridx_label, 'Введите в текстбоксы ограничения левой и правой \nграницы оси X', fontsize)
ToolTip(gridx_label, msg="Введите в текстбоксы ограничения оси X", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridx_min_entry = tkinter.Entry(width=10, font=("", 14))
gridx_min_entry.grid(row=0, column=0, sticky="NW", pady=150, padx=15)
ToolTip(gridx_min_entry, msg="Например: -8", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridx_max_entry = tkinter.Entry(width=10, font=("", 14))
gridx_max_entry.grid(row=0, column=0, sticky="NW", pady=150, padx=155)
ToolTip(gridx_max_entry, msg="Например: 8", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridy_label = tkinter.Label(text="Параметры оси Y:", font=("Arial", 14), bg='gray76')
gridy_label.grid(row=0, column=0, sticky="NW", pady=180, padx=15)
# myTip = Hovertip(gridy_label, 'Введите в текстбоксы ограничения левой и правой \nграницы оси Y')
ToolTip(gridy_label, msg="Введите в текстбоксы ограничения оси Y", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)


gridy_min_entry = tkinter.Entry(width=10, font=("", 14))
gridy_min_entry.grid(row=0, column=0, sticky="NW", pady=210, padx=15)
ToolTip(gridy_min_entry, msg="Например: -7", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridy_max_entry = tkinter.Entry(width=10, font=("", 14))
gridy_max_entry.grid(row=0, column=0, sticky="NW", pady=210, padx=155)
ToolTip(gridy_max_entry, msg="Например: 7", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

gridx_label = tkinter.Label(text="Введите длину стороны квадрата:", font=("Arial", 14), bg='gray76')
gridx_label.grid(row=0, column=0, sticky="NW", pady=250, padx=15)
ToolTip(gridx_label, msg="2s", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

grid_s_entry = tkinter.Entry(width=10, font=("", 14))
grid_s_entry.grid(row=0, column=0, sticky="NW", pady=280, padx=15)
ToolTip(gridy_max_entry, msg="Например: 8", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)

frame = tkinter.Frame(root, bg='gray76', highlightbackground="black", highlightthickness=2)
frame.grid(row=0, column=1, sticky="NW", padx=10, pady=60)

lyambda_label = tkinter.Label(frame, text="Параметры:", font=("Arial", 14), fg="forest green", bg='gray76')
lyambda_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)

lyambda1_label = tkinter.Label(frame, text="λ1 :", font=("Arial", 14), bg='gray76')
lyambda1_label.grid(row=1, column=0, sticky="W", padx=5, pady=5)

lyambda1_entry = tkinter.Entry(frame, width=10, font=("", 14))
lyambda1_entry.grid(row=1, column=1, sticky="W", padx=5, pady=5)

lamcoef_label = tkinter.Label(frame, text="Коэффициент увеличения λ :", font=("Arial", 14), bg='gray76')
lamcoef_label.grid(row=2, column=0, sticky="W", padx=5, pady=5)

lamcoef_entry = tkinter.Entry(frame, width=10, font=("", 14))
lamcoef_entry.grid(row=2, column=1, sticky="W", padx=5, pady=5)

speed_label = tkinter.Label(frame, text="Скорость (с) :", font=("Arial", 14), bg='gray76')
speed_label.grid(row=3, column=0, sticky="W", padx=5, pady=5)

speed_entry = tkinter.Entry(frame, width=10, font=("", 14))
speed_entry.grid(row=3, column=1, sticky="W", padx=5, pady=5)

r_label = tkinter.Label(frame, text="Гладкость функции (r) :", font=("Arial", 14), bg='gray76')
r_label.grid(row=4, column=0, sticky="W", padx=5, pady=5)

r_entry = tkinter.Entry(frame, width=10, font=("", 14))
r_entry.grid(row=4, column=1, sticky="W", padx=5, pady=5)

e_label = tkinter.Label(frame, text="Точность (е) :", font=("Arial", 14), bg='gray76')
e_label.grid(row=5, column=0, sticky="W", padx=5, pady=5)

e_entry = tkinter.Entry(frame, width=10, font=("", 14))
e_entry.grid(row=5, column=1, sticky="W", padx=5, pady=5)

params_button = tkinter.Button(master=frame, text="Сохранить", command=save_params,
                           font=("Arial", 10, "bold"))
params_button.grid(row=6, column=1, sticky="SE", pady=15, padx=5)

# Скрыть все элементы после r_entry
for widget in frame.winfo_children():
    if widget.grid_info()["row"] > 6:
        widget.grid_remove()




ok_button = tkinter.Button(master=root, text="Сгенерировать", command=get_equation, width=15, height=2,
                           font=("Arial", 10, "bold"))
ok_button.grid(row=0, column=0, sticky="NW", pady=320, ipadx=220, padx=15)

mas_button = tkinter.Button(master=root, text="Запустить алгоритм", command=main_algorithm, width=15, height=2,
                           font=("Arial", 10, "bold"))
mas_button.grid(row=0, column=0, sticky="NW", pady=380, ipadx=220, padx=15)

frame1 = tkinter.Frame(root, bg='gray76', highlightbackground="black", highlightthickness=2)
frame1.grid(row=0, column=0, sticky="NW", padx=10, pady=460)

point_label = tkinter.Label(frame1, text="Введите координаты точки (х, у)", font=("Helvetica 15 underline"), fg="forest green",
                            bg='gray76')
point_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)

point_x_label = tkinter.Label(frame1, text="X :", font=("Arial", 14), bg='gray76')
point_x_label.grid(row=2, column=0, sticky="W", padx=25, pady=5)

point_x_entry = tkinter.Entry(frame1, width=10, font=("", 14))
point_x_entry.grid(row=2, column=0, sticky="W", padx=90, pady=5)

point_y_label = tkinter.Label(frame1, text="Y :", font=("Arial", 14), bg='gray76')
point_y_label.grid(row=3, column=0, sticky="W", padx=25, pady=5)

point_y_entry = tkinter.Entry(frame1, width=10, font=("", 14))
point_y_entry.grid(row=3, column=0, sticky="W", padx=90, pady=5)

point_xy_button = tkinter.Button(master=frame1, text="Рассчитать значения", command=save_point,
                           font=("Arial", 10, "bold"))
point_xy_button.grid(row=4, column=0, sticky="W", pady=5, padx=75)

frame2 = tkinter.Frame(root, bg='gray76', highlightbackground="black", highlightthickness=2)
frame2.grid(row=0, column=1, sticky="NW", padx=10, pady=460)

result_label = tkinter.Label(frame2, text="Полученные значения", font=("Helvetica 15 underline"), fg="forest green",
                            bg='gray76')
result_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)

result_f_label = tkinter.Label(frame2, text="f ̃(x,y):", font=("Arial", 14), bg='gray76')
result_f_label.grid(row=2, column=0, sticky="W", padx=25, pady=5)

result_f_entry = tkinter.Entry(frame2, width=10, font=("", 14))
result_f_entry.grid(row=2, column=0, sticky="W", padx=90, pady=5)

result_dx_label = tkinter.Label(frame2, text="(∂f ̃)/∂x", font=("Arial", 14), bg='gray76')
result_dx_label.grid(row=3, column=0, sticky="W", padx=25, pady=5)

result_dx_entry = tkinter.Entry(frame2, width=10, font=("", 14))
result_dx_entry.grid(row=3, column=0, sticky="W", padx=90, pady=5)

result_dy_label = tkinter.Label(frame2, text="(∂f ̃)/∂y:", font=("Arial", 14), bg='gray76')
result_dy_label.grid(row=4, column=0, sticky="W", padx=25, pady=5)

result_dy_entry = tkinter.Entry(frame2, width=10, font=("", 14))
result_dy_entry.grid(row=4, column=0, sticky="W", padx=90, pady=5)



canvas0 = tkinter.Canvas(root,
                         bg='grey95',
                         borderwidth=10,
                         highlightthickness=10)
canvas0.grid(row=0, column=2, columnspan=1, sticky="NE", pady=15, padx=50)

fig = make_equation(-8, 8, -8, 8, 1, "1 - (x/8) ** 2 + 0.5 * sin(pi/4 * y)")
fig.set_size_inches(5.5, 4.5)


canvas = FigureCanvasTkAgg(fig, master=canvas0)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=1, sticky="NW")
canvas.draw()


toolbarFrame = tkinter.Frame(master=canvas0)
toolbarFrame.grid(row=0, column=2, sticky="NW", pady=2)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


# toolbar_button = tkinter.Button(master=root, text="Скрыть тулбар", command=lambda: tool_options(), width=15, height=2)
# toolbar_button.grid(row=1, column=4, rowspan=1, sticky="E", pady=10)

quit_button = tkinter.Button(master=root, text="Выход", command=_quit, width=15, height=2, font=("Arial", 14))
quit_button.grid(row=0, column=3, sticky="NE", ipadx=20, ipady=10, padx=30, pady=10)



root.mainloop()


