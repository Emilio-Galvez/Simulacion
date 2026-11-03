package com.simulacion.estrategias;

/**
 * Parametros matematicos de un generador congruencial lineal.
 *
 * @param multiplicador coeficiente a
 * @param incremento    constante aditiva c
 * @param modulo        modulo m
 * @param semilla       semilla inicial X(0)
 */
public record ParametrosGenerador(long multiplicador, long incremento, long modulo, long semilla) {

    public static final long MULTIPLICADOR_POR_DEFECTO = 1664525L;
    public static final long INCREMENTO_POR_DEFECTO = 1013904223L;
    public static final long MODULO_POR_DEFECTO = 4294967296L;
    public static final long SEMILLA_POR_DEFECTO = 12345L;

    public static ParametrosGenerador porDefecto() {
        return new ParametrosGenerador(
                MULTIPLICADOR_POR_DEFECTO,
                INCREMENTO_POR_DEFECTO,
                MODULO_POR_DEFECTO,
                SEMILLA_POR_DEFECTO
        );
    }

    public ParametrosGenerador conSemilla(long nuevaSemilla) {
        return new ParametrosGenerador(multiplicador, incremento, modulo, nuevaSemilla);
    }
}
