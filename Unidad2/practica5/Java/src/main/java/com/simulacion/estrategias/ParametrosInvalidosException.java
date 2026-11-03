package com.simulacion.estrategias;

/**
 * Error de negocio lanzado cuando los parametros del generador son invalidos.
 */
public class ParametrosInvalidosException extends RuntimeException {

    public ParametrosInvalidosException(String mensaje) {
        super(mensaje);
    }
}
