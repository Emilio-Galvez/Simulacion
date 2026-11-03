# Práctica N.º 02: Comparación de modelos determinísticos, estocásticos, discretos y continuos

**Práctica:** Comparación de modelos determinísticos, estocásticos, discretos y continuos
**Asignatura:** Simulación — Ciclo 5, Carrera de Computación
**Universidad:** Universidad Nacional de Loja
**Estudiante:** Emilio Jose Galvez Merchan
**Docente:** José O. Guamán Q.

## 1. Descripción del proyecto

Esta práctica compara cuatro paradigmas de simulación aplicados al mismo problema: el crecimiento poblacional. El objetivo es mostrar cómo cada paradigma representa el paso del tiempo y el azar, partiendo de una misma población inicial y una misma tasa de crecimiento.

Modelos implementados y sus fórmulas:

- **Determinístico:** $P(t) = P_0 \cdot e^{r \cdot t}$
- **Discreto:** $P(t+1) = P(t) + r \cdot P(t)$
- **Estocástico:** $P(t+1) = P(t) + r \cdot P(t) + \varepsilon$, con $\varepsilon \sim N(0, \sigma^2)$; si el resultado es negativo se establece en 0.
- **Continuo (Euler):** $P(t+\Delta t) = P(t) + \Delta t \cdot r \cdot P(t)$

Cada modelo calcula una lista de poblaciones en función del tiempo. Los resultados se presentan mediante el patrón Observer:

- `Subject` mantiene la lista de observadores y los notifica con los resultados.
- `Observer` define la interfaz `actualizar(resultados)`.
- `Tabla` y `Grafica` son observadores concretos que muestran los resultados en consola y en una gráfica, respectivamente.
- Los modelos solo calculan la serie de población; no saben cómo ni dónde se presentan los resultados.

## 2. Tecnologías utilizadas

- **Python 3.14.4** — lenguaje en el que está implementada toda la práctica.
- **numpy 2.5.3** — genera el ruido aleatorio con distribución normal en el modelo estocástico.
- **matplotlib 3.11.2** — dibuja la gráfica del crecimiento poblacional.
- **Entorno virtual (venv)** — aísla las dependencias del proyecto.
- **Linux / WSL** — sistema sobre el que se desarrolla y ejecuta.

## 3. Instalación

Requisito: Python 3.x instalado.

Comandos para crear el entorno virtual, activarlo e instalar las dependencias (Linux / WSL):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Uso

El punto de entrada es `main.py`, ubicado en `codigo/`. Para ejecutarlo:

```bash
cd codigo
python main.py
```

**Cambiar de modelo:** en `codigo/main.py` se asigna una instancia a la variable `modelo`, por ejemplo `modelo = ModeloDeterministico()`. Para probar otro paradigma basta con reemplazar esa instancia por `ModeloDiscreto()`, `ModeloEstocastico()` o `ModeloContinuo()`. No es necesario tocar los observadores.

**Configuración de parámetros:** los valores se definen en `codigo/datos/datos_poblacion.py`.

| Parámetro | Valor | Significado |
| --------- | ----- | ----------- |
| `P0` | 1000 | Población inicial |
| `r` | 0.1 | Tasa de crecimiento de la población |
| `sigma` | 20 | Desviación estándar del ruido (solo modelo estocástico) |
| `dt` | 0.1 | Tamaño del paso de tiempo (solo modelo continuo) |
| `tiempo` | 6 | Duración de la simulación |

**Salida esperada:**

- La consola muestra una tabla con dos columnas, `Tiempo` y `Población`, con un punto por cada instante simulado.
- Se abre una ventana de matplotlib con el título "Crecimiento de la población", eje X "Tiempo", eje Y "Población", una cuadrícula y puntos marcados sobre la línea.

Comportamiento por modelo:

- **Determinístico y discreto:** 7 puntos (tiempos 0 a 6). El determinístico crece de forma exponencial suave; el discreto crece de forma compuesta paso a paso.
- **Estocástico:** 7 puntos (tiempos 0 a 6). La serie cambia en cada ejecución porque incorpora ruido aleatorio normal.
- **Continuo:** 61 puntos, producto de dividir `tiempo / dt`. Refleja la integración numérica por el método de Euler.

**Notas:**

- El arreglo `datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]` presente en `datos_poblacion.py` se conserva solo como referencia de la guía y no entra en ningún cálculo; ningún modelo lo importa.
- El modelo continuo genera 61 muestras (pasos de 0.1). En la gráfica, el eje X se construye con `range(len(resultados))`, por lo que actualmente usa índices enteros de 0 a 60 y no el tiempo fraccionario.

## 5. Estructura del proyecto

```
practica2/
├── codigo/
│   ├── datos/
│   │   └── datos_poblacion.py   # Parámetros de la simulación (P0, r, sigma, dt, tiempo) y arreglo de referencia
│   ├── modelos/
│   │   ├── deterministico.py    # Modelo determinístico P(t) = P0 * e^(r*t)
│   │   ├── discreto.py          # Modelo discreto P(t+1) = P(t) + r*P(t)
│   │   ├── estocastico.py       # Modelo estocástico con ruido normal y límite inferior en 0
│   │   └── continuo.py          # Modelo continuo resuelto por Euler con paso dt
│   ├── observer/
│   │   ├── observer.py          # Interfaz Observer y clase Subject
│   │   ├── tabla.py             # Observador que imprime la tabla de resultados en consola
│   │   └── grafica.py           # Observador que dibuja la gráfica con matplotlib
│   └── main.py                  # Punto de entrada: crea el modelo, el subject y notifica a los observadores
├── requirements.txt             # Dependencias del proyecto con versiones fijadas
├── README.md                    # Este documento
└── Practica_2_Simulacion.pdf    # Enunciado de la práctica
```
