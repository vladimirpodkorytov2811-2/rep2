import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import math


# Читаем файл
with open("эксперимент_2027-09-16_14-16-53.txt", "r", encoding="utf-8") as file:
    data = []

    for line in file:
        line = line.strip()

        if line and not line.startswith("#"):
            data.append(int(line))


# Объединяем каждые 40 измерений (40 секунд)
experiments = []

for i in range(0, len(data), 40):
    group = data[i:i+40]

    if len(group) == 40:
        experiments.append(sum(group))


N = len(experiments)

print("Количество опытов:", N)


# Среднее количество срабатываний за 40 секунд
mean = np.mean(experiments)


# Экспериментальное среднеквадратическое отклонение
sigma = np.sqrt(np.mean((np.array(experiments)-mean)**2))


# Теоретическое отклонение Пуассона
sigma_poisson = np.sqrt(mean)


print("Среднее число срабатываний:", mean)
print("Экспериментальная sigma:", sigma)
print("sqrt(среднего числа срабатываний):", sigma_poisson)


# ===== ЭКСПЕРИМЕНТАЛЬНАЯ ГИСТОГРАММА =====

counts = Counter(experiments)

x = np.array(sorted(counts.keys()))

y = np.array([
    counts[value]/N
    for value in x
])


plt.bar(
    x,
    y,
    width=1,
    edgecolor="black",
    alpha=0.6,
    label="Эксперимент (40 секунд)"
)


# ===== НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ =====

x_line = np.linspace(min(x)-2, max(x)+2, 500)

normal = (
    1/(sigma*np.sqrt(2*np.pi))
    *
    np.exp(
        -(x_line-mean)**2/(2*sigma**2)
    )
)


plt.plot(
    x_line,
    normal,
    linewidth=2,
    label=f"Нормальное распределение σ={sigma:.2f}"
)


# ===== РАСПРЕДЕЛЕНИЕ ПУАССОНА =====

poisson = []

for k in x:
    p = (
        mean**k
        *
        math.exp(-mean)
        /
        math.factorial(k)
    )
    poisson.append(p)


plt.plot(
    x,
    poisson,
    "o-",
    linewidth=2,
    label=f"Пуассон σ=√n={sigma_poisson:.2f}"
)


# ===== ОФОРМЛЕНИЕ =====

plt.xlabel("Количество срабатываний за 40 секунд")
plt.ylabel("Вероятность")
plt.title("Распределение срабатываний счётчика Гейгера (40 секунд)")

plt.legend()
plt.grid(alpha=0.3)

plt.show()