import random
import simpy
import math

class PeluqueriaSimulacion:
    def __init__(self, semilla, num_peluqueros, tiempo_corte_min, tiempo_corte_max, t_llegadas, tot_clientes):
        self.semilla = semilla
        self.num_peluqueros = num_peluqueros
        self.tiempo_corte_min = tiempo_corte_min
        self.tiempo_corte_max = tiempo_corte_max
        self.t_llegadas = t_llegadas
        self.tot_clientes = tot_clientes
        self.te = 0.0  # tiempo de espera total
        self.dt = 0.0  # duración total del servicio
        self.fin = 0.0  # minuto en que finaliza
        random.seed(self.semilla)  # Inicializar la semilla para la simulación
        self.env = simpy.Environment()  # Crear el entorno de simulación
        self.personal = simpy.Resource(self.env, self.num_peluqueros)  # Crear los recursos (peluqueros)

    def cortar(self, cliente):
        """Simula el proceso de corte de cabello"""
        R = random.random()
        tiempo = self.tiempo_corte_max - self.tiempo_corte_min
        tiempo_corte = self.tiempo_corte_min + (tiempo * R)  # Dist Uniforme
        yield self.env.timeout(tiempo_corte)  # Simula el tiempo que toma el corte
        print(f"Corte listo para {cliente} en {tiempo_corte:.2f} minutos")
        self.dt += tiempo_corte  # Acumular tiempo de uso de la instalación

    def cliente(self, name):
        """Simula la llegada y servicio de un cliente"""
        llega = self.env.now  # Guarda el minuto de llegada del cliente
        print(f"--> {name} llegó a la peluquería en el minuto {llega:.2f}")
        with self.personal.request() as request:  # Espera turno
            yield request  # Obtener turno
            pasa = self.env.now
            espera = pasa - llega  # Calcula el tiempo de espera
            self.te += espera  # Acumula el tiempo de espera
            print(f"{name} pasa y espera en la peluquería en el minuto {pasa:.2f}, habiendo esperado {espera:.2f}")
            yield self.env.process(self.cortar(name))  # Llama al proceso de corte
            deja = self.env.now  # Momento en que el cliente deja la peluquería
            print(f"<-- {name} deja la peluquería en el minuto {deja:.2f}")
            self.fin = deja  # Guarda el minuto en que termina

    def principal(self):
        """Simula la llegada de los clientes en intervalos aleatorios"""
        llegada = 0
        for i in range(1, self.tot_clientes + 1):
            R = random.random()
            llegada = -self.t_llegadas * math.log(R)
            yield self.env.timeout(llegada)  # Dejar transcurrir un tiempo entre un cliente y otro
            self.env.process(self.cliente(f'cliente {i}'))  # Procesar al cliente

    def run(self):
        """Inicia la simulación"""
        print("---Simulación Peluquería---")
        self.env.process(self.principal())  # Inicia el proceso principal
        self.env.run()  # Ejecuta la simulación

    def mostrar_resultados(self):
        """Calcula y muestra los resultados de la simulación"""
        print("Indicadores obtenidos:")
        lpc = self.te / self.fin  # Longitud promedio de la cola
        tep = self.te / self.tot_clientes  # Tiempo de espera promedio
        upi = (self.dt / self.fin) / self.num_peluqueros  # Uso promedio de la instalación
        print(f"Longitud promedio de la cola: {lpc:.2f}")
        print(f"Tiempo de espera promedio: {tep:.2f}")
        print(f"Uso promedio de la instalación: {upi:.2f}")


# Entrada de parámetros
semilla = int(input("Ingrese la semilla (int): "))
num_peluqueros = int(input("Ingrese el número de peluqueros (int): "))
tiempo_corte_min = float(input("Ingrese el tiempo de corte mínimo: "))
tiempo_corte_max = float(input("Ingrese el tiempo de corte máximo: "))
t_llegadas = float(input("Ingrese el tiempo de llegadas: "))
tot_clientes = int(input("Ingrese el total de clientes (int): "))

# Crear una instancia de la simulación
simulacion = PeluqueriaSimulacion(semilla, num_peluqueros, tiempo_corte_min, tiempo_corte_max, t_llegadas, tot_clientes)

# Ejecutar la simulación
simulacion.run()

# Mostrar los resultados
simulacion.mostrar_resultados()