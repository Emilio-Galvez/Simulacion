from modelo.metricas import Metricas


# Calcula las métricas teóricas de un sistema de colas M/M/1.
# Recibe un escenario con las tasas de llegada y de servicio.
def calcular_teoricas(escenario):

    # Obtiene la tasa promedio de llegada de clientes (lambda).
    lam = escenario.lam

    # Obtiene la tasa promedio de servicio del servidor (mu).
    mu = escenario.mu

    # Calcula la utilización del servidor (rho).
    # Representa la proporción del tiempo que el servidor permanece ocupado.
    rho = lam / mu

    # Calcula el número promedio de clientes en todo el sistema (L).
    # Incluye tanto a los clientes que esperan como al que está en servicio.
    L = lam / (mu - lam)

    # Calcula el número promedio de clientes que esperan en la cola (Lq).
    # No incluye al cliente que está siendo atendido.
    Lq = (lam ** 2) / (mu * (mu - lam))

    # Calcula el tiempo promedio que un cliente permanece en el sistema (W).
    # Incluye el tiempo de espera y el tiempo de servicio.
    W = 1 / (mu - lam)

    # Calcula el tiempo promedio que un cliente espera antes de ser atendido (Wq).
    Wq = lam / (mu * (mu - lam))

    # Crea y devuelve un objeto Metricas con los cinco indicadores teóricos.
    return Metricas(rho, L, Lq, W, Wq)