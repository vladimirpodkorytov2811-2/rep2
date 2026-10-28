import time
from mcp3021_driver import MCP3021
import adc_plot

# Замени 5.0 на динамический диапазон, измеренный на контакте PWR блока AUX
dynamic_range = 5.0

voltage_values = []
time_values = []
duration = 10.0

adc = None

try:
    adc = MCP3021(dynamic_range)

    start_time = time.time()

    while time.time() - start_time < duration:
        voltage = adc.get_voltage()
        voltage_values.append(voltage)
        time_values.append(time.time() - start_time)

    # Задание 8: график
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

    # Задание 9: гистограмма
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    if adc is not None:
        adc.deinit()
