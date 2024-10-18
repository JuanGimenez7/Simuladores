import simpy
import random

class SimulacionServidor:
    def __init__(self, semilla, capacidad_servidor, capacidad_cola, tiempo_proc_min, tiempo_proc_max, tiempo_llegadas, total_paquetes):
        self.semilla = semilla
        self.capacidad_servidor = capacidad_servidor
        self.capacidad_cola = capacidad_cola
        self.tiempo_proc_min = tiempo_proc_min
        self.tiempo_proc_max = tiempo_proc_max
        self.tiempo_llegadas = tiempo_llegadas
        self.total_paquetes = total_paquetes
        self.paquetes_perdidos = 0
        self.tiempo_total_espera = 0
        self.paquetes_procesados = 0

        # Configura el entorno y el servidor
        random.seed(self.semilla)
        self.env = simpy.Environment()
        self.servidor = simpy.Resource(self.env, self.capacidad_servidor)

    def procesar_paquete(self, nombre):
        """Simula el procesamiento de un paquete"""
        llegada = self.env.now
        print(f'{nombre} llega al servidor en el segundo {llegada:.2f}')

        with self.servidor.request() as req:
            # Si la cola está llena, el paquete se pierde
            if len(self.servidor.queue) >= self.capacidad_cola:
                self.paquetes_perdidos += 1
                print(f'{nombre} se pierde debido a cola llena en el segundo {self.env.now:.2f}')
                return

            # El paquete espera su turno y se procesa
            yield req
            espera = self.env.now - llegada
            self.tiempo_total_espera += espera
            print(f'{nombre} comienza a ser procesado después de esperar {espera:.2f} segundos en el segundo {self.env.now:.2f}')

            # Simula el procesamiento del paquete
            tiempo_procesamiento = random.randint(self.tiempo_proc_min, self.tiempo_proc_max)
            yield self.env.timeout(tiempo_procesamiento)
            print(f'{nombre} termina de ser procesado en el segundo {self.env.now:.2f}')
            self.paquetes_procesados += 1

    def generar_paquetes(self):
        """Genera los paquetes que llegan al servidor"""
        for i in range(self.total_paquetes):
            yield self.env.timeout(random.expovariate(1.0 / self.tiempo_llegadas))
            self.env.process(self.procesar_paquete(f'Paquete {i+1}'))

    def ejecutar_simulacion(self):
        """Inicia la simulación"""
        print('--- Simulación de Red de Computadoras ---')
        self.env.process(self.generar_paquetes())
        self.env.run()
        print('--- Fin de la simulación ---')

        # Resultados de la simulación
        self.mostrar_resultados()

    def mostrar_resultados(self):
        """Muestra los resultados de la simulación"""
        print("\nResultados de la simulación:")
        print(f'Total de paquetes simulados: {self.total_paquetes}')
        print(f'Paquetes procesados: {self.paquetes_procesados}')
        print(f'Paquetes perdidos: {self.paquetes_perdidos}')
        tasa_perdida = 100 * self.paquetes_perdidos / self.total_paquetes
        print(f'Tasa de pérdida de paquetes: {tasa_perdida:.2f}%')
        tiempo_promedio_espera = self.tiempo_total_espera / self.paquetes_procesados if self.paquetes_procesados > 0 else 0
        print(f'Tiempo promedio de espera de los paquetes: {tiempo_promedio_espera:.2f} segundos')
        utilizacion_servidor = 100 * (self.paquetes_procesados * (self.tiempo_proc_min + self.tiempo_proc_max) / 2) / self.env.now
        print(f'Utilización del servidor: {utilizacion_servidor:.2f}%')


# Solicitar parámetros al usuario
semilla = int(input("Ingrese la semilla: "))
capacidad_servidor = int(input("Ingrese la capacidad del servidor (número de paquetes que puede procesar simultáneamente): "))
capacidad_cola = int(input("Ingrese la capacidad de la cola de espera: "))
tiempo_proc_min = float(input("Ingrese el tiempo mínimo de procesamiento de un paquete (en segundos): "))
tiempo_proc_max = float(input("Ingrese el tiempo máximo de procesamiento de un paquete (en segundos): "))
tiempo_llegadas = float(input("Ingrese el tiempo promedio entre llegadas de paquetes (en segundos): "))
total_paquetes = int(input("Ingrese el número total de paquetes a simular: "))

# Crear instancia de la simulación
simulacion = SimulacionServidor(semilla, capacidad_servidor, capacidad_cola, tiempo_proc_min, tiempo_proc_max, tiempo_llegadas, total_paquetes)

# Ejecutar la simulación
simulacion.ejecutar_simulacion()