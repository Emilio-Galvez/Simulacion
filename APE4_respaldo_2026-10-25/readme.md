# Simulación SIR en Java — APE 4

Implementación de la guía `ape_guia simulacion semana 4-firmado-signed.pdf`.
Usa Java sin bibliotecas externas ni interfaz gráfica. Requiere JDK 11 o superior.

## Compilar y ejecutar

Desde la carpeta del proyecto, en Linux o macOS:

```bash
mkdir -p out
javac -encoding UTF-8 -d out src/Main.java src/modelo/*.java src/controlador/*.java
java -cp out Main
```

Se genera `resultados/resultados_java.csv`. La carpeta `resultados` se crea automáticamente si no existe. Cada ejecución reemplaza ese archivo.
Para usar otra semilla aleatoria:

```bash
java -cp out Main 123
```

La semilla predeterminada es 42. Con la misma semilla, una nueva ejecución reproduce
los mismos resultados en este programa. No garantiza resultados idénticos a Python
o NetLogo, que pueden generar o consumir números aleatorios de otra manera.

## Organización MVC sin vista

- **Modelo:** `Estado`, `Resultado` y `ModeloSIR`, dentro de `src/modelo`.
  Contiene únicamente los estados, los datos de cada resultado y los parámetros del modelo.
- **Controlador:** `ControladorSimulacion`, dentro de `src/controlador`.
  Contiene los métodos para crear la población, simular los pasos y contar los estados.
  `ExportadorCSV`, en la misma carpeta, contiene el método para guardar el CSV.
- **Resultados:** `resultados/` contiene los archivos generados por la simulación.
- **Entrada:** `Main` inicia el controlador y comunica si el archivo se generó.

Se conserva la separación de responsabilidades de MVC, omitiendo la vista según
lo solicitado. La visualización posterior corresponde a NetLogo.

## Parámetros y reglas

Los parámetros editables están al inicio de `main`, en `src/Main.java`.
Allí también se configuran la semilla y la ruta del CSV. `ModeloSIR` solo almacena
los parámetros y el controlador los valida antes de simular:

| Parámetro | Valor |
| --- | --- |
| Población | 100 |
| Susceptibles iniciales | 95 |
| Infectados iniciales | 5 |
| Recuperados iniciales | 0 |
| Beta: probabilidad de transmisión por contacto | 0,30 |
| Gamma: probabilidad de recuperación por paso | 0,10 |
| Pasos de simulación | 100 |

Las fórmulas están separadas en dos métodos de `ControladorSimulacion`:

- `calcularContagiosEsperados(S, I)`: beta * S * I / N.
- `calcularRecuperacionesEsperadas(I)`: gamma * I.

Se utiliza un paso de tiempo de una unidad. Los valores esperados se dividen por
el tamaño de cada grupo para obtener las probabilidades individuales:
`p(contagio) = beta * I / N` y `p(recuperación) = gamma`.
Se sortea cada cambio de estado con esas probabilidades, conservando conteos enteros.
Los grupos vacíos se manejan sin divisiones entre cero.
Esta regla reemplaza la selección de un contacto por infectado. Para comparar las
herramientas, Python y NetLogo deberán usar también esta regla.

Se lee la población al inicio del paso y se escriben los cambios en una copia.
Así, un nuevo infectado comienza a contagiar y puede recuperarse desde el siguiente
paso. Un infectado que se recupera en el paso todavía puede transmitir durante ese
paso. Los recuperados no vuelven a infectarse.

Esta es una simulación aleatoria de individuos, con actualización simultánea de estados;
no es una integración numérica de las ecuaciones diferenciales. Las cantidades son
enteras y siempre se conserva `S + I + R = 100`.

## Datos exportados

```csv
tiempo,susceptibles,infectados,recuperados
0,95,5,0
```

El archivo contiene un encabezado y 101 filas de datos: del tiempo 0 al 100,
incluyendo ambos extremos. Se registra el estado inicial y después de cada paso.
Aunque no queden infectados, se continúa registrando hasta el tiempo 100.

Para la integración indicada en la guía, copia `resultados/resultados_java.csv` junto a
`modelo_sir_netlogo.nlogo`. NetLogo debe leer el encabezado y las cuatro columnas
para graficar S, I y R respecto al tiempo. Este proyecto cubre la implementación
Java y su exportación; las implementaciones Python y NetLogo son partes separadas
de la práctica.

El CSV usa UTF-8, comas como separadores y valores enteros, sin filas de resumen
ni mensajes mezclados con los datos. Al importarlo, se debe omitir el encabezado:
la columna 0 corresponde al tiempo (eje X), y las columnas 1, 2 y 3 a S, I y R
(eje Y). Estos conteos permiten graficar la evolución; no contienen posiciones ni
identificadores para reconstruir el movimiento de personas individuales.
Se verificó la estructura y la coherencia de los datos; la importación en una
vista concreta de NetLogo queda pendiente porque este proyecto no incluye un `.nlogo`.

La rúbrica menciona M/M/1, pero el fundamento, los parámetros y el procedimiento
de la guía corresponden al modelo SIR, que es el implementado aquí.
