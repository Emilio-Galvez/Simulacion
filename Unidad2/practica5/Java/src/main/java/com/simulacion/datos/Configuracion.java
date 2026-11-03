package com.simulacion.datos;

import com.simulacion.estrategias.ParametrosGenerador;
import com.simulacion.estrategias.ParametrosInvalidosException;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Capa de DATOS: lectura de la configuracion de la simulacion.
 *
 * <p>La configuracion se guarda en un archivo INI ({@code configuracion.ini})
 * con una seccion {@code [lcg]}, legible tanto por Java como por Python, de modo
 * que ambos programas compartan los mismos parametros matematicos.</p>
 */
public final class Configuracion {

    private static final String SECCION = "lcg";

    private final long multiplicador;
    private final long incremento;
    private final long modulo;
    private final long semilla;
    private final int cantidad;

    public Configuracion(long multiplicador, long incremento, long modulo, long semilla, int cantidad) {
        this.multiplicador = multiplicador;
        this.incremento = incremento;
        this.modulo = modulo;
        this.semilla = semilla;
        this.cantidad = cantidad;
        validar();
    }

    /**
     * Configuracion con los parametros obligatorios de la practica.
     *
     * @return configuracion por defecto
     */
    public static Configuracion porDefecto() {
        ParametrosGenerador parametros = ParametrosGenerador.porDefecto();
        return new Configuracion(parametros.multiplicador(), parametros.incremento(),
                parametros.modulo(), parametros.semilla(), 10000);
    }

    /**
     * Lee la configuracion desde un archivo INI; si no existe, usa los valores por defecto.
     *
     * @param ruta archivo de configuracion
     * @return configuracion leida
     * @throws IOException si el archivo existe pero no se puede leer
     */
    public static Configuracion desdeArchivo(Path ruta) throws IOException {
        if (ruta == null || !Files.isRegularFile(ruta)) {
            return porDefecto();
        }
        Map<String, String> valores = leerSeccion(ruta, SECCION);
        Configuracion porDefecto = porDefecto();
        return new Configuracion(
                valorLong(valores, "multiplicador", porDefecto.multiplicador),
                valorLong(valores, "incremento", porDefecto.incremento),
                valorLong(valores, "modulo", porDefecto.modulo),
                valorLong(valores, "semilla", porDefecto.semilla),
                (int) valorLong(valores, "cantidad", porDefecto.cantidad));
    }

    private static Map<String, String> leerSeccion(Path ruta, String seccion) throws IOException {
        Map<String, String> valores = new LinkedHashMap<>();
        boolean dentroDeSeccion = false;
        for (String linea : Files.readAllLines(ruta, StandardCharsets.UTF_8)) {
            String limpia = linea.trim();
            if (limpia.isEmpty() || limpia.startsWith("#") || limpia.startsWith(";")) {
                continue;
            }
            if (limpia.startsWith("[") && limpia.endsWith("]")) {
                dentroDeSeccion = limpia.substring(1, limpia.length() - 1).trim().equals(seccion);
                continue;
            }
            if (!dentroDeSeccion) {
                continue;
            }
            int separador = limpia.indexOf('=');
            if (separador > 0) {
                valores.put(limpia.substring(0, separador).trim().toLowerCase(),
                        limpia.substring(separador + 1).trim());
            }
        }
        return valores;
    }

    private static long valorLong(Map<String, String> valores, String clave, long porDefecto) {
        String texto = valores.get(clave);
        if (texto == null || texto.isBlank()) {
            return porDefecto;
        }
        try {
            return Long.parseLong(texto);
        } catch (NumberFormatException error) {
            throw new ParametrosInvalidosException(
                    "El valor de '" + clave + "' no es un entero valido: " + texto);
        }
    }

    /** Valida los parametros matematicos de la simulacion. */
    public void validar() {
        if (multiplicador <= 0) {
            throw new ParametrosInvalidosException("El multiplicador a debe ser mayor que cero.");
        }
        if (modulo <= 1) {
            throw new ParametrosInvalidosException("El modulo m debe ser mayor que uno.");
        }
        if (incremento < 0 || incremento >= modulo) {
            throw new ParametrosInvalidosException("El incremento c debe cumplir 0 <= c < m.");
        }
        if (semilla < 0 || semilla >= modulo) {
            throw new ParametrosInvalidosException("La semilla debe cumplir 0 <= X(0) < m.");
        }
        if (cantidad <= 0) {
            throw new ParametrosInvalidosException("La cantidad de numeros debe ser mayor que cero.");
        }
    }

    /**
     * Devuelve una copia de la configuracion con otra semilla inicial.
     *
     * @param nuevaSemilla semilla a utilizar
     * @return nueva configuracion
     */
    public Configuracion conSemilla(long nuevaSemilla) {
        return new Configuracion(multiplicador, incremento, modulo, nuevaSemilla, cantidad);
    }

    /**
     * Devuelve una copia de la configuracion con otra cantidad de valores.
     *
     * @param nuevaCantidad cantidad a generar
     * @return nueva configuracion
     */
    public Configuracion conCantidad(int nuevaCantidad) {
        return new Configuracion(multiplicador, incremento, modulo, semilla, nuevaCantidad);
    }

    public long getMultiplicador() {
        return multiplicador;
    }

    public long getIncremento() {
        return incremento;
    }

    public long getModulo() {
        return modulo;
    }

    public long getSemilla() {
        return semilla;
    }

    public int getCantidad() {
        return cantidad;
    }
}
