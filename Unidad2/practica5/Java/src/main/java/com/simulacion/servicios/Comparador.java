package com.simulacion.servicios;

import com.simulacion.datos.ExportadorCSV;
import com.simulacion.datos.FilaComparacion;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Servicio de comparacion entre secuencias pseudoaleatorias.
 *
 * <p>Permite comparar la secuencia generada por Java con la generada por Python
 * a traves del archivo CSV de intercambio.</p>
 */
public final class Comparador {

    /** Diferencia detectada entre dos secuencias. */
    public record Diferencia(int indice, Long valorIzquierdo, Long valorDerecho) {
        @Override
        public String toString() {
            return "indice " + indice + ": " + valorIzquierdo + " != " + valorDerecho;
        }
    }

    /** Resultado de comparar dos secuencias de estados crudos X(n). */
    public record ResultadoComparacion(boolean identicas, int totalComparadas, int longitudIzquierda,
                                       int longitudDerecha, List<Diferencia> diferencias,
                                       Integer totalDiferencias) {

        public String mensaje() {
            if (identicas) {
                return "SECUENCIAS IDENTICAS: las " + totalComparadas
                        + " observaciones comparadas coinciden exactamente.";
            }
            String detalle = diferencias.isEmpty() ? "sin detalle" : diferencias.get(0).toString();
            return "SECUENCIAS DIFERENTES: " + totalDiferencias
                    + " diferencia(s) detectada(s). Primera: " + detalle + ".";
        }
    }

    private Comparador() {
    }

    /**
     * Compara dos secuencias de estados crudos elemento a elemento.
     *
     * @param izquierda primera secuencia
     * @param derecha   segunda secuencia
     * @return resultado de la comparacion
     */
    public static ResultadoComparacion compararSecuencias(long[] izquierda, long[] derecha) {
        int total = Math.min(izquierda.length, derecha.length);
        List<Diferencia> diferencias = new ArrayList<>();
        int totalDiferencias = 0;
        for (int indice = 0; indice < total; indice++) {
            if (izquierda[indice] != derecha[indice]) {
                totalDiferencias++;
                if (diferencias.size() < 20) {
                    diferencias.add(new Diferencia(indice, izquierda[indice], derecha[indice]));
                }
            }
        }
        boolean identicas = izquierda.length == derecha.length && totalDiferencias == 0;
        return new ResultadoComparacion(identicas, total, izquierda.length, derecha.length,
                List.copyOf(diferencias), totalDiferencias);
    }

    /**
     * Compara dos archivos CSV de resultados con la misma estructura.
     *
     * @param rutaIzquierda ruta del primer CSV
     * @param rutaDerecha   ruta del segundo CSV
     * @return resultado de la comparacion
     * @throws IOException si no se puede leer algun archivo
     */
    public static ResultadoComparacion compararArchivosCsv(Path rutaIzquierda, Path rutaDerecha) throws IOException {
        long[] estadosIzquierda = ExportadorCSV.leerEstados(rutaIzquierda);
        long[] estadosDerecha = ExportadorCSV.leerEstados(rutaDerecha);
        return compararSecuencias(estadosIzquierda, estadosDerecha);
    }

    /**
     * Construye la tabla comparativa de las primeras observaciones.
     *
     * @param izquierda  estados de la primera secuencia
     * @param derecha    estados de la segunda secuencia
     * @param modulo     modulo m del generador
     * @param cantidad   cantidad de filas
     * @return lista de filas comparativas
     */
    public static List<FilaComparacion> tablaPrimerasObservaciones(long[] izquierda, long[] derecha,
                                                                     long modulo, int cantidad) {
        List<FilaComparacion> filas = new ArrayList<>();
        int total = Math.min(cantidad, Math.min(izquierda.length, derecha.length));
        for (int indice = 0; indice < total; indice++) {
            filas.add(new FilaComparacion(
                    indice + 1,
                    izquierda[indice],
                    derecha[indice],
                    ExportadorCSV.formatearNormalizadoExacto(izquierda[indice], modulo),
                    ExportadorCSV.formatearNormalizadoExacto(derecha[indice], modulo),
                    izquierda[indice] == derecha[indice]));
        }
        return List.copyOf(filas);
    }
}
