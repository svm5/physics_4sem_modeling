import sys
import math
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

phi_1 = int(input("Введите угол, на который отклонён 1й маятник(°): "))
phi_2 = int(input("Введите угол, на который отклонён 2й маятник(°): ")) # градусы
phi_1 = math.radians(phi_1)
phi_2 = math.radians(phi_2)
d_phi_1 = 0
d_phi_2 = 0
dd_phi_1 = 0
dd_phi_2 = 0

dt = 0.01

L = float(input("Введите длину нити(м): "))
if (L <= 0):
    print("Длина нити должна быть положительной")
    sys.exit(1)

L1 =  float(input("Введите расстояние до пружины(м): "))
if (L1 <= 0):
    print("Расстояние должно быть положительным")
    sys.exit(1)

if (L1 > L):
    print("Расстояние до пружины не может быть больше длины нити:(")
    sys.exit(1)

dist = float(input("Введите расстояние м/д маятниками(м): "))
if (dist <= 0):
    print("Расстояние должно быть положительным")
    sys.exit(1)

beta = float(input("Введите к-т затухания: ")) # 0.1 # 0.5
if beta < 0:
    print("К-т затухания не может быть отрицательным")
    sys.exit(1)

m = float(input("Введите массу(кг): "))
if m <= 0:
    print("Масса должна быть положительной")
    sys.exit(1)

g = 9.81
k = float(input("Введите жёсткость пружины(H/м): ")) # 10 # 5
if k <= 0:
    print("К-т жесткости должен быть положительным")
    exit

arr_1 = []
arr_2 = []

def get_sin(phi):
    return round(math.sin(phi), 6)

def get_cos(phi):
    return round(math.cos(phi), 6)

def calc_delta_x(phi_1, phi_2):
    return ((L1 * get_sin(phi_2) + dist - L1 * get_sin(phi_1)) ** 2 + (L1 * get_cos(phi_2) - L1 * get_cos(phi_1)) ** 2) ** .5 - dist

def calc_frac_1():
    return (g / L) ** .5

def calc_frac_2():
    return (g / L + 2 * k * L1**2 / (m * L ** 2)) ** .5

def calc():
    global phi_1, phi_2, d_phi_1, d_phi_2, dd_phi_1, dd_phi_2
    prev_data = [phi_1, phi_2, d_phi_1, d_phi_2, dd_phi_1, dd_phi_2]
    
    arr_v_1 = []
    arr_v_2 = []
    N = 20000
    for _ in range(N):
        arr_1.append(phi_1)
        arr_2.append(phi_2)
        arr_v_1.append(d_phi_1)
        arr_v_2.append(d_phi_2)
        # print(calc_delta_x(phi_1, phi_2))
        dd_phi_1 = - g / L * get_sin(phi_1) - 2 * beta * d_phi_1 * (L1**2/L**2) + (k * L1) / (m * L ** 2) * calc_delta_x(phi_1, phi_2) * get_cos(phi_1)
        dd_phi_2 = - g / L * get_sin(phi_2) - 2 * beta * d_phi_2 * (L1**2/L**2) - (k * L1) / (m * L ** 2) * calc_delta_x(phi_1, phi_2) * get_cos(phi_2)
        d_phi_1 += dd_phi_1 * dt
        d_phi_2 += dd_phi_2 * dt
        phi_1 += d_phi_1 * dt
        phi_2 += d_phi_2 * dt
        
    t = [i * dt for i in range(N)]
    fig0, ax0 = plt.subplots(1, 2)
    ax0[0].plot(t, arr_1, label="Маятник 1")
    ax0[0].plot(t, arr_2, label="Маятник 2")
    ax0[0].set_title("Зависимость углов от времени")
    ax0[0].set_xlabel("t, c")
    ax0[0].set_ylabel("phi, рад")
    ax0[0].legend()
    ax0[0].grid()

    ax0[1].plot(t, arr_v_1, label="Маятник 1")
    ax0[1].plot(t, arr_v_2, label="Маятник 2")
    ax0[1].set_title("Зависимость скоростей от времени")
    ax0[1].set_xlabel("t, c")
    ax0[1].set_ylabel("d_phi/d_t, рад/с")
    ax0[1].legend()
    ax0[1].grid()

calc()

fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box')

t = np.linspace(0, 3, 4000)
hor_line = ax.plot([0, 300], [300, 300])
L *= 100
L1 *= 100
dist *= 100
offset = 100
m1 = ax.scatter(offset, 300 - L)
m1_line = ax.plot([offset, offset], [300, 300 - L])[0]
# print(offset + dist + L * get_sin(arr_2[0]), 300 - L * get_cos(arr_2[0]))
m2 = ax.scatter(offset + dist + L * get_sin(arr_2[0]), 300 - L * get_cos(arr_2[0]))
m2_line = ax.plot([offset + dist, offset + dist + L * get_sin(arr_2[0])], [300, 300 - L * get_cos(arr_2[0])])[0]
line_merge = ax.plot([offset, offset + L1 * get_sin(arr_2[0])], [300 - L1, 300 - L1 * get_cos(arr_2[0])])[0]

def update(frame):
    frame *= 2
    if (frame >= len(arr_1)):
        frame = len(arr_1) - 1
    m1.set_offsets([offset + L * get_sin(arr_1[frame]), 300 - L * get_cos(arr_1[frame])])
    m2.set_offsets([offset + dist + L * get_sin(arr_2[frame]), 300 - L * get_cos(arr_2[frame])])

    m1_line.set_xdata([offset, offset + L * get_sin(arr_1[frame])])
    m1_line.set_ydata([300, 300 - L * get_cos(arr_1[frame])])
    m2_line.set_xdata([offset + dist, offset + dist + L * get_sin(arr_2[frame])])
    m2_line.set_ydata([300, 300 - L * get_cos(arr_2[frame])])

    line_merge.set_xdata([offset + L1 * get_sin(arr_1[frame]), offset + dist + L1 * get_sin(arr_2[frame])])
    line_merge.set_ydata([300 - L1 * get_cos(arr_1[frame]), 300 - L1 * get_cos(arr_2[frame])])

    return (hor_line, m1, m2, m1_line, m2_line, line_merge)

ani = animation.FuncAnimation(fig=fig, func=update, interval=30)

print("Нормальная частота 1(Гц):", calc_frac_1())
print("Нормальная частота 2(Гц):", calc_frac_2())
plt.show()
