import numpy as np
import simpy

from modelo.cliente import Cliente
from modelo.estado import Estado
from modelo.foto import Foto


# Clase encargada de ejecutar la simulación del sistema de colas M/M/1.
class SimuladorMM1:

    # Inicializa el simulador con los parámetros de un escenario
    # y una semilla para controlar la generación de números aleatorios.
    def __init__(self, escenario, semilla):

        # Obtiene los parámetros del escenario.
        self.lam = escenario.lam  # Tasa promedio de llegada de clientes (lambda).
        self.mu = escenario.mu  # Tasa promedio de servicio (mu).
        self.tiempo_simulacion = escenario.tiempo  # Duración total de la simulación.

        # Generador de números aleatorios para las llegadas y los servicios.
        self.aleatorio = np.random.default_rng(semilla)

        # Crea el entorno que administra el tiempo y los eventos de SimPy.
        self.entorno = simpy.Environment()

        # Crea un servidor con capacidad para atender a un solo cliente a la vez.
        self.servidor = simpy.Resource(self.entorno, capacity=1)

        # Lista que almacena los clientes que llegan al sistema.
        self.clientes = []

        # Guarda el estado inicial del sistema:
        # tiempo 0, cero clientes en cola y cero clientes en el sistema.
        self.estados = [Estado(0, 0, 0)]

        # Lista de clientes que esperan para ser atendidos.
        self.cola = []

        # Almacena el cliente que está siendo atendido.
        # None indica que no hay un cliente registrado en servicio.
        self.en_servicio = None

        # Número total de clientes que están esperando o siendo atendidos.
        self.en_sistema = 0

        # Lista que almacena las capturas periódicas del sistema.
        self.fotos = []

        # Acumula los tiempos de espera de los clientes que comienzan su servicio.
        self.suma_esperas = 0

        # Cuenta los clientes que han comenzado su servicio.
        self.atendidos = 0

    # Registra el estado actual del sistema en un instante determinado.
    def registrar_estado(self):

        # Crea un registro con el tiempo actual, los clientes en cola
        # y el número total de clientes presentes en el sistema.
        estado = Estado(
            self.entorno.now,
            len(self.cola),
            self.en_sistema
        )

        # Agrega el estado registrado a la lista de estados.
        self.estados.append(estado)

    # Genera las llegadas de clientes mediante un proceso de Poisson,
    # utilizando tiempos entre llegadas con distribución exponencial.
    def generar_clientes(self):

        # Contador utilizado para asignar un número a cada cliente.
        numero = 0

        # Continúa generando llegadas hasta que finalice la simulación.
        while True:

            # Genera el tiempo entre llegadas consecutivas.
            # La media de este tiempo es 1/lambda.
            tiempo_entre_llegadas = self.aleatorio.exponential(1 / self.lam)

            # Avanza el tiempo simulado hasta la siguiente llegada.
            yield self.entorno.timeout(tiempo_entre_llegadas)

            # Incrementa el contador y crea el nuevo cliente
            # registrando su número y su instante de llegada.
            numero = numero + 1
            cliente = Cliente(numero, self.entorno.now)

            # Guarda el cliente en la lista general de clientes.
            self.clientes.append(cliente)

            # Inicia el proceso que administra la espera y atención del cliente.
            self.entorno.process(self.atender_cliente(cliente))

    # Administra el ingreso a la cola, la espera, el servicio y la salida
    # de un cliente del sistema.
    def atender_cliente(self, cliente):

        # Incorpora al cliente a la cola de espera.
        self.cola.append(cliente)

        # Incrementa el número de clientes presentes en el sistema.
        self.en_sistema = self.en_sistema + 1

        # El cliente solicita utilizar el servidor.
        turno = self.servidor.request()

        # Registra el estado del sistema después de la llegada del cliente.
        self.registrar_estado()

        # Espera hasta que SimPy conceda el uso del servidor.
        # Si está ocupado, el cliente permanece esperando.
        yield turno

        # Cuando obtiene el servidor, el cliente sale de la cola de espera.
        self.cola.remove(cliente)

        # Registra al cliente como el que está siendo atendido.
        self.en_servicio = cliente

        # Guarda el instante en que comienza el servicio.
        cliente.inicio_servicio = self.entorno.now

        # Calcula el tiempo de espera del cliente y lo acumula.
        # El cálculo depende de la implementación de tiempo_espera()
        # en la clase Cliente.
        self.suma_esperas = self.suma_esperas + cliente.tiempo_espera()

        # Incrementa el contador de clientes que han comenzado su servicio.
        self.atendidos = self.atendidos + 1

        # Registra el estado del sistema al comenzar la atención.
        self.registrar_estado()

        # Genera el tiempo de servicio mediante una distribución exponencial.
        # La media del tiempo de servicio es 1/mu.
        tiempo_servicio = self.aleatorio.exponential(1 / self.mu)

        # Avanza el tiempo simulado hasta que finaliza la atención.
        yield self.entorno.timeout(tiempo_servicio)

        # Libera el servidor para que pueda atender a otro cliente.
        self.servidor.release(turno)

        # Indica que ya no hay un cliente registrado en servicio.
        self.en_servicio = None

        # Registra el instante en que el cliente abandona el sistema.
        cliente.salida = self.entorno.now

        # Reduce el número de clientes presentes en el sistema.
        self.en_sistema = self.en_sistema - 1

        # Registra el estado del sistema después de la salida del cliente.
        self.registrar_estado()

    # Toma capturas periódicas del sistema para observar su evolución.
    def tomar_fotos(self, duracion, paso):

        # Repite el proceso mientras el tiempo actual no supere la duración
        # establecida para las capturas.
        while self.entorno.now <= duracion:

            # Lista donde se almacenan los números de los clientes en espera.
            numeros_en_cola = []

            # Recorre la cola para obtener el identificador de cada cliente.
            for cliente in self.cola:
                numeros_en_cola.append(cliente.numero)

            # Inicialmente se considera que no hay ningún cliente en servicio.
            en_servicio = 0

            # Si existe un cliente en servicio, guarda su número.
            if self.en_servicio is not None:
                en_servicio = self.en_servicio.numero

            # Inicializa el tiempo promedio de espera.
            espera_promedio = 0

            # Si hay clientes que han comenzado su servicio,
            # calcula su tiempo de espera promedio acumulado.
            if self.atendidos > 0:
                espera_promedio = self.suma_esperas / self.atendidos

            # Crea y almacena una captura con el tiempo actual,
            # el cliente en servicio, la cola y la espera promedio.
            self.fotos.append(
                Foto(
                    self.entorno.now,
                    en_servicio,
                    numeros_en_cola,
                    espera_promedio
                )
            )

            # Espera el intervalo indicado antes de tomar otra captura.
            yield self.entorno.timeout(paso)

    # Inicia y ejecuta todos los procesos necesarios para la simulación.
    def ejecutar(self, duracion_fotos, paso_fotos):

        # Inicia el proceso que genera las llegadas de clientes.
        self.entorno.process(self.generar_clientes())

        # Inicia el proceso que toma capturas periódicas del sistema.
        self.entorno.process(
            self.tomar_fotos(duracion_fotos, paso_fotos)
        )

        # Ejecuta los eventos hasta alcanzar el tiempo total de simulación.
        self.entorno.run(until=self.tiempo_simulacion)