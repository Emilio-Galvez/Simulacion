package com.simulacion.presentacion;

import com.simulacion.datos.Configuracion;
import com.simulacion.datos.ExportadorCSV;
import com.simulacion.datos.FilaComparacion;
import com.simulacion.servicios.Analisis;
import com.simulacion.servicios.Comparador;
import com.simulacion.servicios.ServicioLCG;

import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Path;
import java.util.List;
import java.util.Scanner;

/**
 * CAPA DE PRESENTACION: menu interactivo del programa Java.
 *
 * <p>El menu interactua con el usuario y coordina el uso de los servicios;
 * no contiene logica de generacion ni de persistencia.</p>
 */
public final class Menu {

    public static final String ARCHIVO_RESULTADOS_JAVA = "resultados_java.csv";
    public static final String ARCHIVO_RESULTADOS_PYTHON = "resultados_python.csv";
    public static final String ARCHIVO_COMPARACION = "comparacion.csv";
    public static final String ARCHIVO_COMPARACION_SEMILLAS = "comparacion_semillas.csv";

    private final ServicioLCG servicio;
    private final Path directorioResultados;
    private final Scanner scanner;
    private final PrintStream salida;

    public Menu(ServicioLCG servicio, Path directorioResultados, Scanner scanner, PrintStream salida) {
        this.servicio = servicio;
        this.directorioResultados = directorioResultados;
        this.scanner = scanner;
        this.salida = salida;
    }

    /**
     * Bucle principal del menu.
     */
    public void iniciar() {
        salida.println("=".repeat(78));
        salida.println("SIMULACION - GENERADOR CONGRUENCIAL LINEAL (LCG)");
        salida.println("Proyecto Practica 5 | Java | Arquitectura en capas");
        salida.println("=".repeat(78));
        while (true) {
            mostrarOpciones();
            String opcion = scanner.nextLine().trim();
            try {
                switch (opcion) {
                    case "1" -> simular(servicio.getConfiguracion().getSemilla(), true);
                    case "2" -> simularConSemillaPersonalizada();
                    case "3" -> compararSemillas();
                    case "4" -> compararPythonJava();
                    case "5" -> analisisPeriodo();
                    case "6" -> generarGraficas();
                    case "7" -> {
                        salida.println("Saliendo del sistema. Hasta pronto.");
                        return;
                    }
                    default -> salida.println("Opcion no valida. Intente nuevamente.");
                }
            } catch (IllegalArgumentException | IOException error) {
                salida.println("[ERROR] " + error.getMessage());
            }
        }
    }

    private void mostrarOpciones() {
        salida.println("\n" + "-".repeat(78));
        salida.println("MENU PRINCIPAL");
        salida.println("-".repeat(78));
        salida.println("1. Ejecutar simulacion con la semilla por defecto (12345)");
        salida.println("2. Ejecutar simulacion con una semilla personalizada");
        salida.println("3. Comparar los resultados obtenidos con dos semillas distintas");
        salida.println("4. Comparar las secuencias de Python y Java (archivos CSV)");
        salida.println("5. Analisis del periodo del generador (Hull-Dobell)");
        salida.println("6. Mostrar el histograma de frecuencias en consola");
        salida.println("7. Salir");
        salida.println("-".repeat(78));
        salida.print("Seleccione una opcion: ");
    }

    /**
     * Ejecuta la simulacion, muestra los resultados y exporta el CSV.
     *
     * @param semilla semilla inicial
     * @param exportar indica si debe exportarse el resultado
     * @throws IOException si falla la escritura del CSV
     */
    public void simular(long semilla, boolean exportar) throws IOException {
        Configuracion configuracion = servicio.getConfiguracion();
        salida.printf("%nEjecutando simulacion: a=%d, c=%d, m=%d, X(0)=%d, n=%d%n",
                configuracion.getMultiplicador(), configuracion.getIncremento(),
                configuracion.getModulo(), semilla, configuracion.getCantidad());
        long[] estados = servicio.simular(semilla);
        Presentacion.imprimirObservaciones("Java", estados, configuracion.getModulo(), 20);
        Presentacion.imprimirEstadisticas(
                Analisis.estadisticas(servicio.simularNormalizados(semilla)));
        if (exportar) {
            Path ruta = ExportadorCSV.exportarResultados(
                    directorioResultados.resolve(ARCHIVO_RESULTADOS_JAVA), estados, configuracion.getModulo());
            salida.println("\nResultados exportados en: " + ruta);
        }
    }

    private void simularConSemillaPersonalizada() throws IOException {
        salida.print("Ingrese la semilla inicial (entero en [0, m)): ");
        long semilla = leerSemilla();
        simular(semilla, true);
    }

    private void compararSemillas() throws IOException {
        salida.println("\nComparacion entre dos semillas distintas");
        salida.print("Semilla de la primera simulacion: ");
        long primera = leerSemilla();
        salida.print("Semilla de la segunda simulacion: ");
        long segunda = leerSemilla();
        long[] estados1 = servicio.simular(primera);
        long[] estados2 = servicio.simular(segunda);
        Comparador.ResultadoComparacion resultado = Comparador.compararSecuencias(estados1, estados2);
        salida.printf("%nSemilla 1 = %d | Semilla 2 = %d%n", primera, segunda);
        salida.println(resultado.mensaje());
        Presentacion.imprimirObservaciones("Semilla " + primera, estados1,
                servicio.getConfiguracion().getModulo(), 10);
        Presentacion.imprimirObservaciones("Semilla " + segunda, estados2,
                servicio.getConfiguracion().getModulo(), 10);
        Path ruta = ExportadorCSV.exportarComparacionSemillas(
                directorioResultados.resolve(ARCHIVO_COMPARACION_SEMILLAS), estados1, estados2);
        salida.println("\nComparacion de semillas exportada en: " + ruta);
    }

    private void compararPythonJava() throws IOException {
        Path rutaPython = directorioResultados.resolve(ARCHIVO_RESULTADOS_PYTHON);
        Path rutaJava = directorioResultados.resolve(ARCHIVO_RESULTADOS_JAVA);
        if (!java.nio.file.Files.isRegularFile(rutaPython)
                || !java.nio.file.Files.isRegularFile(rutaJava)) {
            salida.println("[AVISO] Se requieren 'resultados_python.csv' y 'resultados_java.csv'.");
            salida.println("        Ejecute primero la simulacion en Python y en Java.");
            return;
        }
        Comparador.ResultadoComparacion resultado = Comparador.compararArchivosCsv(rutaPython, rutaJava);
        salida.println("\nComparacion Python vs Java");
        salida.println(resultado.mensaje());
        long[] estadosPython = ExportadorCSV.leerEstados(rutaPython);
        long[] estadosJava = ExportadorCSV.leerEstados(rutaJava);
        List<FilaComparacion> tabla = Comparador.tablaPrimerasObservaciones(
                estadosPython, estadosJava, servicio.getConfiguracion().getModulo(), 20);
        Presentacion.imprimirComparacion(tabla);
        Path ruta = ExportadorCSV.exportarComparacion(directorioResultados.resolve(ARCHIVO_COMPARACION), tabla);
        salida.println("\nComparacion exportada en: " + ruta);
    }

    private void analisisPeriodo() {
        Configuracion configuracion = servicio.getConfiguracion();
        Analisis.ResultadoHullDobell verificacion = Analisis.verificarHullDobell(
                configuracion.getMultiplicador(), configuracion.getIncremento(), configuracion.getModulo());
        salida.println("\nANALISIS DEL PERIODO DEL GENERADOR");
        salida.println("-".repeat(78));
        salida.printf("Parametros: a=%d, c=%d, m=%d%n",
                verificacion.multiplicador(), verificacion.incremento(), verificacion.modulo());
        salida.println("\nCondiciones del teorema de Hull-Dobell:");
        for (Analisis.CondicionHullDobell condicion : verificacion.condiciones()) {
            salida.println("  " + (condicion.cumple() ? "[OK] " : "[FALLA] ") + condicion.descripcion());
            if (!condicion.detalle().isBlank()) {
                salida.println("         " + condicion.detalle());
            }
        }
        salida.println("\nResultado: " + verificacion.resumen());
        salida.println("\nDiferencia entre periodo teorico y cantidad generada:");
        salida.printf("  Periodo teorico (maximo)   : %,d valores%n", verificacion.periodoTeorico());
        salida.printf("  Cantidad generada (practica): %,d valores%n", configuracion.getCantidad());
        salida.printf("  Solo se observa el %.6f%% del ciclo.%n",
                configuracion.getCantidad() * 100.0 / verificacion.periodoTeorico());
        Long periodoEmpirico = Analisis.periodoEmpirico(
                servicio.crearGenerador(null), configuracion.getCantidad());
        if (periodoEmpirico == null) {
            salida.printf("  Periodo empirico: no se detecta repeticion en las %,d muestras; "
                    + "el ciclo es mas largo que la simulacion.%n", configuracion.getCantidad());
        } else {
            salida.printf("  Periodo empirico detectado: %,d%n", periodoEmpirico);
        }
    }

    private void generarGraficas() {
        salida.println("\nLas graficas academicas se generan con Python y Matplotlib");
        salida.println("(comando: python main.py --automatica). En Java se muestra el histograma ASCII:");
        Presentacion.imprimirHistogramaAscii(
                servicio.simularNormalizados(servicio.getConfiguracion().getSemilla()), 20);
    }

    private long leerSemilla() {
        String texto = scanner.nextLine().trim();
        long semilla;
        try {
            semilla = Long.parseLong(texto);
        } catch (NumberFormatException error) {
            throw new IllegalArgumentException(
                    "La semilla '" + texto + "' no es un numero entero valido.");
        }
        long modulo = servicio.getConfiguracion().getModulo();
        if (semilla < 0 || semilla >= modulo) {
            throw new IllegalArgumentException("La semilla debe estar en el intervalo [0, " + modulo + ").");
        }
        return semilla;
    }
}
