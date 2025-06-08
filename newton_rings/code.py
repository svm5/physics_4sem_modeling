import math

import matplotlib.pyplot as plt

def wavelength_to_rgb(wave_length):
    w = int(wave_length)
    if w >= 380 and w < 440:
        R = -(w - 440) / (440 - 350)
        G = 0.0
        B = 1.0
    elif w >= 440 and w < 490:
        R = 0.0
        G = (w - 440) / (490 - 440)
        B = 1.0
    elif w >= 490 and w < 510:
        R = 0.0
        G = 1.0
        B = -(w - 510) / (510 - 490)
    elif w >= 510 and w < 580:
        R = (w - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif w >= 580 and w < 645:
        R = 1.0
        G = -(w - 645) / (645 - 580)
        B = 0.0
    elif w >= 645 and w <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    if w >= 380 and w < 420:
        factor = 0.3 + 0.7 * (w - 380) / (420 - 380)
    elif w >= 420 and w <= 700:
        factor = 1.0
    elif w > 700 and w <= 780:
        factor = 0.3 + 0.7 * (780 - w) / (780 - 700)
    else:
        factor = 0.0
    
    R = (R * factor) ** .8
    G = (G * factor) ** .8
    B = (B * factor) ** .8
    return [R, G, B]


def intensity(r, R, wave_length):
    # print(r, R, wave_length)
    return 1 / 2 * (1 + round(math.cos((2 * math.pi * r ** 2) / (wave_length * R) + math.pi), 10))


def quasi_monochromatic_intensity(r, R, wave_length, spectrum_width):
    K = 10
    delta = spectrum_width / K
    summa = 0
    for i in range(K):
        current_length = wave_length - spectrum_width / 2 + delta * i
        current_i = intensity(r, R, current_length)
        summa += current_i

    return summa / K

def wide_intensity(r, R, left, right):
    # left = 380 * 10 ** -9 # 380 * 10 ** -9
    # right = 780 * 10 ** -9 # 750 * 10 ** -9
    P = 10
    delta = (right - left) / P
    lengths = [left + i * delta for i in range(P + 1)]
    I = [[0 for _ in range(N)] for _ in range(N)]
    image = [[[0 for _ in range(3)] for _ in range(N)] for _ in range(N)]
    for current_length in lengths:
        for i in range(N):
            for j in range(N):
                current_intensity = intensity(r[i][j], R, current_length)
                I[i][j] += current_intensity
                current_color = wavelength_to_rgb(current_length * 10 ** 9)
                for k in range(3):
                    image[i][j][k] += current_intensity * current_color[k]

    mx = -1
    for i in range(N):
        for j in range(N):
            I[i][j] /= P
            for k in range(3):
                mx = max(mx, image[i][j][k])
    for i in range(N):
        for j in range(N):
            for k in range(3):
                image[i][j][k] /= mx

    return I, image

R = float(input("Радиус линзы: "))

# is_white = int(input("Белый свет(0 или 1)?: "))
# if is_white == 0:
#     is_white = False
# else:
#     is_white = True

# if is_white is False:
wave_length = float(input("Середина спектра(нм): "))
spectrum_width = float(input("Ширина спектра(нм): "))
wave_length *= 10 ** (-9)
spectrum_width *= 10 ** (-9)
# R = 0.7
# wave_length = 460 * 10 ** (-9)
# spectrum_width = 0 # 30 * 10 ** (-9)

W = 3
width = W * 10 ** (-3)
N = 500
dt = 2 * width / N
x = []
y = []
for i in range(N):
    x.append(round(-width + i * dt, 7))
    y.append(round(-width + i * dt, 7))
r = [[0 for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        r[i][j] = (y[i] ** 2 + x[j] ** 2) ** .5

I = [[0 for _ in range(N)] for _ in range(N)]
image = [[[0 for _ in range(3)] for _ in range(N)] for _ in range(N)]
# print("IS WHITE", is_white)
# if is_white is False:
# color = wavelength_to_rgb(wave_length * 10 ** 9)
if spectrum_width == 0:
    for i in range(N):
        for j in range(N):
            if spectrum_width == 0:
                I[i][j] = intensity(r[i][j], R, wave_length)
            else:
                I[i][j] = quasi_monochromatic_intensity(r[i][j], R, wave_length, spectrum_width)

    color = wavelength_to_rgb(wave_length * 10 ** 9)
    image = [[[0 for _ in range(3)] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(3):
                image[i][j][k] = I[i][j] * color[k]
else:
    left = wave_length - spectrum_width / 2
    right = wave_length + spectrum_width / 2
    I, image = wide_intensity(r, R, left, right)
# else:
#     I, image = white_intensity(r, R)

plt.subplot(1, 2, 1)
plt.imshow(image, extent=[-W, W, -W, W])
plt.title("Кольца Ньютона")
plt.xlabel("x (мм)")
plt.ylabel("y (мм)")

plt.subplot(1, 2, 2)
mem = dict()
for i in range(N):
    for j in range(N):
        mem[r[i][j]] = I[i][j]
x_values = sorted(mem.keys())
y_values = [mem[key] for key in x_values]
plt.plot([elem * 1000 for elem in x_values], y_values)
plt.title("Интенсивность от радиальной координаты")
plt.xlabel("Радиус (мм)")
plt.ylabel("Интенсивность")
plt.grid()
plt.show()
