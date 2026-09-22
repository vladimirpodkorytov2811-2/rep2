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


# Объединяем по 20 измерений
experiments = []

for i in range(0, len(data), 20):
    group = data[i:i+20]

    if len(group) == 20:
        experiments.append(sum(group))


N = len(experiments)

print("Количество опытов:", N)


# Среднее значение
mean = np.mean(experiments)


# Среднеквадратическое отклонение из эксперимента
sigma = np.sqrt(np.mean((np.array(experiments) - mean)**2))


# Сигма из распределения Пуассона
sigma_poisson = np.sqrt(mean)


print("Среднее число срабатываний:", mean)
print("Экспериментальная sigma:", sigma)
print("sqrt(N среднего):", sigma_poisson)


# Экспериментальная гистограмма
counts = Counter(experiments)

x = np.array(sorted(counts.keys()))
y = np.array([counts[i] / N for i in x])


plt.bar(
    x,
    y,
    width=1,
    edgecolor="black",
    alpha=0.6,
    label="Эксперимент"
)


# ===== НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ =====

x_line = np.linspace(min(x)-1, max(x)+1, 500)

normal = (
    1 / (sigma * np.sqrt(2*np.pi))
    * np.exp(-(x_line-mean)**2 / (2*sigma**2))
)


# Масштабируем плотность под шаг 1
normal *= 1


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
        * math.exp(-mean)
        / math.factorial(k)
    )
    poisson.append(p)


plt.plot(
    x,
    poisson,
    "o-",
    linewidth=2,
    label=f"Пуассон σ=√n={sigma_poisson:.2f}"
)


# Оформление
plt.xlabel("Количество срабатываний за 20 секунд")
plt.ylabel("Вероятность")
plt.title("Распределение срабатываний счётчика Гейгера")

plt.legend()
plt.grid(alpha=0.3)

plt.show()