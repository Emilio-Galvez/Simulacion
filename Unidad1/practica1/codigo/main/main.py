import numpy as np
import matplotlib.pyplot as plt

from datos.datos_climaticos import datos
from simulador.modelo_ajustado import ModeloAjustado
from simulador.modelo_inicial import ModeloInicial
from simulador.simulador import Simulador


def clasificar_indice(indice):

    if indice < 0.40:
        return "Sin lluvia"

    elif indice < 0.60:
        return "Baja posibilidad"

    elif indice < 0.75:
        return "Lluvia probable"

    else:
        return "Lluvia"


# Creamos el modelo
modelo = ModeloInicial()

# Creamos el simulador y le pasamos el modelo
simulador = Simulador(modelo)


# Guardamos los datos en listas

horas = []
humedades = []
nubosidades = []
temperaturas = []
indices = []
resultados = []
factores_temperatura = []

for dato in datos:

    indice = simulador.ejecutar(dato)

    resultado = clasificar_indice(indice)

    # Obtenemos el factor de temperatura
    tf = simulador.modelo.factor_temperatura.obtener_factor(
        dato.temperatura
    )

    horas.append(dato.hora)
    humedades.append(dato.humedad)
    nubosidades.append(dato.nubosidad)
    temperaturas.append(dato.temperatura)
    factores_temperatura.append(tf)

    indices.append(indice)
    resultados.append(resultado)


# Convertimos las listas numéricas en arrays de NumPy

horas = np.array(horas)
humedades = np.array(humedades)
nubosidades = np.array(nubosidades)
temperaturas = np.array(temperaturas)
factores_temperatura = np.array(factores_temperatura)
indices = np.array(indices)
    

# TABLA DE RESULTADOS

print("\nTABLA DE RESULTADOS")
print("-" * 75)

print(
    f"{'Hora':<8} "
    f"{'Humedad':<10} "
    f"{'Nubosidad':<12} "
    f"{'Temp':<8} "
    f"{'Tf':<8} "
    f"{'Índice':<10} "
    f"{'Resultado'}"
)

print("-" * 75)

for i in range(len(horas)):

    print(
        f"{horas[i]:<8} "
        f"{humedades[i]:<10} "
        f"{nubosidades[i]:<12} "
        f"{temperaturas[i]:<8} "
        f"{factores_temperatura[i]:<8.2f} "
        f"{indices[i]:<10.3f} "
        f"{resultados[i]}"
    )


# PRIMERA GRÁFICA: ÍNDICE DE LLUVIA

plt.figure()

plt.plot(horas, indices, marker="o")

plt.xlabel("Hora")
plt.ylabel("Índice de lluvia")
plt.title("Índice de lluvia durante el día")

plt.grid(True)

plt.show(block=False)


# SEGUNDA GRÁFICA: HUMEDAD Y NUBOSIDAD

plt.figure()

plt.plot(horas, humedades, marker="o", label="Humedad")
plt.plot(horas, nubosidades, marker="o", label="Nubosidad")

plt.xlabel("Hora")
plt.ylabel("Porcentaje (%)")
plt.title("Humedad y nubosidad durante el día")

plt.legend()
plt.grid(True)

plt.show(block=False)


# TERCERA GRÁFICA: TEMPERATURA Y FACTOR Tf

fig, ax1 = plt.subplots()

ax1.plot(
    horas,
    temperaturas,
    marker="o",
    color="red",
    label="Temperatura"
)

ax1.set_xlabel("Hora")
ax1.set_ylabel("Temperatura (°C)")
ax1.set_title("Temperatura y factor de temperatura")

ax2 = ax1.twinx()

ax2.plot(
    horas,
    factores_temperatura,
    marker="o",
    color="purple",
    label="Factor Tf"
)

ax2.set_ylabel("Factor Tf")

ax1.grid(True)

fig.legend(
    ["Temperatura", "Factor Tf"],
    loc="upper center",
    bbox_to_anchor=(0.5, 1.02),
    ncol=2
)

plt.show(block=False)


# Mantener las tres ventanas abiertas

plt.show()