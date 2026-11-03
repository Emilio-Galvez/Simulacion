package com.simulacion.presentacion;

import com.simulacion.datos.FilaComparacion;
import com.simulacion.servicios.Analisis;

import java.util.List;
import java.util.Locale;

/**
 * CAPA DE PRESENTACION: formato de tablas y graficos de texto para la consola.
 */
public final class Presentacion {

    private Presentacion() {
    }

    /**
     * Imprime la tabla de las primeras observaciones de una simulacion.
     *
     * @param etiqueta nombre de la implementacion
     * @param estados  estados generados
     * @param modulo   modulo m del generador
     * @param cantidad numero de filas
     */
    public static void imprimirObservaciones(String etiqueta, long[] estados, long modulo, int cantidad) {
        System.out.printf("%nPrimeras %d observaciones (%s):%n", Math.min(cantidad, estados.length), etiqueta);
        System.out.printf("%4s | %14s | %20s%n", "n", "X(n)", "U(n) = X(n)/m");
        System.out.println("-".repeat(44));
        for (int indice = 0; indice < Math.min(cantidad, estados.length); indice++) {
            System.out.printf("%4d | %14d | %20s%n", indice + 1, estados[indice],
                    com.simulacion.datos.ExportadorCSV.formatearNormalizadoExacto(estados[indice], modulo));
        }
    }

    /**
     * Imprime la tabla comparativa de dos secuencias.
     *
     * @param filas filas de la comparacion
     */
    public static void imprimirComparacion(List<FilaComparacion> filas) {
        System.out.printf("%nPrimeras %d observaciones comparadas:%n", filas.size());
        System.out.printf("%4s | %14s | %14s | %16s | %16s | %9s%n",
                "n", "X(n) Python", "X(n) Java", "U(n) Python", "U(n) Java", "Coincide");
        System.out.println("-".repeat(88));
        for (FilaComparacion fila : filas) {
            System.out.printf("%4d | %14d | %14d | %16s | %16s | %9s%n",
                    fila.indice(), fila.xPython(), fila.xJava(), fila.uPython(), fila.uJava(),
                    fila.coincide() ? "SI" : "NO");
        }
    }

    /**
     * Imprime un histograma de texto con las frecuencias por intervalo.
     *
     * @param valores valores normalizados
     * @param bins    cantidad de intervalos
     */
    public static void imprimirHistogramaAscii(double[] valores, int bins) {
        int[] frecuencias = new int[bins];
        for (double valor : valores) {
            int indice = (int) Math.min(Math.floor(valor * bins), bins - 1);
            frecuencias[indice]++;
        }
        int maxima = 0;
        for (int frecuencia : frecuencias) {
            maxima = Math.max(maxima, frecuencia);
        }
        System.out.printf("%nHistograma de frecuencias (%d intervalos):%n", bins);
        for (int indice = 0; indice < bins; indice++) {
            int longitud = maxima == 0 ? 0 : (int) Math.round(40.0 * frecuencias[indice] / maxima);
            System.out.printf("[%.2f, %.2f) %6d | %s%n",
                    (double) indice / bins, (double) (indice + 1) / bins, frecuencias[indice],
                    "#".repeat(longitud));
        }
    }

    /**
     * Imprime las estadisticas descriptivas de una simulacion.
     *
     * @param estadisticas estadisticas calculadas
     */
    public static void imprimirEstadisticas(Analisis.Estadisticas estadisticas) {
        System.out.println("\nEstadisticas descriptivas de los valores normalizados:");
        System.out.printf(Locale.ROOT, "  Cantidad      : %,d%n", estadisticas.cantidad());
        System.out.printf(Locale.ROOT, "  Minimo        : %.12f%n", estadisticas.minimo());
        System.out.printf(Locale.ROOT, "  Maximo        : %.12f%n", estadisticas.maximo());
        System.out.printf(Locale.ROOT, "  Media         : %.12f  (teorico 0.5)%n", estadisticas.media());
        System.out.printf(Locale.ROOT, "  Varianza      : %.12f  (teorico 0.083333333333)%n", estadisticas.varianza());
        System.out.printf(Locale.ROOT, "  Desv. estandar: %.12f%n", estadisticas.desviacionEstandar());
    }
}
