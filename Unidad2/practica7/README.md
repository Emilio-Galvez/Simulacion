# Práctica N.º 07 — Estimación de π mediante el método de Monte Carlo

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-17%2B-ED8B00?logo=openjdk&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.1-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11-eb6834)
![Pytest](https://img.shields.io/badge/Pytest-9.2-0A9EDC?logo=pytest)

**Práctica:** Estimación de resultados mediante el método de Monte Carlo  
**Asignatura:** Simulación — Ciclo 5, Carrera de Computación  
**Universidad:** Universidad Nacional de Loja — FEIRNNR  
**Estudiante:** Emilio Jose Galvez Merchan  
**Docente:** José O. Guamán Q.  
**Implementaciones:** Python 3.14 y Java 17+ (probado con OpenJDK 25)

---

## 1. Descripción

El experimento estima π con el método **Monte Carlo**. Para cada cantidad `N`
se generan `N` puntos uniformes en el cuadrado `[0, 1) × [0, 1)` y se cuentan
los que caen dentro del círculo unitario:

```text
x² + y² ≤ 1
```

Como el área del cuarto de círculo es `π/4`, la estimación es:

```text
π ≈ 4 · (Nc / N)
```

donde `Nc` es la cantidad de puntos dentro del círculo. El error absoluto se
calcula con el valor de referencia:

```text
Error = |π_real − π_estimado|,   π_real = 3.141592653589793
```

Tamaños de muestra solicitados por la guía:

- 1 000 puntos
- 10 000 puntos
- 100 000 puntos
- 1 000 000 de puntos

El proyecto contiene dos implementaciones independientes, una en Python y otra
en Java, con el mismo procedimiento y los mismos valores de `N`. Cada lenguaje
utiliza su **RNG nativo** con la misma semilla (`seed = 12345`). El procedimiento
es comparable, pero las secuencias no son idénticas porque Python usa Mersenne
Twister y Java usa el generador congruencial de `java.util.Random`.

Los resultados completos, la tabla comparativa y el análisis están en
[`documentation/informe.md`](documentation/informe.md).

---

## 2. Configuración

Los parámetros compartidos están en
[`config/simulation.properties`](config/simulation.properties):

| Parámetro | Valor | Descripción |
|---|---:|---|
| `seed` | 12 345 | Semilla del RNG nativo en ambos lenguajes |
| `sample.sizes` | 1000, 10000, 100000, 1000000 | Cantidades de puntos |
| `repetitions` | 5 | Repeticiones para calcular el tiempo mediano |
| `warmup.size` | 1 000 000 | Muestra de calentamiento no medida |
| `real.pi` | 3.141592653589793 | Valor de referencia de π |

Cada valor de `N` inicia un RNG nuevo con la misma semilla. Por tanto, la
muestra de `N = 10 000` contiene los primeros 1 000 puntos de `N = 1 000`, lo
que permite observar la convergencia al aumentar `N`.

---

## 3. Estructura del proyecto

```text
practica7/
├── config/
│   └── simulation.properties
├── python/
│   ├── src/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── models/results.py
│   │   ├── simulation/monte_carlo_pi.py
│   │   ├── services/
│   │   │   ├── simulation_service.py
│   │   │   ├── export_service.py
│   │   │   └── comparison_service.py
│   │   └── visualization/plots.py
│   └── tests/
│       ├── conftest.py
│       └── test_monte_carlo_pi.py
├── java/
│   └── src/main/java/simulation/
│       ├── Main.java
│       ├── config/Config.java
│       ├── models/Measurement.java
│       ├── models/Summary.java
│       ├── simulation/MonteCarloPi.java
│       └── services/
│           ├── SimulationService.java
│           └── CsvExporter.java
├── results/
│   ├── python/mediciones.csv
│   ├── python/resumen.csv
│   ├── java/mediciones.csv
│   ├── java/resumen.csv
│   ├── comparison/tabla_comparativa.csv
│   ├── comparison/tabla_solicitada.csv
│   └── plots/
├── documentation/informe.md
├── requirements.txt
└── README.md
```

---

## 4. Requisitos e instalación

- Python 3.10 o superior (probado con 3.14.4).
- Java 17 o superior (probado con OpenJDK 25.0.4.1).
- Dependencias de Python: `numpy`, `pandas`, `matplotlib` y `pytest`.

```bash
cd ~/simulacion
source venv/bin/activate
pip install -r Unidad2/practica7/requirements.txt
```

---

## 5. Ejecución

### 5.1 Python

```bash
cd ~/simulacion/Unidad2/practica7
python python/src/main.py --no-compare
```

Opciones disponibles:

```bash
python python/src/main.py --sizes 1000,10000
python python/src/main.py --repetitions 3
python python/src/main.py --no-warmup
python python/src/main.py --compare-only
python python/src/main.py --no-plots
```

### 5.2 Java

```bash
cd ~/simulacion/Unidad2/practica7/java
mkdir -p build/classes
javac -encoding UTF-8 -d build/classes $(find src/main/java -name "*.java")
java -cp build/classes simulation.Main
```

Para usar otro archivo de configuración:

```bash
java -cp build/classes simulation.Main ../config/simulation.properties
```

Para omitir el calentamiento:

```bash
java -cp build/classes simulation.Main --no-warmup
```

### 5.3 Comparación y gráficas

Después de ejecutar Python y Java:

```bash
cd ~/simulacion/Unidad2/practica7
python python/src/main.py --compare-only
```

Esto genera:

- `results/comparison/tabla_comparativa.csv`
- `results/comparison/tabla_solicitada.csv`
- `results/comparison/tabla_comparativa.md`
- `results/plots/error_vs_n.png`
- `results/plots/tiempos_vs_n.png`
- `results/plots/monte_carlo_1000.png`

### 5.4 Pruebas

```bash
cd ~/simulacion/Unidad2/practica7
python -m pytest -q python/tests
```

Resultado esperado: **6 pruebas aprobadas**.

---

## 6. Resultados obtenidos

Los tiempos son la mediana de 5 repeticiones y miden únicamente el ciclo Monte
Carlo (generación de puntos y conteo), sin incluir el arranque del intérprete,
el arranque de la JVM, la compilación ni la escritura de archivos.

### 6.1 Tabla solicitada por la guía

Se usa la estimación de Python como referencia para la columna «π estimado».
La estimación independiente de Java se muestra en la tabla 6.2.

| N | π estimado | Error | Tiempo Python (s) | Tiempo Java (s) |
|---:|---:|---:|---:|---:|
| 1 000 | 3.192000000000 | 5.040735e-02 | 0.000104 | 0.000015 |
| 10 000 | 3.139200000000 | 2.392654e-03 | 0.001011 | 0.000202 |
| 100 000 | 3.143640000000 | 2.047346e-03 | 0.009696 | 0.001777 |
| 1 000 000 | 3.139676000000 | 1.916654e-03 | 0.100435 | 0.014497 |

### 6.2 Estimaciones por lenguaje

| N | π Python | Error Python | π Java | Error Java |
|---:|---:|---:|---:|---:|
| 1 000 | 3.192000000000 | 5.040735e-02 | 3.204000000000 | 6.240735e-02 |
| 10 000 | 3.139200000000 | 2.392654e-03 | 3.156000000000 | 1.440735e-02 |
| 100 000 | 3.143640000000 | 2.047346e-03 | 3.139640000000 | 1.952654e-03 |
| 1 000 000 | 3.139676000000 | 1.916654e-03 | 3.141368000000 | 2.246536e-04 |

### 6.3 Tiempos

| N | Python (s) | Java (s) | Java / Python | Python / Java |
|---:|---:|---:|---:|---:|
| 1 000 | 0.000104 | 0.000015 | 0.145 | 6.88 |
| 10 000 | 0.001011 | 0.000202 | 0.200 | 5.01 |
| 100 000 | 0.009696 | 0.001777 | 0.183 | 5.46 |
| 1 000 000 | 0.100435 | 0.014497 | 0.144 | 6.93 |

---

## 7. Supuestos y ambigüedades

1. **Monte Carlo es obligatorio en la guía.** La guía de la Práctica 7
   especifica explícitamente el procedimiento `π ≈ 4·(Nc/N)`. Se implementó ese
   procedimiento después de la confirmación del usuario.
2. **RNG nativo con la misma semilla.** La guía espera que ambas
   implementaciones produzcan la misma secuencia con los mismos parámetros. En
   este proyecto se usó el RNG nativo de cada lenguaje, tal como se solicitó.
   Python (`random.Random`) y Java (`java.util.Random`) usan algoritmos
   distintos, por lo que las secuencias y las estimaciones no son idénticas.
   La comparación es válida en procedimiento, `N`, semilla y método de medición.
3. **Medición de tiempos.** Se mide solo el ciclo Monte Carlo. Se descartan el
   arranque de Python, el arranque de la JVM, la compilación, la exportación CSV
   y las gráficas. Se reporta la mediana de 5 repeticiones después de una
   muestra de calentamiento de 1 000 000 de puntos. Los tiempos dependen del
   equipo y no deben interpretarse como una propiedad universal de cada
   lenguaje.
4. **Muestras anidadas.** Para cada `N` se reinicia el RNG con la misma semilla.
   Por ello, `N = 10 000` contiene los primeros 1 000 puntos de `N = 1 000`.
   Esto es útil para estudiar convergencia, pero las muestras de distinto `N` no
   son independientes entre sí.
5. **`N` significa puntos, no números individuales.** Cada punto consume dos
   valores uniformes (`x`, `y`). La guía habla de «puntos» y así se interpretó.
6. **Error absoluto.** Se usa exactamente `|π_real − π_estimado|` con
   `π_real = 3.141592653589793`, según la instrucción del usuario.
7. **Referencia de la guía.** La sección de evaluación de la guía menciona
   «modelo M/M/1» por un error de copia; esa parte no corresponde al objetivo de
   esta práctica y no se implementó.
8. **Resultados reales.** Todos los valores de las tablas provienen de las
   ejecuciones registradas en `results/`; no se inventaron datos.

---

## 8. Documentación

- Informe completo: [`documentation/informe.md`](documentation/informe.md)
- Tabla comparativa: [`results/comparison/tabla_comparativa.csv`](results/comparison/tabla_comparativa.csv)
- Tabla solicitada: [`results/comparison/tabla_solicitada.csv`](results/comparison/tabla_solicitada.csv)
- Gráficas: [`results/plots/`](results/plots/)
