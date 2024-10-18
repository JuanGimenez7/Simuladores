import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class ReactorSimulacion:
    def __init__(self, Q_gen, k, T_cool, C, T0, tiempo_simulacion):
        self.Q_gen = Q_gen  # Tasa de generación de calor (W)
        self.k = k  # Coeficiente de enfriamiento (W/°C)
        self.T_cool = T_cool  # Temperatura del sistema de enfriamiento (°C)
        self.C = C  # Capacidad térmica del reactor (J/°C)
        self.T0 = T0  # Temperatura inicial del reactor (°C)
        self.tiempo = np.linspace(0, tiempo_simulacion, 10000)  # Tiempo de simulación (minutos)

    def modelo(self, T, t):
        """Ecuación diferencial para la variación de la temperatura."""
        dT_dt = (self.Q_gen / self.C) - self.k * (T - self.T_cool)
        return dT_dt

    def resolver(self):
        """Resuelve la ecuación diferencial."""
        solucion = odeint(self.modelo, self.T0, self.tiempo)
        return solucion

    def graficar(self, solucion):
        """Genera la gráfica de la temperatura del reactor a lo largo del tiempo."""
        plt.figure(figsize=(10, 5))
        plt.plot(self.tiempo, solucion, label='Temperatura del Reactor')
        plt.axhline(self.T_cool, color='red', linestyle='--', label='Temperatura del Sistema de Enfriamiento')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Enfriamiento del Reactor Nuclear')
        plt.grid(True)
        plt.legend()
        plt.show()

# Pedir al usuario los parámetros del sistema
Q_gen = float(input("Ingrese la tasa de generación de calor en vatios (W): "))
k = float(input("Ingrese el coeficiente de enfriamiento (W/°C): "))
T_cool = float(input("Ingrese la temperatura del sistema de enfriamiento en grados Celsius (°C): "))
C = float(input("Ingrese la capacidad térmica del reactor (J/°C): "))
T0 = float(input("Ingrese la temperatura inicial del reactor: "))
tiempo_simulacion = float(input("Ingrese el tiempo de simulación en minutos: "))

# Crear una instancia de la simulación del reactor
reactor = ReactorSimulacion(Q_gen, k, T_cool, C, T0, tiempo_simulacion)

# Resolver la ecuación diferencial y graficar los resultados
solucion = reactor.resolver()
reactor.graficar(solucion)