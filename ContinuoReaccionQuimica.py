import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SistemaReaccion:
    def __init__(self, k, A0, tiempo_total):
        self.k = k  # Constante de velocidad de la reacción (1/min)
        self.A0 = A0  # Concentración inicial de A (mol/L)
        self.tiempo_total = tiempo_total  # Tiempo total de simulación en minutos
        self.tiempo = np.linspace(0, self.tiempo_total, 1000)  # Tiempo de simulación en 1000 puntos

    def modelo(self, A, t):
        """Ecuación diferencial para la concentración de A"""
        dA_dt = -self.k * A
        return dA_dt

    def resolver(self):
        """Resuelve la ecuación diferencial"""
        solucion = odeint(self.modelo, self.A0, self.tiempo)
        return solucion

    def graficar(self, solucion):
        """Genera la gráfica de la concentración de A a lo largo del tiempo"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.tiempo, solucion, label='Concentración de [A]')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Concentración (mol/L)')
        plt.title('Descomposición de un Reactivo de Primer Orden')
        plt.grid(True)
        plt.legend()
        plt.show()

# Pedir al usuario los parámetros del sistema
k = int(input("Ingrese la constante de velocidad de la reacción (1/min): "))
A0 = int(input("Ingrese la concentración inicial de A (mol/L): "))
tiempo_total = int(input("Ingrese el tiempo de simulación (minutos): "))

# Crear una instancia de la clase SistemaReaccion
sistema = SistemaReaccion(k, A0, tiempo_total)

# Resolver la ecuación y graficar los resultados
solucion = sistema.resolver()
sistema.graficar(solucion)