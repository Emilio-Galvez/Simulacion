# Importa la clase ControladorMM1, encargada de coordinar
# la ejecución de los escenarios y los procesos de la simulación.
from controlador.controlador import ControladorMM1


# Define los escenarios que se utilizarán para evaluar el sistema de colas.
# Cada escenario establece una tasa de llegada (lam), una tasa de servicio
# (mu) y una descripción de la condición del sistema.
ESCENARIOS = [
    # Escenario 1: el sistema trabaja en condiciones estables.
    {"lam": 2.0, "mu": 3.0, "condicion": "Sistema estable"},

    # Escenario 2: aumenta la tasa de llegada y el servidor tiene
    # una mayor utilización.
    {"lam": 2.5, "mu": 3.0, "condicion": "Mayor utilización"},

    # Escenario 3: la tasa de llegada se aproxima a la tasa de servicio,
    # por lo que el sistema se encuentra cerca de la saturación.
    {"lam": 2.9, "mu": 3.0, "condicion": "Cerca de saturación"},
]


# Establece la duración total de cada simulación.
# El sistema dejará de procesar eventos cuando alcance este tiempo.
TIEMPO_SIMULACION = 20_000

# Define el tiempo inicial de calentamiento que se excluirá
# de determinados cálculos estadísticos para reducir la influencia
# de las condiciones iniciales del sistema.
TIEMPO_CALENTAMIENTO = 500

# Establece la semilla del generador de números pseudoaleatorios.
# Permite reproducir la misma secuencia aleatoria cuando se mantienen
# las mismas condiciones y el mismo orden de ejecución.
SEMILLA = 42


# Define hasta qué minuto se representará la simulación animada.
MINUTOS_ANIMADOS = 120

# Establece el intervalo de tiempo simulado entre los pasos de la animación.
MINUTOS_POR_PASO = 1

# Define la duración en segundos de cada paso de la animación.
SEGUNDOS_POR_PASO = 0.15

# Establece la pausa en segundos entre la presentación de escenarios.
SEGUNDOS_ENTRE_ESCENARIOS = 2

# Define la altura utilizada para representar la gráfica,
# según cómo se aplique este parámetro en la interfaz.
ALTO_GRAFICA = 10

# Establece la cantidad de clientes que se mostrarán en la interfaz,
# según la implementación de la vista.
# No establece por sí mismo el límite de clientes que puede crear
# la simulación.
CLIENTES_VISIBLES = 10


# Define el nombre de la carpeta donde se almacenarán las gráficas.
CARPETA_GRAFICAS = "graficas"

# Establece la ventana temporal utilizada para representar
# la evolución de la cola en una gráfica, según su implementación.
VENTANA_GRAFICA_COLA = 200


# Agrupa todos los parámetros anteriores en un diccionario.
# Así, el controlador puede recibir la configuración completa
# mediante un solo argumento.
CONFIGURACION = {
    "ESCENARIOS": ESCENARIOS,
    "TIEMPO_SIMULACION": TIEMPO_SIMULACION,
    "TIEMPO_CALENTAMIENTO": TIEMPO_CALENTAMIENTO,
    "SEMILLA": SEMILLA,
    "MINUTOS_ANIMADOS": MINUTOS_ANIMADOS,
    "MINUTOS_POR_PASO": MINUTOS_POR_PASO,
    "SEGUNDOS_POR_PASO": SEGUNDOS_POR_PASO,
    "SEGUNDOS_ENTRE_ESCENARIOS": SEGUNDOS_ENTRE_ESCENARIOS,
    "ALTO_GRAFICA": ALTO_GRAFICA,
    "CLIENTES_VISIBLES": CLIENTES_VISIBLES,
    "CARPETA_GRAFICAS": CARPETA_GRAFICAS,
    "VENTANA_GRAFICA_COLA": VENTANA_GRAFICA_COLA,
}


# Comprueba si este archivo se está ejecutando directamente.
# Si es así, crea el controlador con la configuración definida
# y llama a su método ejecutar() para iniciar el proceso.
if __name__ == "__main__":
    ControladorMM1(CONFIGURACION).ejecutar()