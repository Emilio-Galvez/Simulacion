# Importa la clase que almacena las métricas calculadas del sistema.
from modelo.metricas import Metricas


# Calcula el promedio aritmético de los valores de una lista.
def promedio(lista):

    # Si la lista está vacía, devuelve 0 para evitar una división entre cero.
    if len(lista) == 0:
        return 0

    # Suma los valores de la lista y divide el resultado para su cantidad.
    return sum(lista) / len(lista)


# Calcula el promedio temporal de una variable dentro de un intervalo.
# Se utiliza para calcular el número promedio de clientes en el sistema,
# el número promedio en cola y la utilización del servidor.
def promedio_en_el_tiempo(tiempos, valores, inicio, fin):

    # Acumula el área bajo la curva de los valores registrados.
    area = 0

    # Recorre los instantes en los que se registraron los estados.
    for i in range(len(tiempos)):

        # Obtiene el instante inicial del intervalo actual.
        desde = tiempos[i]

        # Si existe un siguiente estado, utiliza su tiempo como límite.
        # El valor actual se mantiene hasta que ocurre el siguiente cambio.
        if i + 1 < len(tiempos):
            hasta = tiempos[i + 1]
        else:
            # Para el último estado, utiliza el final del intervalo analizado.
            hasta = fin

        # Ajusta el inicio para no considerar tiempos anteriores
        # al período de análisis.
        if desde < inicio:
            desde = inicio

        # Evita considerar tiempos posteriores al final del análisis.
        if hasta > fin:
            hasta = fin

        # Si el intervalo tiene duración positiva, calcula su área.
        # Multiplica el tiempo transcurrido por el valor registrado.
        if hasta > desde:
            area = area + (hasta - desde) * valores[i]

    # Divide el área acumulada para la duración del intervalo.
    # Así obtiene el promedio temporal de la variable.
    return area / (fin - inicio)


# Calcula las métricas obtenidas mediante la simulación.
# Recibe los clientes, los estados registrados, el tiempo de calentamiento
# y el instante final del período de análisis.
def calcular_simuladas(clientes, estados, calentamiento, fin):

    # Listas que almacenan los tiempos de espera y de permanencia
    # de los clientes que cumplen las condiciones del análisis.
    esperas = []
    tiempos_en_sistema = []

    # Recorre todos los clientes registrados en la simulación.
    for cliente in clientes:

        # Ignora a los clientes que llegaron antes del calentamiento.
        # De esta manera, no se incluyen en los promedios individuales.
        if cliente.llegada < calentamiento:
            continue

        # Si el cliente comenzó su servicio, registra su tiempo de espera.
        if cliente.inicio_servicio is not None:
            esperas.append(cliente.tiempo_espera())

        # Si el cliente salió del sistema, registra su tiempo total
        # de permanencia, desde su llegada hasta su salida.
        if cliente.salida is not None:
            tiempos_en_sistema.append(cliente.tiempo_en_sistema())

    # Listas para almacenar los tiempos y los valores de cada estado.
    tiempos = []
    en_cola = []
    en_sistema = []
    servidor_ocupado = []

    # Recorre los estados registrados durante la simulación.
    for estado in estados:

        # Guarda el instante en que se registró el estado.
        tiempos.append(estado.tiempo)

        # Guarda la cantidad de clientes que esperan en la cola.
        en_cola.append(estado.en_cola)

        # Guarda la cantidad total de clientes en el sistema.
        en_sistema.append(estado.en_sistema)

        # Si hay clientes en el sistema, se considera ocupado el servidor.
        # Esto se aplica porque el modelo tiene un único servidor.
        if estado.en_sistema > 0:
            servidor_ocupado.append(1)
        else:
            # Si el sistema está vacío, el servidor está desocupado.
            servidor_ocupado.append(0)

    # Calcula la utilización promedio del servidor (rho),
    # es decir, la proporción del tiempo en que permanece ocupado.
    rho = promedio_en_el_tiempo(
        tiempos, servidor_ocupado, calentamiento, fin
    )

    # Calcula el número promedio de clientes presentes en el sistema (L).
    L = promedio_en_el_tiempo(
        tiempos, en_sistema, calentamiento, fin
    )

    # Calcula el número promedio de clientes que esperan en la cola (Lq).
    Lq = promedio_en_el_tiempo(
        tiempos, en_cola, calentamiento, fin
    )

    # Calcula el tiempo promedio de permanencia en el sistema (W),
    # utilizando los clientes que ya salieron y cumplen las condiciones.
    W = promedio(tiempos_en_sistema)

    # Calcula el tiempo promedio de espera antes de iniciar el servicio (Wq).
    Wq = promedio(esperas)

    # Crea un objeto Metricas con los cinco indicadores calculados.
    return Metricas(rho, L, Lq, W, Wq)


# Calcula el error relativo porcentual entre el valor teórico
# y el valor obtenido mediante la simulación.
def error_relativo(teorico, simulado):

    # Si el valor teórico es cero, devuelve 0 para evitar una división
    # entre cero.
    if teorico == 0:
        return 0

    # Calcula la diferencia absoluta entre ambos valores,
    # la divide para el valor teórico y la multiplica por 100.
    return abs(simulado - teorico) / teorico * 100