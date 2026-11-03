package com.simulacion;

import com.simulacion.datos.Configuracion;
import com.simulacion.datos.ExportadorCSV;
import com.simulacion.datos.FilaComparacion;
import com.simulacion.datos.RutasProyecto;
import com.simulacion.presentacion.Menu;
import com.simulacion.presentacion.Presentacion;
import com.simulacion.servicios.Analisis;
import com.simulacion.servicios.Comparador;
import com.simulacion.servicios.ServicioLCG;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Scanner;

/**
 * Punto de entrada de la implementacion en Java del Generador LCG.
 *
 * <p>Uso rapido:</p>
 * <pre>
 * java -cp target/classes com.simulacion.Main                # menu interactivo
 * java -cp target/classes com.simulacion.Main --automatica   # flujo completo
 * </pre>
 */
public final class Main {

    public static final String ARCHIVO_RESULTADOS_JAVA = "resultados_java.csv";
    public static final String ARCHIVO_RESULTADOS_JAVA_SEMILLA_2 = "resultados_java_semilla_2.csv";
    public static final String ARCHIVO_RESULTADOS_PYTHON = "resultados_python.csv";
    public static final String ARCHIVO_COMPARACION = "comparacion.csv";
    public static final String ARCHIVO_COMPARACION_SEMILLAS = "comparacion_semillas.csv";
    public static final long SEMILLA_ALTERNATIVA = 54321L;

    private Main() {
    }

    public static void main(String[] argumentos) throws IOException {
        Argumentos opciones = Argumentos.leer(argumentos);
        Path raiz = RutasProyecto.encontrarRaizProyecto();
        Configuracion configuracion = Configuracion.desdeArchivo(RutasProyecto.rutaConfiguracion(raiz));
        if (opciones.semilla != null) {
            configuracion = configuracion.conSemilla(opciones.semilla);
        }
        if (opciones.cantidad != null) {
            configuracion = configuracion.conCantidad(opciones.cantidad);
        }
        configuracion.validar();

        ServicioLCG servicio = new ServicioLCG(configuracion);
        Path resultados = opciones.salida != null ? opciones.salida : RutasProyecto.directorioResultados(raiz);

        if (opciones.automatica) {
            flujoAutomatico(servicio, resultados, opciones.semilla2);
            return;
        }

        try (Scanner scanner = new Scanner(System.in)) {
            Menu menu = new Menu(servicio, resultados, scanner, System.out);
            menu.iniciar();
        }
    }

    /**
     * Ejecuta el flujo completo de la practica de forma no interactiva.
     *
     * @param servicio servicio de dominio
     * @param resultados carpeta de salida
     * @param semilla2 segunda semilla para la comparacion
     * @throws IOException si falla la escritura de los archivos
     */
    private static void flujoAutomatico(ServicioLCG servicio, Path resultados, long semilla2)
            throws IOException {
        Configuracion configuracion = servicio.getConfiguracion();
        long modulo = configuracion.getModulo();

        System.out.println("=".repeat(78));
        System.out.println("SIMULACION LCG - EJECUCION AUTOMATICA (JAVA)");
        System.out.println("=".repeat(78));
        System.out.printf("a = %d | c = %d | m = %d | X(0) = %d | n = %d%n",
                configuracion.getMultiplicador(), configuracion.getIncremento(), modulo,
                configuracion.getSemilla(), configuracion.getCantidad());

        long[] estados = servicio.simular(null);
        Path rutaJava = ExportadorCSV.exportarResultados(
                resultados.resolve(ARCHIVO_RESULTADOS_JAVA), estados, modulo);
        System.out.printf("%n[OK] %,d valores generados y exportados en: %s%n",
                estados.length, rutaJava);
        Presentacion.imprimirObservaciones("Java", estados, modulo, 20);

        double[] normalizados = servicio.simularNormalizados(null);
        Presentacion.imprimirEstadisticas(Analisis.estadisticas(normalizados));

        Analisis.ResultadoChiCuadrado chiCuadrado = Analisis.pruebaChiCuadrado(normalizados, 20, 0.95);
        System.out.println("\nPrueba de uniformidad chi-cuadrado (20 intervalos, 95%):");
        System.out.printf("  Estadistico X2 = %.4f | Valor critico = %.4f | Conclusion: %s%n",
                chiCuadrado.estadistico(), chiCuadrado.valorCritico(),
                chiCuadrado.rechazaHipotesis() ? "se rechaza la uniformidad"
                        : "no se rechaza la uniformidad");

        Analisis.ResultadoHullDobell verificacion = Analisis.verificarHullDobell(
                configuracion.getMultiplicador(), configuracion.getIncremento(), modulo);
        System.out.println("\nAnalisis del periodo (Hull-Dobell):");
        for (Analisis.CondicionHullDobell condicion : verificacion.condiciones()) {
            System.out.println("  " + (condicion.cumple() ? "[OK] " : "[FALLA] ")
                    + condicion.descripcion());
        }
        System.out.println("  " + verificacion.resumen());
        System.out.printf("  Se generan %,d valores de un ciclo teorico de %,d (%.6f%%).%n",
                configuracion.getCantidad(), verificacion.periodoTeorico(),
                configuracion.getCantidad() * 100.0 / verificacion.periodoTeorico());

        long[] estadosSemilla2 = servicio.simular(semilla2);
        Path rutaSemilla2 = ExportadorCSV.exportarResultados(
                resultados.resolve(ARCHIVO_RESULTADOS_JAVA_SEMILLA_2), estadosSemilla2, modulo);
        Comparador.ResultadoComparacion comparacionSemillas =
                Comparador.compararSecuencias(estados, estadosSemilla2);
        Path rutaComparacionSemillas = ExportadorCSV.exportarComparacionSemillas(
                resultados.resolve(ARCHIVO_COMPARACION_SEMILLAS), estados, estadosSemilla2);
        System.out.printf("%n[OK] Segunda semilla (%d) exportada en: %s%n", semilla2, rutaSemilla2);
        System.out.println("[OK] Comparacion de semillas: " + comparacionSemillas.mensaje());
        System.out.println("     Exportada en: " + rutaComparacionSemillas);

        Path rutaPython = resultados.resolve(ARCHIVO_RESULTADOS_PYTHON);
        if (Files.isRegularFile(rutaPython)) {
            long[] estadosPython = ExportadorCSV.leerEstados(rutaPython);
            Comparador.ResultadoComparacion comparacion =
                    Comparador.compararSecuencias(estadosPython, estados);
            List<FilaComparacion> tabla = Comparador.tablaPrimerasObservaciones(
                    estadosPython, estados, modulo, 20);
            Path rutaComparacion = ExportadorCSV.exportarComparacion(
                    resultados.resolve(ARCHIVO_COMPARACION), tabla);
            System.out.println("\n" + "=".repeat(78));
            System.out.println("COMPARACION PYTHON vs JAVA (primeras 20 observaciones)");
            System.out.println("=".repeat(78));
            Presentacion.imprimirComparacion(tabla);
            System.out.println("\n" + comparacion.mensaje());
            System.out.println("Comparacion exportada en: " + rutaComparacion);
        } else {
            System.out.printf("%n[AVISO] No existe '%s'; se omite la comparacion entre lenguajes.%n",
                    rutaPython);
        }
    }

    /** Opciones de linea de comandos del programa. */
    private record Argumentos(boolean automatica, Long semilla, Integer cantidad, Long semilla2, Path salida) {

        static Argumentos leer(String[] argumentos) {
            boolean automatica = false;
            Long semilla = null;
            Integer cantidad = null;
            Long semilla2 = SEMILLA_ALTERNATIVA;
            Path salida = null;
            for (int indice = 0; indice < argumentos.length; indice++) {
                switch (argumentos[indice]) {
                    case "--automatica" -> automatica = true;
                    case "--semilla" -> semilla = Long.parseLong(argumentos[++indice]);
                    case "--cantidad" -> cantidad = Integer.parseInt(argumentos[++indice]);
                    case "--semilla-2" -> semilla2 = Long.parseLong(argumentos[++indice]);
                    case "--salida" -> salida = Path.of(argumentos[++indice]);
                    default -> throw new IllegalArgumentException(
                            "Argumento desconocido: " + argumentos[indice]);
                }
            }
            return new Argumentos(automatica, semilla, cantidad, semilla2, salida);
        }
    }
}
