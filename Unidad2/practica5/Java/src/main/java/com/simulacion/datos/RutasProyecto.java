package com.simulacion.datos;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Utilidad de la capa de DATOS para localizar la raiz del proyecto.
 *
 * <p>Permite que el programa funcione independientemente del directorio de
 * trabajo desde el que se ejecute, localizando la carpeta que contiene los
 * modulos {@code Python}, {@code Java} y {@code Resultados}.</p>
 */
public final class RutasProyecto {

    public static final String NOMBRE_RESULTADOS = "Resultados";
    public static final String NOMBRE_GRAFICAS = "graficas";
    public static final String ARCHIVO_CONFIGURACION = "configuracion.ini";

    private static final String[] NOMBRES_RAIZ = {"Python", "Java"};

    private RutasProyecto() {
    }

    /**
     * Busca la raiz del proyecto subiendo directorios hasta el sistema de archivos.
     *
     * @return ruta absoluta de la raiz del proyecto
     */
    public static Path encontrarRaizProyecto() {
        Path actual = Paths.get(System.getProperty("user.dir")).toAbsolutePath();
        while (actual != null) {
            boolean completa = true;
            for (String nombre : NOMBRES_RAIZ) {
                if (!Files.isDirectory(actual.resolve(nombre))) {
                    completa = false;
                    break;
                }
            }
            if (completa) {
                return actual;
            }
            actual = actual.getParent();
        }
        return Paths.get(System.getProperty("user.dir")).toAbsolutePath();
    }

    /**
     * @param raiz raiz del proyecto
     * @return ruta de la carpeta de resultados
     */
    public static Path directorioResultados(Path raiz) {
        return raiz.resolve(NOMBRE_RESULTADOS);
    }

    /**
     * @param raiz raiz del proyecto
     * @return ruta de la carpeta de graficas
     */
    public static Path directorioGraficas(Path raiz) {
        return directorioResultados(raiz).resolve(NOMBRE_GRAFICAS);
    }

    /**
     * @param raiz raiz del proyecto
     * @return ruta del archivo de configuracion INI
     */
    public static Path rutaConfiguracion(Path raiz) {
        return raiz.resolve(ARCHIVO_CONFIGURACION);
    }
}
