# 🌧️ Práctica 01 de Simulación

## 📖 Descripción del proyecto

Este proyecto simula la posibilidad de lluvia durante un día, hora por hora (de 06:00 a 22:00).
Con datos de humedad, nubosidad y temperatura calcula un índice de lluvia y lo clasifica en cuatro estados.
Sirve para comparar cómo se comporta un modelo de predicción inicial frente a uno ajustado.
Es un programa de consola, sin interfaz gráfica, base de datos, API ni servidor.

## 🛠️ Tecnologías utilizadas

- **Python 3.14**
- **NumPy** (para manejar los datos de forma ordenada)
- **Matplotlib** (para mostrar las gráficas al final)

No se usan otras librerías. Las dependencias están en `requirements.txt`.

## 💻 Instalación

El entorno virtual (venv) está en la carpeta superior a `practica1/`, no dentro de ella.
Los comandos son para Linux o WSL.

```bash
# 1. Ir a la carpeta que contiene el entorno virtual
cd ~/simulacion

# 2. Activar el entorno virtual
source venv/bin/activate

# 3. Instalar las dependencias del proyecto
pip install -r practica1/requirements.txt
```

Si las dependencias ya están instaladas, el paso 3 se puede omitir.

## ▶️ Uso

El programa se ejecuta desde la carpeta `codigo/`, porque ahí viven los paquetes `datos`, `simulador` y `main`.

```bash
cd practica1/codigo
python -m main.main
```

El comando `python -m main.main` es el correcto. Ejecutar `python main/main.py` da error, porque los imports del programa esperan estar parado en la carpeta `codigo/`.

Al final se abre una ventana con tres gráficas: el índice de lluvia, la humedad y nubosidad, y la temperatura con su factor `Tf`.

### Ejemplo de salida en consola

```text
TABLA DE RESULTADOS
---------------------------------------------------------------------------
Hora     Humedad    Nubosidad    Temp     Tf       Índice     Resultado
---------------------------------------------------------------------------
06:00    65         40           14       0.80     0.605      Lluvia probable
08:00    70         50           16       0.70     0.640      Lluvia probable
10:00    68         45           18       0.60     0.595      Baja posibilidad
12:00    60         30           22       0.40     0.470      Baja posibilidad
14:00    75         70           20       0.50     0.685      Lluvia probable
16:00    85         85           18       0.60     0.800      Lluvia
18:00    92         95           16       0.70     0.885      Lluvia
20:00    88         90           17       0.60     0.830      Lluvia
22:00    80         75           15       0.70     0.765      Lluvia
```

Nota: antes de la tabla aparecen cuatro números (`0.8`, `0.6`, `0.15`, `0.1`). Son una pequeña prueba interna del factor de temperatura que se imprime al cargar el archivo del factor.

## 📁 Estructura del proyecto

```text
practica1/
├── codigo/
│   ├── datos/
│   │   ├── datos_climaticos.py    # Datos de entrada: hora, humedad, nubosidad y temperatura
│   │   └── factor_temperatura.py  # Tabla que convierte la temperatura en un factor Tf
│   ├── main/
│   │   └── main.py                # Programa principal (la vista): ejecuta la simulación y muestra la tabla y las gráficas
│   └── simulador/
│       ├── modelo_prediccion.py   # Modelo base, deja claro qué debe tener todo modelo de predicción
│       ├── modelo_inicial.py      # Modelo inicial (pesos 0.5 / 0.3 / 0.2)
│       ├── modelo_ajustado.py     # Modelo ajustado (pesos 0.4 / 0.5 / 0.1)
│       └── simulador.py           # Intermediario (el controlador): recibe los datos y llama al modelo
├── README.md                      # Este archivo
├── requirements.txt               # Librerías que usa el proyecto (numpy y matplotlib)
├── referencias.bib                # Referencia bibliográfica usada
└── informe_practica1_overleaf__1_.pdf  # Informe de la práctica
```

En resumen: `datos` guarda la información y la tabla de temperatura, `simulador` tiene la lógica matemática y el intermediario, y `main` es el punto de entrada del programa.

## 📝 Información adicional

### Funcionalidades principales

- Recorre 9 horas del día (06:00 a 22:00).
- Calcula el índice de lluvia `I = r_H·H + r_N·N + r_T·Tf`.
- Obtiene el factor de temperatura `Tf` desde una tabla.
- Clasifica el índice en cuatro estados.
- Muestra una tabla de resultados en consola.
- Muestra tres gráficas con Matplotlib.

El programa principal usa el **modelo inicial**. El **modelo ajustado** también está definido y se puede usar cambiando una línea en `main.py`, pero tal como está el código no se ejecuta en la corrida normal.

### Pesos de cada modelo

Los pesos suman 1 en ambos modelos.

| Modelo   | Peso humedad (r_H) | Peso nubosidad (r_N) | Peso temperatura (r_T) |
|:---------|:------------------:|:--------------------:|:----------------------:|
| Inicial  |        0.5         |         0.3          |          0.2           |
| Ajustado |        0.4         |         0.5          |          0.1           |

### Estados según el índice

| Valor del índice I |      Estado      |
|:------------------:|:----------------:|
| I < 0.40           |    Sin lluvia    |
| 0.40 ≤ I < 0.60    | Baja posibilidad |
| 0.60 ≤ I < 0.75    | Lluvia probable  |
| I ≥ 0.75           |      Lluvia      |

### Tabla del factor de temperatura (Tf)

| Temperatura (°C) | Factor Tf |
|:----------------:|:---------:|
| ≤ 10             |   1.00    |
| ≤ 12             |   0.90    |
| ≤ 14             |   0.80    |
| ≤ 16             |   0.70    |
| ≤ 18             |   0.60    |
| ≤ 20             |   0.50    |
| ≤ 22             |   0.40    |
| ≤ 24             |   0.30    |
| ≤ 26             |   0.20    |
| < 28             |   0.15    |
| ≥ 28             |   0.10    |

### Referencias

- Guamán Q., José O. *Introducción a la Simulación: del mundo real al modelo*. Diapositivas de clase, Semana 1. Carrera de Computación, Universidad Nacional de Loja, 2026.

### Autor

- **Autor:** Emilio Jose Galvez Merchan
- **Docente:** José O. Guamán Q.
- **Asignatura:** Simulación (ciclo 5)
- **Universidad Nacional de Loja**
