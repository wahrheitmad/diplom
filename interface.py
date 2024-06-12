import tkinter
from idlelib.tooltip import Hovertip
from tkinter import filedialog, messagebox, ttk
from tkinter.filedialog import asksaveasfile

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from numpy import sin, cos
from scipy.interpolate import interp2d, bisplrep, bisplev
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
x_int = []
y_int = []
z_int = []

def get_equation():
    global g, x_int, y_int, z_int, toolbar, toolbarFrame
    isEmpty = False
    dict = {
        'Уравнение': equation_entry.get(),
        'x_min:': gridx_min_entry.get(),
        'x_max': gridx_max_entry.get(),
        'y_min': gridy_min_entry.get(),
        'y_max': gridy_max_entry.get(),
        's': grid_s_entry.get()
    }

    for key, value in dict.items():
        if value.strip() == '':
            isEmpty = True
        else:
            isEmpty = False
    if isEmpty:
        messagebox.showinfo(title="Предупреждение",
                            message="Пожалуйста, заполните все поля!")
    else:
        equation = equation_entry.get()
        x_min = int(float(gridx_min_entry.get()))
        x_max = int(float(gridx_max_entry.get()))
        y_min = int(float(gridy_min_entry.get()))
        y_max = int(float(gridy_max_entry.get()))
        length = float(grid_s_entry.get())/2
        g = Equation(x_min, x_max, y_min, y_max, length, equation)
        x_int = copy(g.x_)
        y_int = copy(g.y_)
        z_int = copy(g.z_)
        messagebox.showinfo(title="Успешно", message="Создана сетка [{0}, {1}] x [{2}, {3}], сторона квадрата: {4}. Уравнение: {5}".format(x_min, x_max, y_min, y_max, length, equation))
        # g = Equation(x_min, x_max, y_min, y_max, length, equation)
        x = g.x_values()
        y = g.y_values()
        fig = make_equation(x_min, x_max, y_min, y_max, length, equation)
        fig.set_size_inches(5.5, 4.5)

        canvas = FigureCanvasTkAgg(fig, master=canvas0)
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=1, sticky="NW")
        canvas.draw()
        toolbarFrame = tkinter.Frame(master=canvas0)
        toolbarFrame.grid(row=0, column=2, sticky="NW", pady=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
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
    isEmpty = False
    dict = {
        'λ1': lyambda1_entry.get(),
        'Коэффициент увеличения λ:': lamcoef_entry.get(),
        'r': r_entry.get(),
        'c': speed_entry.get(),
        'e': e_entry.get()
    }

    for key, value in dict.items():
        if value.strip() == '':
            isEmpty = True
        else:
            isEmpty = False
    if isEmpty:
        messagebox.showinfo(title="Предупреждение",
                            message="Пожалуйста, заполните все параметры!")
    else:
        lyambda1 = float(lyambda1_entry.get())
        lamcoef = float(lamcoef_entry.get())
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
    isEmpty = False
    dict = {
        'x': point_x_entry.get(),
        'y:': point_y_entry.get(),
    }

    for key, value in dict.items():
        if value.strip() == '':
            isEmpty = True
        else:
            isEmpty = False
    if isEmpty:
        messagebox.showinfo(title="Предупреждение",
                            message="Пожалуйста, заполните все параметры!")
    else:
        y = float(point_y_entry.get())
        x = float(point_x_entry.get())
        # fz = find_point(x,y)
        messagebox.showinfo(title="Успешно", message="Точка сохранена")
        interpolator = bisplrep(np.array(x_int), np.array(y_int), np.array(z_int),)
        fz = bisplev(np.array(x), np.array(y), interpolator)
        messagebox.showinfo(title="Успешно", message="Значения найдены")
        result_f_entry.insert(0, fz)
    # result_dx_entry.insert(0, fz)
    # result_dy_entry.insert(0, fz)


def find_point(x, y):
    global lyambda0
    fz = point(g.count, x, y, g.x_, g.y_, sigma, lyambda0, m, 3)
    return fz



def open_file():
    global s
    def check():
        global s
        s = int(entry.get())/2
        g.s = s
        root1.destroy()
    global g, x_int, y_int, z_int
    filepath = filedialog.askopenfilename()
    x, y, z = read_from_excel(filepath)
    g = Equation(x=x, y=y, z=z, length=10)
    x = copy(g.x_)
    y = copy(g.y_)
    xgrid, ygrid = np.meshgrid(x, y)
    interpolator = bisplrep(np.array(g.x_), np.array(g.y_), np.array(g.z_))
    zgrid = bisplev(np.array(g.x_), np.array(g.y_), interpolator)
    fig = plt.figure(figsize=(12, 7))
    fig.set_size_inches(5.5, 4.5)
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.plot_surface(xgrid, ygrid, zgrid, cmap='viridis')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    canvas = FigureCanvasTkAgg(fig, master=canvas0)
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=1, sticky="NW")
    canvas.draw()
    toolbarFrame = tkinter.Frame(master=canvas0)
    toolbarFrame.grid(row=0, column=2, sticky="NW", pady=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    x_int = copy(g.x_)
    y_int = copy(g.y_)
    z_int = copy(g.z_)
    root1 = tkinter.Tk()
    label = tkinter.Label(root1, text="Введите параметр s:", font=("Arial", 14), bg='gray76')
    label.grid()
    entry = tkinter.Entry(root1)
    entry.grid(pady=10)
    button = tkinter.Button(root1, text='Передать', command=check)
    button.grid()
    root1.mainloop()
    # length = int(grid_s_entry.get()) / 2

    # root1.quit()  # остановка цикла


def save_to_table():
    def saveex():
        x1, y1, z1 = get_points()
        df = pd.DataFrame({'x': x1,
                           'y': y1,
                           'z': z1})
        file = asksaveasfile(initialfile='Untitled',
                             defaultextension=".xlsx", filetypes=[("All Files", "*.*"), ("Excel Documents", "*.xlsx")])
        if file is not None:
            df.to_excel(file.name, index=False)
            file.close()
            print("DataFrame saved to", file.name)
            messagebox.showinfo(title="Успешно", message="Файл сохранен по пути {0}".format(file.name))
        else:
            print("File save cancelled")

    def get_points():
        x_min = int(float(x_min_entry.get()))
        x_max = int(float(x_max_entry.get()))
        x_step = float(x_step_entry.get())
        y_min = int(float(y_min_entry.get()))
        y_max = int(float(y_max_entry.get()))
        y_step = float(y_step_entry.get())
        x_mas = []
        x_temp = copy(x_min)
        y_temp = copy(y_min)
        y_mas = []
        for x in np.arange(x_min, x_max + x_step, x_step):
            x_mas.append(x)
        for y in np.arange(y_min, y_max + y_step, y_step):
            y_mas.append(y)
        interpolator = bisplrep(np.array(x_int), np.array(y_int), np.array(z_int), )
        # fz = bisplev(np.array(x_mas), np.array(y_mas), interpolator)
        points = []
        z1 = []
        for i in range(len(x_mas)):
            for j in range(len(x_mas)):
                z1.append(bisplev(np.array(x_mas[i]), np.array(y_mas[j]), interpolator))
                points.append((x_mas[i], y_mas[j], bisplev(np.array(x_mas[i]), np.array(y_mas[j]), interpolator)))
        # добавляем данные
        print(points)
        for point in points:
            tree.insert("", 'end', values=point)

        x1 = []
        y1 = []
        for x in np.arange(x_min, x_max + x_step, x_step):
            for y in np.arange(y_min, y_max + y_step, y_step):
                x1.append(x)
                y1.append(y)
        return x1, y1, z1


    rt = tkinter.Tk()
    rt.geometry("700x950")
    rt.wm_title("Сохранить в таблицу")
    rt.configure(bg='gray76')


    # определяем столбцы
    columns = ("x", "y", "z")

    gridx_label = tkinter.Label(rt, text="Параметры оси Х:", font=("Arial", 14), bg='gray76')
    gridx_label.grid(row=0, column=0, sticky="NW", pady=60, padx=35)
    # myTip = Hovertip(gridx_label, 'Введите в текстбоксы ограничения левой и правой \nграницы оси X', fontsize)
    ToolTip(gridx_label, msg="Введите в текстбоксы ограничения оси X", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)

    x_min_entry = tkinter.Entry(rt, width=10, font=("", 14))
    x_min_entry.grid(row=0, column=0, sticky="NW", pady=90, padx=35)
    ToolTip(x_min_entry, msg="Например: -8", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)
    x_min_entry.bind("<FocusOut>", validate_digit_input)

    x_max_entry = tkinter.Entry(rt, width=10, font=("", 14))
    x_max_entry.grid(row=0, column=0, sticky="NW", pady=90, padx=175)
    ToolTip(x_max_entry, msg="Например: 8", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)
    x_max_entry.bind("<FocusOut>", validate_digit_input1)

    x_step_label = tkinter.Label(rt, text="Шаг по оси Х:", font=("Arial", 14), bg='gray76')
    x_step_label.grid(row=0, column=0, sticky="NW", pady=60, padx=325)
    # myTip = Hovertip(gridx_label, 'Введите в текстбокс шаг по оси X', fontsize)
    ToolTip(x_step_label, msg="Введите в текстбокс шаг по оси X", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)

    x_step_entry = tkinter.Entry(rt, width=10, font=("", 14))
    x_step_entry.grid(row=0, column=0, sticky="NW", pady=90, padx=325)
    ToolTip(x_step_entry, msg="Например: 1", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)
    gridx_min_entry.bind("<FocusOut>", validate_digit_input)

    y_label = tkinter.Label(rt, text="Параметры оси Y:", font=("Arial", 14), bg='gray76')
    y_label.grid(row=0, column=0, sticky="NW", pady=120, padx=35)
    # myTip = Hovertip(gridy_label, 'Введите в текстбоксы ограничения левой и правой \nграницы оси Y')
    ToolTip(y_label, msg="Введите в текстбоксы ограничения оси Y", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)

    y_min_entry = tkinter.Entry(rt, width=10, font=("", 14))
    y_min_entry.grid(row=0, column=0, sticky="NW", pady=150, padx=35)
    ToolTip(y_min_entry, msg="Например: -7", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)
    y_min_entry.bind("<FocusOut>", validate_digit_input2)

    y_max_entry = tkinter.Entry(rt, width=10, font=("", 14))
    y_max_entry.grid(row=0, column=0, sticky="NW", pady=150, padx=175)
    ToolTip(y_max_entry, msg="Например: 7", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)
    y_max_entry.bind("<FocusOut>", validate_digit_input3)

    y_step_label = tkinter.Label(rt, text="Шаг по оси Y:", font=("Arial", 14), bg='gray76')
    y_step_label.grid(row=0, column=0, sticky="NW", pady=120, padx=325)
    # myTip = Hovertip(gridx_label, 'Введите в текстбокс шаг по оси X', fontsize)
    ToolTip(y_step_label, msg="Введите в текстбокс шаг по оси Y", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)

    y_step_entry = tkinter.Entry(rt, width=10, font=("", 14))
    y_step_entry.grid(row=0, column=0, sticky="NW", pady=150, padx=325)
    ToolTip(y_step_entry, msg="Например: 1", delay=1,
            parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
            fg="black", bg="white", padx=10, pady=10)
    gridx_min_entry.bind("<FocusOut>", validate_digit_input)

    okk_button = tkinter.Button(master=rt, text="Показать значения", command=get_points, width=19, height=2,
                               font=("Arial", 10, "bold"))
    okk_button.grid(row=0, column=0, sticky="NW", pady=230, ipadx=220, padx=35)

    saveex_button = tkinter.Button(master=rt, text="Сохранить в ...", command=saveex, width=19, height=2,
                                font=("Arial", 10, "bold"))
    saveex_button.grid(row=0, column=0, sticky="NW", pady=280, ipadx=220, padx=35)

    tree = ttk.Treeview(rt, columns=columns, show="headings", height=25)
    tree.grid(row=0, column=0, sticky="NW", pady=350, padx=35)

    # определяем заголовки
    tree.heading("x", text="x")
    tree.heading("y", text="y")
    tree.heading("z", text="z")
    # Добавляем вертикальную полосу прокрутки
    vsb = ttk.Scrollbar(rt, orient="vertical", command=tree.yview)
    vsb.grid(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)



    rt.mainloop()


def save_to_excel():
    df = pd.DataFrame({'x': g.x_,
                       'y': g.y_,
                       'z': g.z_})
    file = asksaveasfile(initialfile='Untitled',
                      defaultextension=".xlsx", filetypes=[("All Files", "*.*"), ("Excel Documents", "*.xlsx")])
    if file is not None:
        df.to_excel(file.name, index=False)
        file.close()
        print("DataFrame saved to", file.name)
        messagebox.showinfo(title="Успешно", message="Файл сохранен по пути {0}".format(file.name))
    else:
        print("File save cancelled")


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
    # result_dx_entry.delete(0, tkinter.END)
    result_f_entry.delete(0, tkinter.END)
    # result_dy_entry.delete(0, tkinter.END)


def validate_equation_input(event):
    dig = 0
    let = 0
    ops = 0
    value = equation_entry.get()
    chars = ['/', '*', '-', '+', '**']
    for i in value:
        # if i.isdigit():
        #     dig += 1
        if i.isalpha():
            let += 1
        if i in chars:
            ops += 1
    if let == 0 or ops == 0:
        messagebox.showinfo(title="Внимание", message="Введенная строка не является уравнением")

def validate_digit_input(event):
    value = gridx_min_entry.get()
    if value.isalpha():
        messagebox.showinfo(title="Внимание", message="Данный параметр должен быть числом")

def validate_digit_input1(event):
    value = gridx_max_entry.get()
    if value.isalpha():
        messagebox.showinfo(title="Внимание", message="Данный параметр должен быть числом")

def validate_digit_input2(event):
    value = gridy_min_entry.get()
    if value.isalpha():
        messagebox.showinfo(title="Внимание", message="Данный параметр должен быть числом")

def validate_digit_input3(event):
    value = gridy_max_entry.get()
    if value.isalpha():
        messagebox.showinfo(title="Внимание", message="Данный параметр должен быть числом")

def validate_digit_input4(event):
    value = grid_s_entry.get()
    if value.isalpha():
        messagebox.showinfo(title="Внимание", message="Данный параметр должен быть числом")

def validate_int_input(event):
    value = r_entry.get()
    if '.' in value:
        messagebox.showinfo(title="Внимание", message="Данный параметр должен быть целым числом")

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
filemenu.add_command(label="Сохранить...", command=save_to_excel, font=("", 14))
filemenu.add_command(label="Вывести значения в таблицу", command=save_to_table, font=("", 14))
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
equation_entry.bind("<FocusOut>", validate_equation_input)

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
gridx_min_entry.bind("<FocusOut>", validate_digit_input)

gridx_max_entry = tkinter.Entry(width=10, font=("", 14))
gridx_max_entry.grid(row=0, column=0, sticky="NW", pady=150, padx=155)
ToolTip(gridx_max_entry, msg="Например: 8", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)
gridx_max_entry.bind("<FocusOut>", validate_digit_input1)

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
gridy_min_entry.bind("<FocusOut>", validate_digit_input2)

gridy_max_entry = tkinter.Entry(width=10, font=("", 14))
gridy_max_entry.grid(row=0, column=0, sticky="NW", pady=210, padx=155)
ToolTip(gridy_max_entry, msg="Например: 7", delay=1,
        parent_kwargs={"bg": "grey", "padx": 5, "pady": 5},
        fg="black", bg="white", padx=10, pady=10)
gridy_max_entry.bind("<FocusOut>", validate_digit_input3)

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
grid_s_entry.bind("<FocusOut>", validate_digit_input4)

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
r_entry.bind("<FocusOut>", validate_int_input)

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

# result_dx_label = tkinter.Label(frame2, text="(∂f ̃)/∂x", font=("Arial", 14), bg='gray76')
# result_dx_label.grid(row=3, column=0, sticky="W", padx=25, pady=5)
#
# result_dx_entry = tkinter.Entry(frame2, width=10, font=("", 14))
# result_dx_entry.grid(row=3, column=0, sticky="W", padx=90, pady=5)
#
# result_dy_label = tkinter.Label(frame2, text="(∂f ̃)/∂y:", font=("Arial", 14), bg='gray76')
# result_dy_label.grid(row=4, column=0, sticky="W", padx=25, pady=5)
#
# result_dy_entry = tkinter.Entry(frame2, width=10, font=("", 14))
# result_dy_entry.grid(row=4, column=0, sticky="W", padx=90, pady=5)



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


