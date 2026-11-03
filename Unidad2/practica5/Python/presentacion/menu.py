"""Capa de PRESENTACION: menu interactivo y tablas de resultados.

El menu solo orquesta la interaccion con el usuario: toda la logica de
negocio reside en los servicios y toda la persistencia en la capa de datos.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence

from datos.exportador_csv import ExportadorCSV, formatear_normalizado_exacto
from generador_lcg import ServicioLCG
from servicios.analisis import Analisis
from servicios.comparador import Comparador

ARCHIVO_RESULTADOS_PYTHON = "resultados_python.csv"
ARCHIVO_RESULTADOS_JAVA = "resultados_java.csv"
ARCHIVO_COMPARACION = "comparacion.csv"
ARCHIVO_COMPARACION_SEMILLAS = "comparacion_semillas.csv"


class Menu:
    """Menu interactivo de la aplicacion de simulacion LCG."""

    def __init__(
        self,
        servicio: ServicioLCG,
        directorio_resultados: str,
        directorio_graficas: str,
        lector: Callable[[str], str] | None = None,
    ) -> None:
        self._servicio = servicio
        self._directorio_resultados = directorio_resultados
        self._directorio_graficas = directorio_graficas
        self._leer = lector or input
        os.makedirs(self._directorio_resultados, exist_ok=True)
        os.makedirs(self._directorio_graficas, exist_ok=True)

    def iniciar(self) -> None:
        """Bucle principal del menu."""
        print("=" * 78)
        print("SIMULACION - GENERADOR CONGRUENCIAL LINEAL (LCG)")
        print("Proyecto Practica 5 | Python | Arquitectura en capas")
        print("=" * 78)
        while True:
            self._mostrar_opciones()
            opcion = self._pedir_opcion()
            try:
                if opcion == "1":
                    self.opcion_simular(self._servicio.configuracion.semilla)
                elif opcion == "2":
                    self.opcion_simular_con_semilla_personalizada()
                elif opcion == "3":
                    self.opcion_comparar_semillas()
                elif opcion == "4":
                    self.opcion_comparar_python_java()
                elif opcion == "5":
                    self.opcion_analisis_periodo()
                elif opcion == "6":
                    self.opcion_generar_graficas()
                elif opcion == "7":
                    print("Saliendo del sistema. Hasta pronto.")
                    return
                else:
                    print("Opcion no valida. Intente nuevamente.")
            except (ValueError, OSError) as error:
                print(f"[ERROR] {error}")
            except KeyboardInterrupt:
                print("\nEjecucion interrumpida por el usuario.")
                return

    def _mostrar_opciones(self) -> None:
        print("\n" + "-" * 78)
        print("MENU PRINCIPAL")
        print("-" * 78)
        print("1. Ejecutar simulacion con la semilla por defecto (12345)")
        print("2. Ejecutar simulacion con una semilla personalizada")
        print("3. Comparar los resultados obtenidos con dos semillas distintas")
        print("4. Comparar las secuencias de Python y Java (archivos CSV)")
        print("5. Analisis del periodo del generador (Hull-Dobell)")
        print("6. Generar las graficas de la simulacion")
        print("7. Salir")
        print("-" * 78)

    def _pedir_opcion(self) -> str:
        return self._leer("Seleccione una opcion: ").strip()

    def opcion_simular(self, semilla: int, exportar: bool = True) -> None:
        """Ejecuta la simulacion, muestra resultados y exporta el CSV."""
        configuracion = self._servicio.configuracion
        print(
            f"\nEjecutando simulacion: a={configuracion.multiplicador}, "
            f"c={configuracion.incremento}, m={configuracion.modulo}, "
            f"X(0)={semilla}, n={configuracion.cantidad}"
        )
        resultado = self._servicio.simular(semilla)
        self._mostrar_tabla_observaciones(resultado.estados, configuracion.modulo, semilla)
        self._mostrar_estadisticas(resultado.estadisticas)
        if exportar:
            ruta = ExportadorCSV.exportar_resultados(
                os.path.join(self._directorio_resultados, ARCHIVO_RESULTADOS_PYTHON),
                resultado.estados,
                configuracion.modulo,
            )
            print(f"\nResultados exportados en: {ruta}")

    def opcion_simular_con_semilla_personalizada(self) -> None:
        """Solicita una semilla y ejecuta la simulacion con ella."""
        entrada = self._leer("Ingrese la semilla inicial (entero en [0, m)): ").strip()
        try:
            semilla = int(entrada)
        except ValueError as error:
            raise ValueError(f"La semilla '{entrada}' no es un numero entero valido.") from error
        self.opcion_simular(semilla)

    def opcion_comparar_semillas(self) -> None:
        """Compara dos simulaciones realizadas con semillas distintas."""
        print("\nComparacion entre dos semillas distintas")
        primera = self._pedir_semilla("Semilla de la primera simulacion: ")
        segunda = self._pedir_semilla("Semilla de la segunda simulacion: ")
        simulacion_1 = self._servicio.simular(primera)
        simulacion_2 = self._servicio.simular(segunda)
        resultado = Comparador.comparar_semillas(simulacion_1.estados, simulacion_2.estados)
        print(f"\nSemilla 1 = {primera} | Semilla 2 = {segunda}")
        print(resultado.mensaje)
        print("\nPrimeras 10 observaciones de cada semilla:")
        print(
            f"{'n':>4} | {'X(n) semilla 1':>16} | {'U(n) semilla 1':>16} | "
            f"{'X(n) semilla 2':>16} | {'U(n) semilla 2':>16}"
        )
        print("-" * 86)
        for indice in range(min(10, len(simulacion_1.estados), len(simulacion_2.estados))):
            x1 = simulacion_1.estados[indice]
            x2 = simulacion_2.estados[indice]
            print(
                f"{indice + 1:>4} | {x1:>16} | "
                f"{formatear_normalizado_exacto(x1, self._servicio.configuracion.modulo):>16} | "
                f"{x2:>16} | "
                f"{formatear_normalizado_exacto(x2, self._servicio.configuracion.modulo):>16}"
            )
        filas = [
            {
                "indice": indice + 1,
                "x_semilla_1": simulacion_1.estados[indice],
                "x_semilla_2": simulacion_2.estados[indice],
                "coincide": simulacion_1.estados[indice] == simulacion_2.estados[indice],
            }
            for indice in range(len(simulacion_1.estados))
        ]
        ruta = ExportadorCSV.exportar_comparacion_semillas(
            os.path.join(self._directorio_resultados, ARCHIVO_COMPARACION_SEMILLAS),
            filas,
            ["indice", "x_semilla_1", "x_semilla_2", "coincide"],
        )
        print(f"\nComparacion de semillas exportada en: {ruta}")

    def opcion_comparar_python_java(self) -> None:
        """Compara los CSV generados por Python y por Java."""
        ruta_python = os.path.join(self._directorio_resultados, ARCHIVO_RESULTADOS_PYTHON)
        ruta_java = os.path.join(self._directorio_resultados, ARCHIVO_RESULTADOS_JAVA)
        if not (
            ExportadorCSV.archivo_existe(ruta_python) and ExportadorCSV.archivo_existe(ruta_java)
        ):
            print("[AVISO] Se requieren 'resultados_python.csv' y 'resultados_java.csv'.")
            print("        Ejecute primero la simulacion en Python y en Java.")
            return
        resultado = Comparador.comparar_archivos_csv(ruta_python, ruta_java)
        print("\nComparacion Python vs Java")
        print(resultado.mensaje)
        filas_python = ExportadorCSV.leer_resultados(ruta_python)
        filas_java = ExportadorCSV.leer_resultados(ruta_java)
        modulo = self._servicio.configuracion.modulo
        tabla = Comparador.tabla_primeras_observaciones(
            [int(fila["x"]) for fila in filas_python],
            [int(fila["x"]) for fila in filas_java],
            modulo,
            cantidad=20,
        )
        self._mostrar_tabla_comparativa(tabla)
        ExportadorCSV.exportar_comparacion(
            os.path.join(self._directorio_resultados, ARCHIVO_COMPARACION), tabla
        )
        print(
            f"\nComparacion exportada en: "
            f"{os.path.join(self._directorio_resultados, ARCHIVO_COMPARACION)}"
        )

    def opcion_analisis_periodo(self) -> None:
        """Muestra el analisis teorico (Hull-Dobell) y empirico del periodo."""
        configuracion = self._servicio.configuracion
        verificacion = Analisis.verificar_hull_dobell(
            configuracion.multiplicador, configuracion.incremento, configuracion.modulo
        )
        print("\nANALISIS DEL PERIODO DEL GENERADOR")
        print("-" * 78)
        print(
            f"Parametros: a={verificacion.multiplicador}, c={verificacion.incremento}, "
            f"m={verificacion.modulo} (2^{_exponente_de_2(verificacion.modulo)})"
        )
        print("\nCondiciones del teorema de Hull-Dobell:")
        for condicion in verificacion.condiciones:
            marca = "[OK] " if condicion.cumple else "[FALLA]"
            print(f"  {marca} {condicion.descripcion}")
            if condicion.detalle:
                print(f"         {condicion.detalle}")
        print(f"\nResultado: {verificacion.resumen}")
        print("\nDiferencia entre periodo teorico y cantidad generada:")
        print(f"  Periodo teorico (maximo)  : {verificacion.periodo_teorico:,} valores")
        print(f"  Cantidad generada (practica): {configuracion.cantidad:,} valores")
        print(
            "  Solo se observa el "
            f"{configuracion.cantidad / verificacion.periodo_teorico * 100:.6f}% del ciclo."
        )
        generador = self._servicio.crear_generador()
        periodo_empirico = Analisis.periodo_empirico(generador, limite=configuracion.cantidad)
        if periodo_empirico is None:
            print(
                f"  Periodo empirico: no se detecta repeticion en las {configuracion.cantidad:,} "
                "muestras; el ciclo es mas largo que la simulacion."
            )
        else:
            print(f"  Periodo empirico detectado: {periodo_empirico:,}")

    def opcion_generar_graficas(self) -> None:
        """Genera las tres graficas requeridas por la practica."""
        from presentacion.graficas import GeneradorGraficas

        generador_graficas = GeneradorGraficas(self._directorio_graficas)
        configuracion = self._servicio.configuracion
        resultado = self._servicio.simular()
        archivos = [
            generador_graficas.grafica_secuencia(
                resultado.normalizados,
                nombre_archivo="secuencia_normalizada.png",
                etiqueta_semilla=resultado.semilla,
            ),
            generador_graficas.histograma(
                resultado.normalizados, nombre_archivo="histograma_frecuencias.png"
            ),
        ]
        segunda_semilla = 54321
        resultado_2 = self._servicio.simular(segunda_semilla)
        archivos.append(
            generador_graficas.grafica_comparativa_semillas(
                {
                    resultado.semilla: resultado.normalizados,
                    segunda_semilla: resultado_2.normalizados,
                },
                nombre_archivo="comparativa_semillas.png",
            )
        )
        ruta_java = os.path.join(self._directorio_resultados, ARCHIVO_RESULTADOS_JAVA)
        if ExportadorCSV.archivo_existe(ruta_java):
            filas_java = ExportadorCSV.leer_resultados(ruta_java)
            archivos.append(
                generador_graficas.grafica_comparativa_python_java(
                    resultado.normalizados,
                    [int(fila["x"]) / self._servicio.configuracion.modulo for fila in filas_java],
                    nombre_archivo="comparativa_python_java.png",
                )
            )
        print("\nGraficas generadas:")
        for archivo in archivos:
            print(f"  - {archivo}")
        print(
            f"Configuracion: {configuracion.multiplicador=}, {configuracion.incremento=}, "
            f"{configuracion.modulo=}, {configuracion.semilla=}, {configuracion.cantidad=}"
        )

    def _pedir_semilla(self, mensaje: str) -> int:
        entrada = self._leer(mensaje).strip()
        try:
            semilla = int(entrada)
        except ValueError as error:
            raise ValueError(f"La semilla '{entrada}' no es un numero entero valido.") from error
        if not 0 <= semilla < self._servicio.configuracion.modulo:
            raise ValueError(
                f"La semilla debe estar en el intervalo [0, {self._servicio.configuracion.modulo})."
            )
        return semilla

    def _mostrar_tabla_observaciones(
        self, estados: Sequence[int], modulo: int, semilla: int, cantidad: int = 20
    ) -> None:
        print(f"\nPrimeras {cantidad} observaciones (semilla X(0) = {semilla}):")
        print(f"{'n':>4} | {'X(n)':>12} | {'U(n) = X(n)/m':>18}")
        print("-" * 40)
        for indice, estado in enumerate(estados[:cantidad], start=1):
            print(
                f"{indice:>4} | {estado:>12} | {formatear_normalizado_exacto(estado, modulo):>18}"
            )

    def _mostrar_tabla_comparativa(self, filas: list[dict[str, object]]) -> None:
        print(f"\nPrimeras {len(filas)} observaciones comparadas:")
        print(
            f"{'n':>4} | {'X(n) Python':>14} | {'X(n) Java':>14} | "
            f"{'U(n) Python':>16} | {'U(n) Java':>16} | {'Coincide':>9}"
        )
        print("-" * 88)
        for fila in filas:
            print(
                f"{fila['indice']:>4} | {fila['x_python']:>14} | {fila['x_java']:>14} | "
                f"{fila['u_python']:>16} | {fila['u_java']:>16} | "
                f"{'SI' if fila['coincide'] else 'NO':>9}"
            )

    def _mostrar_estadisticas(self, estadisticas: dict[str, float]) -> None:
        print("\nEstadisticas descriptivas de los valores normalizados:")
        print(f"  Cantidad      : {int(estadisticas['cantidad']):,}")
        print(f"  Minimo        : {estadisticas['minimo']:.12f}")
        print(f"  Maximo        : {estadisticas['maximo']:.12f}")
        print(f"  Media         : {estadisticas['media']:.12f}  (teorico 0.5)")
        print(f"  Varianza      : {estadisticas['varianza']:.12f}  (teorico 0.083333333333)")
        print(f"  Desv. estandar: {estadisticas['desviacion_estandar']:.12f}")


def _exponente_de_2(numero: int) -> int:
    """Devuelve el exponente k tal que numero = 2^k (o 0 si no es potencia de dos)."""
    if numero <= 0 or numero & (numero - 1) != 0:
        return 0
    return numero.bit_length() - 1
