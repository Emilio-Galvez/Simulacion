"""Punto de entrada de la implementacion en Python del Generador LCG.

Uso rapido:

    python main.py                    # menu interactivo
    python main.py --automatica       # flujo completo sin interaccion
    python main.py --automatica --semilla 999 --cantidad 5000
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence

RAIZ_PYTHON = os.path.dirname(os.path.abspath(__file__))
if RAIZ_PYTHON not in sys.path:
    sys.path.insert(0, RAIZ_PYTHON)

from datos.configuracion import Configuracion  # noqa: E402
from datos.exportador_csv import ExportadorCSV, formatear_normalizado_exacto  # noqa: E402
from datos.rutas import (  # noqa: E402
    directorio_graficas,
    directorio_resultados,
    encontrar_raiz_proyecto,
    ruta_configuracion,
)
from generador_lcg import ServicioLCG  # noqa: E402
from presentacion.graficas import GeneradorGraficas  # noqa: E402
from presentacion.menu import (  # noqa: E402
    ARCHIVO_COMPARACION,
    ARCHIVO_COMPARACION_SEMILLAS,
    ARCHIVO_RESULTADOS_JAVA,
    ARCHIVO_RESULTADOS_PYTHON,
    Menu,
)
from servicios.analisis import Analisis  # noqa: E402
from servicios.comparador import Comparador  # noqa: E402

SEMILLA_ALTERNATIVA = 54321
ARCHIVO_RESULTADOS_PYTHON_SEMILLA_2 = "resultados_python_semilla_2.csv"


def construir_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos de la linea de comandos."""
    parser = argparse.ArgumentParser(
        description="Simulacion del Generador Congruencial Lineal (LCG) en Python."
    )
    parser.add_argument(
        "--semilla", type=int, default=None, help="Semilla inicial X(0) para la simulacion."
    )
    parser.add_argument("--cantidad", type=int, default=None, help="Cantidad de numeros a generar.")
    parser.add_argument(
        "--semilla-2",
        type=int,
        default=SEMILLA_ALTERNATIVA,
        help="Segunda semilla para la comparacion entre semillas.",
    )
    parser.add_argument(
        "--automatica",
        action="store_true",
        help="Ejecuta el flujo completo (simulacion, comparaciones y graficas) sin menu.",
    )
    parser.add_argument("--salida", default=None, help="Carpeta donde se guardan los resultados.")
    parser.add_argument(
        "--sin-graficas", action="store_true", help="Omite la generacion de graficas."
    )
    return parser


def cargar_configuracion(args: argparse.Namespace) -> Configuracion:
    """Carga la configuracion desde el archivo INI y aplica los argumentos."""
    raiz = encontrar_raiz_proyecto()
    configuracion = Configuracion.desde_archivo(ruta_configuracion(raiz))
    if args.semilla is not None:
        configuracion = configuracion.con_semilla(args.semilla)
    if args.cantidad is not None:
        configuracion = Configuracion(
            multiplicador=configuracion.multiplicador,
            incremento=configuracion.incremento,
            modulo=configuracion.modulo,
            semilla=configuracion.semilla,
            cantidad=args.cantidad,
        )
    configuracion.validar()
    return configuracion


def flujo_automatico(
    servicio: ServicioLCG,
    directorio_resultados: str,
    directorio_graficas: str,
    semilla_2: int,
    generar_graficas: bool,
) -> None:
    """Ejecuta el flujo completo de la practica de forma no interactiva."""
    configuracion = servicio.configuracion
    modulo = configuracion.modulo

    print("=" * 78)
    print("SIMULACION LCG - EJECUCION AUTOMATICA (PYTHON)")
    print("=" * 78)
    print(
        f"a = {configuracion.multiplicador} | c = {configuracion.incremento} | "
        f"m = {configuracion.modulo} | X(0) = {configuracion.semilla} | "
        f"n = {configuracion.cantidad}"
    )

    resultado = servicio.simular()
    ruta_python = ExportadorCSV.exportar_resultados(
        os.path.join(directorio_resultados, ARCHIVO_RESULTADOS_PYTHON),
        resultado.estados,
        modulo,
    )
    print(f"\n[OK] {configuracion.cantidad:,} valores generados y exportados en: {ruta_python}")
    print("\nPrimeras 20 observaciones:")
    print(f"{'n':>4} | {'X(n)':>12} | {'U(n) = X(n)/m':>18}")
    print("-" * 40)
    for indice, estado in enumerate(resultado.estados[:20], start=1):
        print(f"{indice:>4} | {estado:>12} | {formatear_normalizado_exacto(estado, modulo):>18}")

    print("\nEstadisticas descriptivas:")
    estadisticas = resultado.estadisticas
    print(f"  Media          : {estadisticas['media']:.12f} (teorico 0.5)")
    print(f"  Varianza       : {estadisticas['varianza']:.12f} (teorico 0.083333333333)")
    print(f"  Minimo / Maximo: {estadisticas['minimo']:.12f} / {estadisticas['maximo']:.12f}")

    chi_cuadrado = Analisis.prueba_chi_cuadrado(resultado.normalizados, bins=20)
    print("\nPrueba de uniformidad chi-cuadrado (20 intervalos, 95%):")
    print(
        f"  Estadistico X2 = {chi_cuadrado.estadistico:.4f} | "
        f"Valor critico = {chi_cuadrado.valor_critico:.4f} | "
        f"Conclusion: {'se rechaza la uniformidad' if chi_cuadrado.rechaza_hipotesis else 'no se rechaza la uniformidad'}"
    )

    verificacion = Analisis.verificar_hull_dobell(
        configuracion.multiplicador, configuracion.incremento, configuracion.modulo
    )
    print("\nAnalisis del periodo (Hull-Dobell):")
    for condicion in verificacion.condiciones:
        print(f"  [{'OK' if condicion.cumple else 'FALLA'}] {condicion.descripcion}")
    print(f"  {verificacion.resumen}")
    print(
        f"  Se generan {configuracion.cantidad:,} valores de un ciclo teorico de "
        f"{verificacion.periodo_teorico:,} "
        f"({configuracion.cantidad / verificacion.periodo_teorico * 100:.6f}%)."
    )

    resultado_2 = servicio.simular(semilla_2)
    ruta_semilla_2 = ExportadorCSV.exportar_resultados(
        os.path.join(directorio_resultados, ARCHIVO_RESULTADOS_PYTHON_SEMILLA_2),
        resultado_2.estados,
        modulo,
    )
    comparacion_semillas = Comparador.comparar_semillas(resultado.estados, resultado_2.estados)
    filas_semillas = [
        {
            "indice": indice + 1,
            "x_semilla_1": resultado.estados[indice],
            "x_semilla_2": resultado_2.estados[indice],
            "coincide": resultado.estados[indice] == resultado_2.estados[indice],
        }
        for indice in range(len(resultado.estados))
    ]
    ruta_comparacion_semillas = ExportadorCSV.exportar_comparacion_semillas(
        os.path.join(directorio_resultados, ARCHIVO_COMPARACION_SEMILLAS),
        filas_semillas,
        ["indice", "x_semilla_1", "x_semilla_2", "coincide"],
    )
    print(f"\n[OK] Segunda semilla ({semilla_2}) exportada en: {ruta_semilla_2}")
    print(f"[OK] Comparacion de semillas: {comparacion_semillas.mensaje}")
    print(f"     Exportada en: {ruta_comparacion_semillas}")

    ruta_java = os.path.join(directorio_resultados, ARCHIVO_RESULTADOS_JAVA)
    if ExportadorCSV.archivo_existe(ruta_java):
        filas_java = ExportadorCSV.leer_resultados(ruta_java)
        estados_java = [int(fila["x"]) for fila in filas_java]
        comparacion = Comparador.comparar_secuencias(resultado.estados, estados_java)
        tabla = Comparador.tabla_primeras_observaciones(
            resultado.estados, estados_java, modulo, cantidad=20
        )
        ruta_comparacion = ExportadorCSV.exportar_comparacion(
            os.path.join(directorio_resultados, ARCHIVO_COMPARACION), tabla
        )
        print("\n" + "=" * 78)
        print("COMPARACION PYTHON vs JAVA (primeras 20 observaciones)")
        print("=" * 78)
        print(
            f"{'n':>4} | {'X(n) Python':>14} | {'X(n) Java':>14} | "
            f"{'U(n) Python':>16} | {'U(n) Java':>16} | {'Coincide':>9}"
        )
        print("-" * 88)
        for fila in tabla:
            print(
                f"{fila['indice']:>4} | {fila['x_python']:>14} | {fila['x_java']:>14} | "
                f"{fila['u_python']:>16} | {fila['u_java']:>16} | "
                f"{'SI' if fila['coincide'] else 'NO':>9}"
            )
        print(f"\n{comparacion.mensaje}")
        print(f"Comparacion exportada en: {ruta_comparacion}")
    else:
        print(f"\n[AVISO] No existe '{ruta_java}'; se omite la comparacion entre lenguajes.")

    if generar_graficas:
        generador_graficas = GeneradorGraficas(directorio_graficas)
        graficas = [
            generador_graficas.grafica_secuencia(
                resultado.normalizados,
                nombre_archivo="secuencia_normalizada.png",
                etiqueta_semilla=resultado.semilla,
            ),
            generador_graficas.histograma(
                resultado.normalizados, nombre_archivo="histograma_frecuencias.png"
            ),
            generador_graficas.grafica_comparativa_semillas(
                {resultado.semilla: resultado.normalizados, semilla_2: resultado_2.normalizados},
                nombre_archivo="comparativa_semillas.png",
            ),
        ]
        if ExportadorCSV.archivo_existe(ruta_java):
            graficas.append(
                generador_graficas.grafica_comparativa_python_java(
                    resultado.normalizados,
                    [int(fila["x"]) / modulo for fila in ExportadorCSV.leer_resultados(ruta_java)],
                    nombre_archivo="comparativa_python_java.png",
                )
            )
        print("\n[OK] Graficas generadas:")
        for grafica in graficas:
            print(f"     - {grafica}")


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada principal del programa."""
    argumentos = construir_parser().parse_args(argv)
    configuracion = cargar_configuracion(argumentos)
    servicio = ServicioLCG(configuracion)

    raiz = encontrar_raiz_proyecto()
    resultados = argumentos.salida or directorio_resultados(raiz)
    graficas = directorio_graficas(raiz)

    if argumentos.automatica:
        flujo_automatico(
            servicio,
            resultados,
            graficas,
            semilla_2=argumentos.semilla_2,
            generar_graficas=not argumentos.sin_graficas,
        )
        return 0

    menu = Menu(servicio, resultados, graficas)
    menu.iniciar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
