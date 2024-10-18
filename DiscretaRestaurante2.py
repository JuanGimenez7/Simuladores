import simpy
import random

class RestauranteSimulacion:
    def __init__(self, semilla, num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes):
        self.semilla = semilla  # Semilla para reproducibilidad
        self.num_mesas = num_mesas  # Número de mesas disponibles en el restaurante
        self.tiempo_comer_min = tiempo_comer_min  # Tiempo mínimo que un cliente pasa comiendo
        self.tiempo_comer_max = tiempo_comer_max  # Tiempo máximo que un cliente pasa comiendo
        self.tiempo_llegadas = tiempo_llegadas  # Tiempo promedio entre la llegada de clientes
        self.total_clientes = total_clientes  # Total de clientes a simular
        random.seed(self.semilla)  # Establece la semilla para reproducir resultados
        self.env = simpy.Environment()  # Crea el entorno de simulación
        self.restaurante = simpy.Resource(self.env, self.num_mesas)  # Crea el recurso de mesas en el restaurante

    def cliente(self, nombre):
        """Simula el proceso de un cliente que llega, espera una mesa, come y luego se va."""
        print(f'{nombre} llega al restaurante en el minuto {self.env.now:.2f}')

        # El cliente solicita una mesa en el restaurante (espera si no hay mesas disponibles)
        with self.restaurante.request() as mesa:
            yield mesa  # Espera a que una mesa esté disponible
            print(f'{nombre} toma una mesa en el minuto {self.env.now:.2f}')

            # Simula el tiempo que el cliente pasa comiendo
            tiempo_comer = random.randint(self.tiempo_comer_min, self.tiempo_comer_max)
            yield self.env.timeout(tiempo_comer)
            print(f'{nombre} termina de comer y deja la mesa en el minuto {self.env.now:.2f}')

    def llegada_clientes(self):
        """Genera la llegada de clientes al restaurante."""
        for i in range(self.total_clientes):
            # Cada cliente llega al restaurante
            yield self.env.timeout(random.expovariate(1.0 / self.tiempo_llegadas))  # Distribución exponencial para el tiempo entre llegadas
            self.env.process(self.cliente(f'Cliente {i+1}'))

    def ejecutar(self):
        """Configura y ejecuta la simulación."""
        print('--- Simulación del Restaurante ---')
        self.env.process(self.llegada_clientes())  # Inicia el proceso de llegada de clientes
        self.env.run()  # Ejecuta la simulación
        print('--- Fin de la simulación ---')



# Pedir al usuario los parámetros del sistema
semilla = int(input("Ingrese la semilla (int): "))
num_mesas = int(input("Ingrese el número de mesas disponibles en el restaurante: "))
tiempo_comer_min = float(input("Ingrese el tiempo mínimo que un cliente pasa comiendo (minutos): "))
tiempo_comer_max = float(input("Ingrese el tiempo máximo que un cliente pasa comiendo (minutos): "))
tiempo_llegadas = float(input("Ingrese el tiempo promedio entre la llegada de clientes (minutos): "))
total_clientes = int(input("Ingrese el total de clientes a simular: "))

# Crear una instancia de la simulación del restaurante
restaurante_sim = RestauranteSimulacion(semilla, num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes)

# Ejecutar la simulación
restaurante_sim.ejecutar()