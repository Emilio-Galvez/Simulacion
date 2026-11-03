package com.simulacion.datos;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Capa de DATOS: persistencia de resultados en archivos CSV.
 *
 * <p>El formato de intercambio es identico al utilizado por Python:</p>
 *
 * <pre>indice,x,normalizado</pre>
 *
 * <p>El campo {@code normalizado} se calcula con aritmetica entera exacta
 * (BigInteger) para que el texto generado por Java y por Python sea byte a byte
 * identico, evitando las diferencias de redondeo entre {@link String#format}
 * (redondeo al alza) y Python (redondeo al par).</p>
 */
public final class ExportadorCSV {

    public static final String[] ENCABEZADO_RESULTADOS = {"indice", "x", "normalizado"};
    public static final String[] ENCABEZADO_COMPARACION =
            {"indice", "x_python", "x_java", "u_python", "u_java", "coincide"};
    public static final int DECIMALES_NORMALIZADO = 12;

    private ExportadorCSV() {
    }

    /**
     * Exporta una secuencia de estados crudos al formato CSV de resultados.
     *
     * @param ruta  archivo de destino
     * @param estados estados crudos X(n)
     * @param modulo modulo m del generador
     * @return ruta absoluta del archivo generado
     * @throws IOException si no se puede escribir el archivo
     */
    public static Path exportarResultados(Path ruta, long[] estados, long modulo) throws IOException {
        crearDirectorio(ruta);
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write(String.join(",", ENCABEZADO_RESULTADOS));
            escritor.newLine();
            for (int indice = 0; indice < estados.length; indice++) {
                escritor.write(String.format(Locale.ROOT, "%d,%d,%s", indice + 1, estados[indice],
                        formatearNormalizadoExacto(estados[indice], modulo)));
                escritor.newLine();
            }
        }
        return ruta.toAbsolutePath();
    }

    /**
     * Exporta la tabla comparativa Python vs Java a un archivo CSV.
     *
     * @param ruta ruta del archivo de destino
     * @param filas filas de la comparacion
     * @return ruta absoluta del archivo generado
     * @throws IOException si no se puede escribir el archivo
     */
    public static Path exportarComparacion(Path ruta, List<FilaComparacion> filas) throws IOException {
        crearDirectorio(ruta);
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write(String.join(",", ENCABEZADO_COMPARACION));
            escritor.newLine();
            for (FilaComparacion fila : filas) {
                escritor.write(String.format(Locale.ROOT, "%d,%d,%d,%s,%s,%s",
                        fila.indice(), fila.xPython(), fila.xJava(), fila.uPython(), fila.uJava(),
                        fila.coincide() ? "si" : "no"));
                escritor.newLine();
            }
        }
        return ruta.toAbsolutePath();
    }

    /**
     * Exporta la comparacion entre dos semillas a un archivo CSV.
     *
     * @param ruta      ruta del archivo de destino
     * @param estados1  estados de la primera semilla
     * @param estados2  estados de la segunda semilla
     * @return ruta absoluta del archivo generado
     * @throws IOException si no se puede escribir el archivo
     */
    public static Path exportarComparacionSemillas(Path ruta, long[] estados1, long[] estados2) throws IOException {
        crearDirectorio(ruta);
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            escritor.write("indice,x_semilla_1,x_semilla_2,coincide");
            escritor.newLine();
            int total = Math.min(estados1.length, estados2.length);
            for (int indice = 0; indice < total; indice++) {
                escritor.write(String.format(Locale.ROOT, "%d,%d,%d,%s", indice + 1, estados1[indice],
                        estados2[indice], estados1[indice] == estados2[indice] ? "si" : "no"));
                escritor.newLine();
            }
        }
        return ruta.toAbsolutePath();
    }

    /**
     * Lee un CSV de resultados y devuelve la columna de estados crudos.
     *
     * @param ruta archivo de origen
     * @return arreglo con los estados X(n)
     * @throws IOException si no se puede leer el archivo
     */
    public static long[] leerEstados(Path ruta) throws IOException {
        List<Long> estados = new ArrayList<>();
        try (BufferedReader lector = Files.newBufferedReader(ruta, StandardCharsets.UTF_8)) {
            String linea = lector.readLine();
            while ((linea = lector.readLine()) != null) {
                if (linea.isBlank()) {
                    continue;
                }
                String[] campos = linea.split(",");
                estados.add(Long.parseLong(campos[1].trim()));
            }
        }
        long[] arreglo = new long[estados.size()];
        for (int indice = 0; indice < estados.size(); indice++) {
            arreglo[indice] = estados.get(indice);
        }
        return arreglo;
    }

    /**
     * Lee un CSV de resultados y devuelve sus filas como mapas de columnas.
     *
     * @param ruta archivo de origen
     * @return lista de filas
     * @throws IOException si no se puede leer el archivo
     */
    public static List<String[]> leerFilas(Path ruta) throws IOException {
        List<String[]> filas = new ArrayList<>();
        try (BufferedReader lector = Files.newBufferedReader(ruta, StandardCharsets.UTF_8)) {
            lector.readLine();
            String linea;
            while ((linea = lector.readLine()) != null) {
                if (!linea.isBlank()) {
                    filas.add(linea.split(","));
                }
            }
        }
        return filas;
    }

    /**
     * Convierte U(n) = X(n) / m en texto decimal exacto y truncado.
     *
     * @param estado    estado crudo X(n)
     * @param modulo    modulo m
     * @param decimales cantidad de decimales del resultado
     * @return texto decimal con punto como separador
     */
    public static String formatearNormalizadoExacto(long estado, long modulo, int decimales) {
        if (modulo <= 0) {
            throw new IllegalArgumentException("El modulo debe ser positivo.");
        }
        BigInteger escala = BigInteger.TEN.pow(decimales);
        BigInteger escalado = BigInteger.valueOf(estado).multiply(escala)
                .divide(BigInteger.valueOf(modulo));
        BigInteger parteEntera = escalado.divide(escala);
        BigInteger parteDecimal = escalado.subtract(parteEntera.multiply(escala));
        return parteEntera.toString() + "."
                + String.format(Locale.ROOT, "%0" + decimales + "d", parteDecimal);
    }

    /**
     * Convierte U(n) = X(n) / m en texto decimal exacto y truncado con 12 decimales.
     *
     * @param estado estado crudo X(n)
     * @param modulo modulo m
     * @return texto decimal con punto como separador
     */
    public static String formatearNormalizadoExacto(long estado, long modulo) {
        return formatearNormalizadoExacto(estado, modulo, DECIMALES_NORMALIZADO);
    }

    private static void crearDirectorio(Path ruta) throws IOException {
        Path padre = ruta.toAbsolutePath().getParent();
        if (padre != null) {
            Files.createDirectories(padre);
        }
    }
}
