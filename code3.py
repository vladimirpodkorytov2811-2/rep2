import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import math


# ================= ЧТЕНИЕ ФАЙЛА =================

with open("эксперимент_2027-09-16_14-16-53.txt", "r", encoding="utf-8") as file:
    data = []

    for line in file:
        line = line.strip()

        if line and not line.startswith("#"):
            data.append(int(line))


# ================= ФУНКЦИЯ ОБРАБОТКИ =================

def process_data(step):
    experiments = []

    for i in range(0, len(data), step):
        group = data[i:i+step]

        if len(group) == step:
            experiments.append(sum(group))

    N = len(experiments)

    mean = np.mean(experiments)

    sigma = np.sqrt(
        np.mean((np.array(experiments)-mean)**2)
    )

    sigma_poisson = np.sqrt(mean)

    counts = Counter(experiments)

    x = np.array(sorted(counts.keys()))

    y = np.array([
        counts[value]/N
        for value in x
    ])

    return experiments, x, y, mean, sigma, sigma_poisson


# Обработка 20 и 40 секунд

exp20, x20, y20, mean20, sigma20, sp20 = process_data(20)
exp40, x40, y40, mean40, sigma40, sp40 = process_data(40)


print("===== 20 секунд =====")
print("Количество опытов:", len(exp20))
print("Среднее:", mean20)
print("sigma эксперимент:", sigma20)
print("корень среднего:", sp20)
print("Абсолютная погрешность:", sigma20/200**0.5)
print("Относительная погрешность:", str((sigma20/200**0.5)/mean20*100)+"%")


print("\n===== 40 секунд =====")
print("Количество опытов:", len(exp40))
print("Среднее:", mean40)
print("sigma эксперимент:", sigma40)
print("sкорень среднего:", sp40)
print("Абсолютная погрешность:", sigma40/100**0.5)
print("Относительная погрешность:", str((sigma40/100**0.5)/mean40*100)+"%")

print("\n20 секунд:")

for k, theory in [(1, 68), (2, 95), (3, 99.7)]:
    inside = sum(
        abs(x - mean20) <= k * sigma20
        for x in exp20
    )

    percent = inside / len(exp20) * 100

    print(
        f"• В интервал ±{k}σ попало {inside} отсчётов "
        f"({percent:.1f}%). Теоретическое ожидание: {theory}%."
    )

print("\n40 секунд:")

for k, theory in [(1, 68), (2, 95), (3, 99.7)]:
    inside = sum(
        abs(x - mean40) <= k * sigma40
        for x in exp40
    )

    percent = inside / len(exp40) * 100

    print(
        f"• В интервал ±{k}σ попало {inside} отсчётов "
        f"({percent:.1f}%). Теоретическое ожидание: {theory}%."
    )

# ================= ГРАФИК =================


plt.figure(figsize=(12,7))


# -------- 20 секунд --------

plt.bar(
    x20,
    y20,
    width=1,
    alpha=0.35,
    edgecolor="black",
    label="Эксперимент 20 секунд"
)


x_line20 = np.linspace(min(x20)-2, max(x20)+2, 500)


normal20 = (
    1/(sigma20*np.sqrt(2*np.pi))
    *
    np.exp(
        -(x_line20-mean20)**2/(2*sigma20**2)
    )
)


plt.plot(
    x_line20,
    normal20,
    color="red",
    linewidth=2,
    label=f"Нормальное 20 с (σ={sigma20:.2f})"
)


poisson20 = []

for k in x20:
    poisson20.append(
        mean20**k *
        math.exp(-mean20) /
        math.factorial(k)
    )


plt.plot(
    x20,
    poisson20,
    color="darkred",
    marker="o",
    linewidth=2,
    label=f"Пуассон 20 с (√n={sp20:.2f})"
)



# -------- 40 секунд --------

plt.bar(
    x40,
    y40,
    width=1,
    alpha=0.35,
    edgecolor="black",
    label="Эксперимент 40 секунд"
)


x_line40 = np.linspace(min(x40)-2, max(x40)+2, 500)


normal40 = (
    1/(sigma40*np.sqrt(2*np.pi))
    *
    np.exp(
        -(x_line40-mean40)**2/(2*sigma40**2)
    )
)


plt.plot(
    x_line40,
    normal40,
    color="blue",
    linewidth=2,
    label=f"Нормальное 40 с (σ={sigma40:.2f})"
)


poisson40 = []

for k in x40:
    poisson40.append(
        mean40**k *
        math.exp(-mean40) /
        math.factorial(k)
    )


plt.plot(
    x40,
    poisson40,
    color="green",
    marker="o",
    linewidth=2,
    label=f"Пуассон 40 с (√n={sp40:.2f})"
)



# ================= ОФОРМЛЕНИЕ =================

plt.xlabel("Количество срабатываний счётчика")
plt.ylabel("Вероятность")
plt.title(
    "Распределение срабатываний счётчика Гейгера\n"
    "Сравнение измерений 20 и 40 секунд"
)

plt.legend()
plt.grid(alpha=0.3)

plt.show()