import queue
import threading

from controlador.estadisticas import calcular_simuladas
from controlador.simulador import SimuladorMM1
from controlador.teoria import calcular_teoricas
from modelo.escenario import Escenario
from modelo.resultado import Resultado
from vista import consola, graficas


class ControladorMM1: # Esta clase organiza simulador.py y ejecuta teoria.py y estadisticas.py
                                # Controaldor reune los resultados
    def __init__(self, config):  # Recibe la configuracion al crearse y prepara los objetos de tipo escenario
        if config["TIEMPO_CALENTAMIENTO"] >= config["TIEMPO_SIMULACION"]:
            raise ValueError("El calentamiento debe ser menor que el tiempo de simulación")
        self.config = config
        self.escenarios = []
        self.resultados = []

        numero = 1
        for datos in config["ESCENARIOS"]:
            escenario = Escenario(numero, datos["lam"], datos["mu"], config["TIEMPO_SIMULACION"], datos["condicion"])
            self.escenarios.append(escenario)
            numero = numero + 1

    
    def ejecutar(self): # Empieza el proceso y cuando hay resultados se los entrega a la vista
        resultados_listos = queue.Queue()
        hilo_simulacion = threading.Thread(target=self.simular_todos, args=(resultados_listos,), daemon=True)
        hilo_simulacion.start()

        for escenario in self.escenarios:
            resultado = resultados_listos.get()
            self.resultados.append(resultado)
            consola.animar(resultado, len(self.escenarios), self.config)
            consola.mostrar_resultados(resultado)
            if resultado.fue_simulado():
                consola.mostrar_archivo(graficas.guardar_escenario(resultado, self.config))
            consola.esperar(self.config["SEGUNDOS_ENTRE_ESCENARIOS"])

        hilo_simulacion.join()
        consola.mostrar_comparacion(self.resultados)
        consola.mostrar_archivo(graficas.guardar_comparacion(self.resultados, self.config))

    def simular(self, escenario):
        resultado = Resultado(escenario)

        if not escenario.es_estable():
            resultado.mensaje = "El sistema no es estable: λ ≥ μ, la cola crece sin límite."
            return resultado # Comprueba si es estable

        simulador = SimuladorMM1(escenario, self.config["SEMILLA"]) # INicia al simualdor, al terminar reune sus datos y calcula als metricas
        simulador.ejecutar(self.config["MINUTOS_ANIMADOS"], self.config["MINUTOS_POR_PASO"])

        resultado.fotos = simulador.fotos
        resultado.clientes = simulador.clientes
        resultado.estados = simulador.estados
        resultado.teoricas = calcular_teoricas(escenario)
        resultado.simuladas = calcular_simuladas(
            simulador.clientes, simulador.estados, self.config["TIEMPO_CALENTAMIENTO"], escenario.tiempo
        )
        return resultado
    
    def simular_todos(self, resultados_listos): # Repite el trabajo con todos los escenarios configurados
        for escenario in self.escenarios: # Se recorre los escenarios almacenados en self.escenarios
            resultados_listos.put(self.simular(escenario)) # Agregamos elementos a al cola
