package com.simulacion.fabricas;

import com.simulacion.estrategias.EstrategiaLCG;
import com.simulacion.estrategias.Generador;
import com.simulacion.estrategias.ParametrosGenerador;

import java.util.Map;
import java.util.TreeMap;
import java.util.function.Function;

/**
 * Factory Method para crear instancias de generadores pseudoaleatorios.
 *
 * <p>El registro de constructores permite incorporar nuevas estrategias
 * (por ejemplo Mersenne Twister o Lehmer) sin modificar el codigo cliente:
 * basta con registrar el constructor asociado al nuevo tipo.</p>
 */
public final class FabricaGenerador {

    /** Error de negocio lanzado cuando se solicita un generador no registrado. */
    public static class TipoGeneradorDesconocidoException extends RuntimeException {
        public TipoGeneradorDesconocidoException(String mensaje) {
            super(mensaje);
        }
    }

    private static final Map<String, Function<ParametrosGenerador, Generador>> REGISTRO =
            new TreeMap<>(String.CASE_INSENSITIVE_ORDER);

    static {
        registrar("LCG", EstrategiaLCG::new);
    }

    private FabricaGenerador() {
    }

    /**
     * Registra (o reemplaza) el constructor asociado a un tipo de generador.
     *
     * @param tipo       nombre del tipo, por ejemplo "LCG"
     * @param constructor fabrica que produce la estrategia
     */
    public static void registrar(String tipo, Function<ParametrosGenerador, Generador> constructor) {
        if (tipo == null || tipo.isBlank()) {
            throw new TipoGeneradorDesconocidoException("El tipo de generador no puede estar vacio.");
        }
        REGISTRO.put(tipo.trim(), constructor);
    }

    /**
     * Crea un generador del tipo indicado aplicando sus parametros.
     *
     * @param tipo        tipo de generador solicitado
     * @param parametros  parametros matematicos de la simulacion
     * @return instancia de la estrategia solicitada
     */
    public static Generador crear(String tipo, ParametrosGenerador parametros) {
        Function<ParametrosGenerador, Generador> constructor = REGISTRO.get(tipo == null ? "" : tipo.trim());
        if (constructor == null) {
            throw new TipoGeneradorDesconocidoException(
                    "Generador desconocido: '" + tipo + "'. Disponibles: " + String.join(", ", REGISTRO.keySet()) + ".");
        }
        return constructor.apply(parametros);
    }

    /**
     * Crea un generador del tipo indicado usando los parametros por defecto.
     *
     * @param tipo tipo de generador solicitado
     * @return instancia de la estrategia solicitada
     */
    public static Generador crear(String tipo) {
        return crear(tipo, ParametrosGenerador.porDefecto());
    }

    /**
     * @return lista ordenada de los tipos de generador registrados
     */
    public static String[] tiposDisponibles() {
        return REGISTRO.keySet().toArray(new String[0]);
    }
}
