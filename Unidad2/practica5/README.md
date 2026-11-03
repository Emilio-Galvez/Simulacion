# Practica 5 — Generador Congruencial Lineal (LCG) en Python y Java

Implementación y análisis del **Generador Congruencial Lineal** con la recurrencia

```
X(n+1) = (a * X(n) + c) mod m          U(n) = X(n) / m
```

| Parámetro | Valor |
|-----------|-------|
| Multiplicador `a` | 1 664 525 |
| Incremento `c` | 1 013 904 223 |
| Módulo `m` | 2^32 = 4 294 967 296 |
| Semilla inicial `X(0)` | 12 345 |
| Cantidad de números | 10 000 |

El proyecto está desarrollado en **Python** y en **Java**, con una arquitectura en
capas de tres niveles y los patrones **Strategy** y **Factory Method**. Ambas
implementaciones son programas independientes que intercambian sus resultados
mediante archivos CSV, y producen **exactamente la misma secuencia**.

---

## 1. Estructura de carpetas

```
Practica 5/
├── Python/
│   ├── main.py                       # punto de entrada
│   ├── generador_lcg.py              # servicio de dominio (fachada LCG)
│   ├── pyproject.toml                # configuración de lint (ruff) y tipado (mypy)
│   ├── conftest.py                   # ajustes de path para pytest
│   ├── estrategias/
│   │   ├── interfaz_generador.py     # contrato Strategy (clase abstracta)
│   │   └── estrategia_lcg.py         # implementación LCG
│   ├── fabricas/
│   │   └── fabrica_generador.py      # Factory Method con registro de tipos
│   ├── servicios/
│   │   ├── analisis.py               # Hull-Dobell, periodo, estadística, chi-cuadrado
│   │   └── comparador.py             # comparación de secuencias y de CSV
│   ├── presentacion/
│   │   ├── menu.py                   # menú interactivo y tablas
│   │   └── graficas.py               # gráficas con Matplotlib
│   ├── datos/
│   │   ├── configuracion.py          # lectura de la configuración INI
│   │   ├── exportador_csv.py         # exportación/lectura de resultados
│   │   └── rutas.py                  # localización de la raíz del proyecto
│   └── pruebas/                      # pruebas automatizadas (pytest)
│       ├── test_generador.py
│       ├── test_servicios.py
│       └── test_integracion_java.py
├── Java/
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/simulacion/
│       │   ├── Main.java
│       │   ├── estrategias/           # Generador.java, EstrategiaLCG.java, ...
│       │   ├── fabricas/              # FabricaGenerador.java
│       │   ├── servicios/             # ServicioLCG.java, Analisis.java, Comparador.java
│       │   ├── datos/                 # ExportadorCSV.java, Configuracion.java, ...
│       │   └── presentacion/          # Menu.java, Presentacion.java
│       └── test/java/com/simulacion/  # pruebas JUnit 5
├── Resultados/
│   ├── resultados_python.csv         # 10 000 valores generados en Python
│   ├── resultados_java.csv           # 10 000 valores generados en Java
│   ├── resultados_python_semilla_2.csv
│   ├── resultados_java_semilla_2.csv
│   ├── comparacion.csv               # comparación de las primeras 20 observaciones
│   ├── comparacion_semillas.csv      # comparación entre dos semillas
│   └── graficas/
│       ├── secuencia_normalizada.png
│       ├── comparativa_semillas.png
│       ├── histograma_frecuencias.png
│       └── comparativa_python_java.png
├── Documentacion/
│   └── informe.md                    # informe técnico y matemático
├── configuracion.ini                 # parámetros compartidos por Python y Java
├── requirements.txt
└── README.md
```

---

## 2. Arquitectura utilizada

Arquitectura **en capas** de tres niveles, sin dependencias de la capa superior
hacia la inferior:

| Capa | Python | Java | Responsabilidad |
|------|--------|------|-----------------|
| Presentación | `presentacion/menu.py`, `presentacion/graficas.py` | `presentacion/Menu.java`, `presentacion/Presentacion.java` | Interacción con el usuario, menús, tablas y gráficas |
| Lógica de negocio | `estrategias/`, `fabricas/`, `servicios/`, `generador_lcg.py` | `estrategias/`, `fabricas/`, `servicios/` | Algoritmo LCG, normalización, validación, análisis del período y comparación |
| Datos | `datos/` | `datos/` | Almacenamiento, exportación CSV, lectura de configuración |

Reglas aplicadas:

- La capa de presentación **no** implementa el algoritmo: consume servicios.
- La capa de datos **no** contiene decisiones de negocio: solo persistencia y E/S.
- Los parámetros se validan en el constructor de la estrategia y en el servicio
  de dominio; los errores de negocio se modelan con excepciones específicas
  (`ParametrosInvalidosError` / `ParametrosInvalidosException`).

### Patrones de diseño

**Strategy (principal).** La clase `Generador` (Python) y la interfaz `Generador`
(Java) definen el contrato común `generar(cantidad)`, `normalizar(estado)` y
`generar_normalizados(cantidad)`. `EstrategiaLCG` implementa la recurrencia.
El servicio de dominio depende del contrato, nunca de la implementación, de
modo que añadir otro generador (Mersenne Twister, Lehmer…) no obliga a
modificar la lógica principal.

**Factory Method (complementario).** `FabricaGenerador.crear(tipo, ...)` resuelve
la implementación a partir de un registro de constructores. Registrar un tipo
nuevo es una línea de código:

```python
FabricaGenerador.registrar("MT19937", GeneradorMT19937)
```

```java
FabricaGenerador.registrar("MT19937", parametros -> new GeneradorMT19937(parametros));
```

No se implementan patrones adicionales, para no sobre-ingenierizar el proyecto.

---

## 3. Requisitos e instalación

- **Python 3.10 o superior** (probado con 3.14).
- **Java 17 o superior** (probado con OpenJDK 25) y **Maven 3.8 o superior**.
- Dependencias de Python: `matplotlib` (gráficas) y `pytest` (pruebas).

```bash
# desde la raíz de "Practica 5"
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Maven no necesita instalación de dependencias adicionales: el `pom.xml` ya
declara JUnit 5 y el plugin de compilación.

---

## 4. Cómo ejecutar

### 4.1 Python

```bash
cd "Practica 5/Python"

python main.py                 # menú interactivo
python main.py --automatica    # flujo completo: simulación, comparaciones y gráficas
python main.py --automatica --semilla 999 --cantidad 5000
python main.py --automatica --sin-graficas
```

Opciones del menú interactivo:

```
1. Ejecutar simulación con la semilla por defecto (12345)
2. Ejecutar simulación con una semilla personalizada
3. Comparar los resultados obtenidos con dos semillas distintas
4. Comparar las secuencias de Python y Java (archivos CSV)
5. Análisis del período del generador (Hull-Dobell)
6. Generar las gráficas de la simulación
7. Salir
```

### 4.2 Java

```bash
cd "Practica 5/Java"

mvn clean package                        # compila y ejecuta las pruebas
java -cp target/classes com.simulacion.Main                 # menú interactivo
java -cp target/classes com.simulacion.Main --automatica    # flujo completo
java -jar target/practica5-lcg-1.0.0.jar --automatica       # empaquetado
```

Alternativa con el plugin de Maven:

```bash
mvn compile exec:java -Dexec.args="--automatica"
```

Los programas localizan la raíz del proyecto automáticamente (buscan la carpeta
que contiene `Python` y `Java`), por lo que los resultados siempre se guardan
en `Practica 5/Resultados`, sin importar el directorio desde el que se ejecuten.

### 4.3 Cómo comparar los resultados

1. Ejecute Python (`--automatica`) para generar `Resultados/resultados_python.csv`.
2. Ejecute Java (`--automatica`) para generar `Resultados/resultados_java.csv`.
3. Python (o Java) detectará automáticamente el CSV del otro lenguaje y
   producirá `Resultados/comparacion.csv` con las primeras 20 observaciones.

Verificación manual desde la terminal:

```bash
cd "Practica 5/Resultados"
diff resultados_python.csv resultados_java.csv && echo "Secuencias idénticas"
```

Las columnas `x` (estado crudo) y `normalizado` coinciden **byte a byte** entre
los dos archivos, y la comparación de las 10 000 observaciones confirma que las
secuencias son idénticas.

### 4.4 Cómo generar las gráficas

Las gráficas se generan con Python y Matplotlib (el motor `Agg`, sin interfaz
gráfica):

```bash
cd "Practica 5/Python"
python main.py --automatica
```

o desde el menú interactivo, opción **6**. Los archivos se guardan en
`Practica 5/Resultados/graficas/`:

| Gráfica | Descripción |
|---------|-------------|
| `secuencia_normalizada.png` | Serie temporal de los 10 000 valores normalizados |
| `comparativa_semillas.png` | Comparación de dos semillas (serie temporal y dispersión) |
| `histograma_frecuencias.png` | Histograma de frecuencias con la frecuencia esperada |
| `comparativa_python_java.png` | Dispersión y diferencia absoluta entre Python y Java |

---

## 5. Pruebas

```bash
# Python (41 pruebas)
cd "Practica 5/Python"
python -m pytest pruebas -v

# Java (24 pruebas JUnit 5)
cd "Practica 5/Java"
mvn test
```

Cobertura de las pruebas:

| Requisito | Prueba |
|-----------|--------|
| Parámetros válidos e inválidos | `TestValidacionDeParametros`, `parametrosInvalidos` |
| Se generan exactamente 10 000 valores | `test_se_generan_exactamente_10000_valores`, `cantidadDeValores` |
| Valores normalizados en `[0, 1)` | `test_todos_los_valores_normalizados_estan_en_el_intervalo_unitario`, `valoresNormalizadosEnRango` |
| Python y Java producen la misma secuencia | `TestIntegracionPythonJava` (compara los CSV y exige identidad byte a byte) |
| Cambiar la semilla produce otra secuencia | `test_cambiar_la_semilla_produce_una_secuencia_distinta`, `semillaDistintaProduceSecuenciaDistinta` |
| Los archivos CSV se generan correctamente | `TestCapaDeDatos`, `exportarResultados`, `exportarComparacion` |
| Condiciones de Hull-Dobell y período | `TestAnalisisDelPeriodo`, `hullDobell` |
| Uniformidad de la distribución | `test_la_prueba_chi_cuadrado_no_rechaza_la_uniformidad` |

Herramientas de calidad adicionales (opcionales):

```bash
cd "Practica 5/Python"
ruff check .        # análisis estático de estilo y errores
ruff format --check .
mypy .              # verificación de tipos
```

---

## 6. Resultados obtenidos (verificados)

- Primeras 20 observaciones **idénticas** en Python y Java
  (`87628868, 71072467, 2332836374, 2726892157, ...`).
- Las 10 000 observaciones coinciden en ambos lenguajes y los CSV son idénticos
  byte a byte.
- Estadísticas de la simulación (semilla 12 345): media `0.498769847970`
  (teórico 0.5), varianza `0.083011766847` (teórico 0.083333333333).
- Chi-cuadrado con 20 intervalos: `X² = 24.08 < 30.144` (valor crítico al 95 %
  con 19 grados de libertad): no se rechaza la uniformidad.
- Hull-Dobell: las tres condiciones se cumplen, por lo que el período **teórico**
  es `m = 4 294 967 296` valores; la simulación observa únicamente los
  10 000 primeros (0.000233 % del ciclo).

El detalle matemático, la arquitectura y las conclusiones están en
[`Documentacion/informe.md`](Documentacion/informe.md).
