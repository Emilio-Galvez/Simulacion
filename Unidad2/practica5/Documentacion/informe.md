# Informe técnico — Implementación y análisis del Generador Congruencial Lineal (LCG)

**Asignatura:** Simulación
**Práctica:** 5
**Tecnologías:** Python 3 y Java 17+

---

## 1. Introducción

El Generador Congruencial Lineal (LCG, *Linear Congruential Generator*) es el
generador de números pseudoaleatorios más simple y,
posiblemente, el más utilizado en la historia de la computación. Fue introducido por Lehmer
(1951) y su uso masivo se popularizó con el libro *Random Number Generators and
Applied Stochastic Processes* de A. R. Teichroew y J. H. Ahrens, y con el
algoritmo de Numerical Recipes. En la práctica, el LCG es el motor de
generación de las bibliotecas de simulación de C, Java (`java.util.Random`),
C++ y de numerosos entornos de simulación discretos.

La práctica consiste en implementar el LCG en dos lenguajes de propósito
general (Python y Java), verificar la equivalencia exacta de ambas
implementaciones, analizar estadísticamente la distribución generada, estudiar
el período del ciclo y disparatear las conclusiones con el soporte de una
arquitectura de software en capas y dos patrones de diseño.

---

## 2. Fundamento matemático

### 2.1 Definición

Un LCG produce una secuencia de enteros pseudoaleatorios a partir de la
recurrencia lineal congruencial:

```
X(n+1) = (a · X(n) + c) mod m
```

con:

| Símbolo | Significado | Valor utilizado |
|---------|-------------|-----------------|
| `a` | multiplicador | 1 664 525 |
| `c` | incremento | 1 013 904 223 |
| `m` | módulo | 2^32 = 4 294 967 296 |
| `X(0)` | semilla inicial | 12 345 |
| `n` | cantidad de valores | 10 000 |

El término `X(n)` se denomina *estado* del generador. A partir de los estados
enteros se obtiene la variable pseudoaleatoria normalizada:

```
U(n) = X(n) / m
```

que toma valores en el intervalo `[0, 1)`, excepto el valor 1, y es apta para ser transformada por la función de
distribución acumulada inversa (CDF inversa) de cualquier distribución.

### 2.2 Período theoretical: teorema de Hull-Dobell

El período de un LCG es la longitud de la secuencia de estados antes de que
aparezca una repetición. Para que el generador tenga el **período completo**
`m` (es decir, recorra los `m` estados posibles sin repetir antes de volver al
semilla), el matemático Hull y Dobell (1963) establecieron tres condiciones
necesarias y suficientes:

1. `c` y `m` deben ser primos relativos.
2. `a - 1` debe ser divisible por todos los factores primos de `m`.
3. Si `m` es divisible por 4, entonces `a - 1` debe ser divisible por 4.

Una formulación equivalente y más operativa (usada en el código del proyecto)
es:

1. `c ≡ 1 (mod p)` para todo factor primo `p` de `m`.
2. `a ≡ 1 (mod p)` para todo factor primo `p` de `m`.
3. Si `4 | m`, entonces `a ≡ 1 (mod 4)`.

#### 2.2.1 Comprobación con los parámetros de la práctica

Como `m = 2^32`, su único factor primo es `p = 2`.

| Condición | Cálculo | Resultado |
|-----------|---------|-----------|
| `c ≡ 1 (mod 2)` | 1 013 904 223 es impar, luego `c mod 2 = 1` | Cumple |
| `a ≡ 1 (mod 2)` | 1 664 525 es impar, luego `a mod 2 = 1` | Cumple |
| `a ≡ 1 (mod 4)` (porque `4 | m`) | 1 664 525 = 4 · 416 131 + 1, luego `a mod 4 = 1` | Cumple |

Las tres condiciones se satisfacen, por lo que el generador alcanza el
**período completo**:

```
Período teórico = m = 2^32 = 4 294 967 296 valores
```

Estos parámetros corresponden al conjunto conocido como *Numerical Recipes*
(minimal standard), elegido porque cumple Hull-Dobell y porque su parte alta
(`X(n) >> 16`) y su parte baja (`X(n) & 0xFFFF`) tienen buenas propiedades
estadísticas.

#### 2.2.2 Período teórico frente a cantidad generada

| Magnitud | Valor | Observación |
|----------|-------|-------------|
| Período teórico (máximo ciclo posible) | 4 294 967 296 valores | Propiedad matemática del par `(a, c, m)` |
| Cantidad generada en la práctica | 10 000 valores | Decisión experimental de la práctica |
| Fracción del ciclo observada | 0.000233 % | 10 000 / 4 294 967 296 |

La diferencia es esencial: el período es una **propiedad del generador**, no
del experimento. Aunque en esta práctica sólo se generan 10 000 valores, el
generador **no** se agota ni se reinicia: si se siguiera iterando, la secuencia
continuaría sin repetir hasta completar 4 294 967 296 estados distintos. La
detección empírica implementada en `Analisis.periodo_empirico` confirma que
**no hay ninguna repetición** dentro de las 10 000 muestras, lo que es
consistente con un período mucho mayor que el número de observaciones.

### 2.3 Desbordamiento numérico

El producto `a · X(n)` puede alcanzar
`1 664 525 × 4 294 967 295 ≈ 7.149 × 10^15`, valor que **excede los 32 bits**
(4.295 × 10^9) pero **cabe en 64 bits** (`Long.MAX_VALUE ≈ 9.223 × 10^18`).

- En **Python** los enteros tienen precisión arbitraria: `a * x + c` se calcula
  sin pérdida y el operador `%` aplica directamente la reducción modular.
- En **Java** se utiliza `long` (64 bits con signo) para el producto y, cuando
  el módulo es una potencia de dos, se aplica la máscara `0xFFFFFFFF`:

```java
long producto = multiplicador * estado + incremento;
if (esPotenciaDeDos(modulo)) {
    return producto & (modulo - 1);   // equivale a producto mod 2^32
}
return Math.floorMod(producto, modulo);
```

La máscara reproduce exactamente el comportamiento modular de 32 bits exigido
por el enunciado, sin recurrir a aritmética de precisión arbitraria.

### 2.4 Formato de intercambio entre lenguajes

Un detalle sutil pero relevante para la comparación entre Python y Java es el
**redondeo decimal**. `U(n) = X(n)/2^32` es un binario exacto, pero al
imprimirlo con 12 decimales Python redondea al par y Java redondea al alza: en
los casos de empate (por ejemplo `X = 2 097 152 → 0.00048828125`) ambos
lenguajes imprimirían textos distintos.

Para evitarlo, el proyecto calcula el valor normalizado exportado mediante
**división entera exacta**:

```text
escalado  = (X(n) · 10^12) // m        (Python: ints; Java: BigInteger)
normalizado = escalado / 10^12  con 12 decimales, truncado
```

El truncamiento es determinista en ambos lenguajes, de modo que las columnas
`x` y `normalizado` de los dos archivos CSV son **idénticas byte a byte**.

---

## 3. Arquitectura de software

### 3.1 Arquitectura en capas

El proyecto se organiza en tres capas, con dependencias exclusivamente hacia
dentro (la capa superior conoce la inferior, nunca al revés):

```
┌──────────────────────────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN                                        │
│  Menú interactivo · tablas · gráficas (Matplotlib)          │
│  Python: presentacion/menu.py, presentacion/graficas.py      │
│  Java:   presentacion/Menu.java, presentacion/Presentacion  │
├──────────────────────────────────────────────────────────────┤
│  CAPA DE LÓGICA DE NEGOCIO                                   │
│  Algoritmo LCG · normalización · validación · período       │
│  · comparación de secuencias                                 │
│  Python: estrategias/, fabricas/, servicios/, generador_lcg  │
│  Java:   estrategias/, fabricas/, servicios/                 │
├──────────────────────────────────────────────────────────────┤
│  CAPA DE DATOS                                               │
│  Exportación/lectura CSV · configuración · rutas del proyecto│
│  Python: datos/   Java: datos/                               │
└──────────────────────────────────────────────────────────────┘
```

**Capa de presentación.** `Menu` (Python) y `Menu` (Java) implementan el menú
interactivo, la presentación de tablas y el despliegue de resultados. Python
incorpora además `GeneradorGraficas`, que produce las figuras con Matplotlib
usando el motor `Agg` (permite generar las imágenes en servidores sin
interfaz gráfica). Java no depende de bibliotecas de graficación: muestra un
histograma ASCII en consola y remite al script de Python para las figuras
académicas.

**Capa de lógica de negocio.** Contiene la recurrencia del LCG, la
normalización, la validación de parámetros, el análisis del período (Hull-Dobell
y detección empírica de ciclos), las estadísticas descriptivas, la prueba
chi-cuadrado y la comparación de secuencias. `ServicioLCG` actúa como fachada de
dominio: coordina la configuración, la fábrica y la estrategia.

**Capa de datos.** `ExportadorCSV` (Python y Java) define y consume el formato
de intercambio `indice,x,normalizado`; `Configuracion` lee el archivo INI
compartido por ambos lenguajes; `RutasProyecto`/`rutas.py` localizan la raíz
del proyecto para que los ejecutables funcionen desde cualquier directorio.

### 3.2 Patrón Strategy

El contrato común se define en la clase abstracta `Generador` (Python) y en la
interfaz `Generador` (Java):

```python
class Generador(ABC):
    @abstractmethod
    def generar(self, cantidad: int) -> list[int]: ...
    @abstractmethod
    def normalizar(self, estado: int) -> float: ...
    def generar_normalizados(self, cantidad: int) -> list[float]:
        return [self.normalizar(x) for x in self.generar(cantidad)]
```

```java
public interface Generador {
    long[] generar(int cantidad);
    double normalizar(long estado);
    default double[] generarNormalizados(int cantidad) { ... }
}
```

La implementación concreta `EstrategiaLCG` contiene la recurrencia. El
beneficio arquitectónico es directo: `ServicioLCG`, `Analisis` y `Comparador`
dependen del contrato y no de la implementación; sustituir o añadir un
generador (por ejemplo un Mersenne Twister) no obliga a modificar la lógica
principal ni la presentación.

### 3.3 Patrón Factory Method

`FabricaGenerador` mantiene un registro de constructores indexados por tipo:

```python
class FabricaGenerador:
    _registro: ClassVar[dict[str, ConstructorGenerador]] = {}

    @classmethod
    def crear(cls, tipo: str = "LCG", **parametros) -> Generador:
        constructor = cls._registro.get(tipo.strip().upper())
        if constructor is None:
            raise TipoGeneradorDesconocidoError(...)
        return constructor(**parametros)
```

```java
public final class FabricaGenerador {
    private static final Map<String, Function<ParametrosGenerador, Generador>> REGISTRO = ...;

    public static Generador crear(String tipo, ParametrosGenerador parametros) { ... }
}
```

El registro (y no una cadena de `if/else`) hace que añadir un generador nuevo
sea una operación localizada y de bajo riesgo. El patrón se complementa con
el Strategy: la fábrica decide **qué** estrategia construir y la estrategia
decide **cómo** generar.

### 3.4 Patrones no implementados

Siguiendo el criterio de simplicidad del enunciado, no se introducen patrones
adicionales (Observer, Singleton, Adapter, etc.): el número de clases y el
acoplamiento siguen siendo reducidos y cada elemento del código tiene una
responsabilidad única.

---

## 4. Procedimiento experimental

1. Se genera la secuencia con `X(0) = 12 345` y los parámetros del enunciado,
   en Python y en Java, de forma independiente.
2. Cada implementación exporta su secuencia a `Resultados/resultados_*.csv`.
3. Se comparan las primeras 20 observaciones y luego las 10 000 completas.
4. Se repite el experimento con `X(0) = 54 321` y se contrastan ambas semillas.
5. Se calculan estadísticos y se aplica la prueba chi-cuadrado.
6. Se generan las gráficas y el histograma de frecuencias.

---

## 5. Resultados

### 5.1 Primeras 20 observaciones (idénticas en Python y Java)

| n | X(n) | U(n) = X(n)/m |
|---|------|----------------|
| 1 | 87 628 868 | 0.020402685739 |
| 2 | 71 072 467 | 0.016547848237 |
| 3 | 2 332 836 374 | 0.543155794497 |
| 4 | 2 726 892 157 | 0.634904056088 |
| 5 | 3 908 547 000 | 0.910029513761 |
| 6 | 483 019 191 | 0.112461669137 |
| 7 | 2 129 828 778 | 0.495889405254 |
| 8 | 2 355 140 353 | 0.548348844284 |
| 9 | 2 560 230 508 | 0.596100117079 |
| 10 | 3 364 893 915 | 0.783450416056 |
| 11 | 171 172 990 | 0.039854317437 |
| 12 | 3 194 601 925 | 0.743801222415 |
| 13 | 4 148 119 648 | 0.965809367597 |
| 14 | 316 399 679 | 0.073667540913 |
| 15 | 3 004 788 882 | 0.699606929440 |
| 16 | 1 976 948 425 | 0.460294174263 |
| 17 | 1 702 883 732 | 0.396483515389 |
| 18 | 4 121 112 547 | 0.959521286888 |
| 19 | 1 744 294 886 | 0.406125301029 |
| 20 | 4 092 090 893 | 0.952764156507 |

La comparación de las 10 000 observaciones devuelve
`SECUENCIAS IDENTICAS`, y los archivos `resultados_python.csv` y
`resultados_java.csv` son idénticos byte a byte.

### 5.2 Estadísticas descriptivas (semilla 12 345)

| Estadístico | Valor obtenido | Valor teórico |
|-------------|----------------|---------------|
| Cantidad | 10 000 | 10 000 |
| Mínimo | 0.000059082638 | ≈ 0 |
| Máximo | 0.999925965443 | ≈ 1 |
| Media | 0.498769847970 | 0.5 |
| Varianza | 0.083011766847 | 1/12 = 0.083333333333 |
| Desviación estándar | 0.288117626755 | 0.288675134595 |

La media y la varianza están muy próximas a los valores teóricos de la
distribución uniforme `U(0,1)`, lo que indica un comportamiento correcto del
generador en la ventana observada.

### 5.3 Prueba de uniformidad chi-cuadrado

Con 20 intervalos equiprobables y 10 000 observaciones, la frecuencia esperada
es 500 por intervalo. Resultado obtenido:

| Magnitud | Valor |
|----------|-------|
| Estadístico `X²` | 24.08 |
| Grados de libertad | 19 |
| Valor crítico (α = 0.05) | 30.144 |
| Conclusión | **No se rechaza la hipótesis de uniformidad** |

### 5.4 Efecto de cambiar la semilla

Con `X(0) = 54 321` la primera observación cambia (`X(1) = 1 238 253 532`) y
**las 10 000 posiciones difieren**: el generador produce una secuencia
completamente distinta. Esto es coherente con la teoría: para un LCG de período
completo, la secuencia es una reordenación del mismo conjunto de estados, y
cualquier semilla produce un recorrido diferente pero estadísticamente
equivalente.

### 5.5 Gráficas

| Gráfica | Interpretación |
|----------|----------------|
| `secuencia_normalizada.png` | La serie no muestra tendencia, ciclos ni valores agrupados: comportamiento compatible con ruido uniforme |
| `comparativa_semillas.png` | Dos semillas distintas producen series visualmente distintas; la dispersión `U(12345)` frente a `U(54321)` es una nube sin estructura, indicio de independencia entre ambas secuencias |
| `histograma_frecuencias.png` | Las frecuencias por intervalo se sitúan en torno a 200 (valor esperado) sin tendencias sistemáticas |
| `comparativa_python_java.png` | La dispersión de `U Python` frente a `U Java` se ajusta exactamente a la recta `y = x` y la diferencia absoluta entre ambos lenguajes es 0 en las 10 000 observaciones |

---

## 6. Conclusiones

1. El LCG con los parámetros `a = 1 664 525`, `c = 1 013 904 223` y `m = 2^32`
   satisface las tres condiciones de Hull-Dobell y alcanza el período completo
   `m = 4 294 967 296`.
2. La cantidad de valores generados en la práctica (10 000) es tres órdenes de
   magnitud inferior al período teórico; en consecuencia no se observa ninguna
   repetición y la simulación no puede "reutilizar" números pseudoaleatorios.
3. Las implementaciones en Python y Java producen **exactamente la misma
   secuencia**, verificado sobre las 10 000 observaciones y byte a byte sobre los
   archivos CSV de intercambio.
4. Cambiar la semilla inicial produce una secuencia distinta con las mismas
   propiedades estadísticas.
5. La arquitectura en capas junto con los patrones Strategy y Factory Method
   permite sustituir el algoritmo de generación o el mecanismo de persistencia
   sin modificar las capas superiores, y facilita la verificación automatizada
   (41 pruebas en Python y 24 en Java).

### Limitaciones y trabajo futuro

- El LCG es un generador **lineal**: su correlación espectral es alta y no es
  apto para simulación estocástica de alta calidad (simulación Monte Carlo
  Multidimensional). Para ese fin se recomiendan generadores no lineales o
  múltiples flujos (Box-Muller, L'Ecuyer).
- Sólo las 10 000 primeras muestras se han analizado estadísticamente;
  un análisis de cobertura de todo el ciclo requeriría 4.295 × 10^9 iteraciones.
- Como extensión natural del proyecto sería implementar un segundo generador
  (por ejemplo Mersenne Twister) aprovechando el Strategy y el Factory Method ya
  implementados, y añadir la lectura de una configuración externa por formato
  JSON.

---

## 7. Reproducibilidad

```bash
# Python
cd "Practica 5/Python" && python main.py --automatica

# Java
cd "Practica 5/Java" && mvn clean package && java -cp target/classes com.simulacion.Main --automatica

# Verificación de la igualdad
cd "Practica 5/Resultados" && diff resultados_python.csv resultados_java.csv

# Pruebas
cd "Practica 5/Python" && python -m pytest pruebas -v
cd "Practica 5/Java" && mvn test
```
