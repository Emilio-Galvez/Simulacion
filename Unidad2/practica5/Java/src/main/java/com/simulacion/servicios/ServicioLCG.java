package com.simulacion.servicios;

import com.simulacion.datos.Configuracion;
import com.simulacion.estrategias.Generador;
import com.simulacion.estrategias.ParametrosGenerador;
import com.simulacion.fabricas.FabricaGenerador;

/**
 * Servicio de dominio del Generador Congruencial Lineal.
 *
 * <p>Coordina la validacion de parametros, la obtencion de la estrategia mediante
 * la Fabrica (patron Factory Method), la generacion de la secuencia y la
 * normalizacion de los valores.</p>
 */
public final class ServicioLCG {

    public static final String TIPO_GENERADOR = "LCG";

    private final Configuracion configuracion;

    public ServicioLCG(Configuracion configuracion) {
        configuracion.validar();
        this.configuracion = configuracion;
    }

    public Configuracion getConfiguracion() {
        return configuracion;
    }

    /**
     * Crea la estrategia LCG a traves de la Fabrica (patron Factory Method).
     *
     * @param semilla semilla inicial opcional
     * @return instancia del generador
     */
    public Generador crearGenerador(Long semilla) {
        Configuracion efectiva = semilla == null ? configuracion : configuracion.conSemilla(semilla);
        ParametrosGenerador parametros = new ParametrosGenerador(
                efectiva.getMultiplicador(), efectiva.getIncremento(),
                efectiva.getModulo(), efectiva.getSemilla());
        return FabricaGenerador.crear(TIPO_GENERADOR, parametros);
    }

    /**
     * Ejecuta la simulacion y devuelve los estados generados.
     *
     * @param semilla semilla inicial opcional
     * @return arreglo con los estados X(n)
     */
    public long[] simular(Long semilla) {
        return crearGenerador(semilla).generar(configuracion.getCantidad());
    }

    /**
     * Ejecuta la simulacion y devuelve los valores normalizados.
     *
     * @param semilla semilla inicial opcional
     * @return arreglo con los valores U(n)
     */
    public double[] simularNormalizados(Long semilla) {
        return crearGenerador(semilla).generarNormalizados(configuracion.getCantidad());
    }
}
