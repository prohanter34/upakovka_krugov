import numpy as np
from scipy.optimize import minimize


# функция-ограничение, определяющая, что круги не пересекаются
def constraint_func(x):
    n = len(x) // 2
    r = x[-1]
    constraints = []
    for i in range(n):
        for j in range(i+1, n):
            d = np.sqrt((x[i]-x[j])**2 + (x[i+n]-x[j+n])**2)
            constraints.append(d - 2*r)
    return constraints

# функция, которую хотим минимизировать, чтобы максимизировать r
def objective_func(x):
    return -x[-1]

# функция для нахождения радиуса кругов, удовлетворяющих ограничениям
def pack_circles_in_square(n):
    x0 = np.zeros(2*n+1) # начальное приближение
    x0[-1] = 1 # начинаем с максимально возможного радиуса
    bounds = [(0, 1) for i in range(2*n+1)] # ограничения на все переменные

    # добавим ограничения на расположение кругов внутри квадрата
    constraints = []
    for i in range(n):
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: x[i] - x[-1]})
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: -x[i] + 1 - x[-1]})
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: x[i+n] - x[-1]})
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: -x[i+n] + 1 - x[-1]})

    res = minimize(objective_func, x0, bounds=bounds, constraints=[{'fun': constraint_func, 'type': 'ineq'}] + constraints)
    r = res.x[-1]
    circles = [(res.x[i], res.x[i+n], r) for i in range(n)]

    return circles


import matplotlib.pyplot as plt

# функция для рисования упаковки кругов
def plot_circles(circles):
    fig, ax = plt.subplots(figsize=(5, 5))
    for circle in circles:
        ax.add_artist(plt.Circle((circle[0], circle[1]), circle[2], color='b', fill=False))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()

# пример использования для n=5
#circles = pack_circles_in_square(n=13)
#plot_circles(circles)
#print(circles)

for n in range(1, 30):
    circles = pack_circles_in_square(n=n)
    print(circles)
    plot_circles(circles)
