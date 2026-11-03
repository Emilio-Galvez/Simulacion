package com.simulacion.datos;

/**
 * Fila del formato de intercambio CSV para comparar dos secuencias.
 *
 * <p>Representa una observacion comparada entre dos implementaciones
 * (por ejemplo Python y Java) y por eso reside en la capa de DATOS,
 * junto al resto de los elementos que definen el formato persistido.</p>
 *
 * @param indice    numero de prueba n
 * @param xPython   estado crudo de la primera secuencia
 * @param xJava     estado crudo de la segunda secuencia
 * @param uPython   valor normalizado de la primera secuencia
 * @param uJava     valor normalizado de la segunda secuencia
 * @param coincide  indica si ambos estados son iguales
 */
public record FilaComparacion(int indice, long xPython, long xJava, String uPython, String uJava,
                              boolean coincide) {
}
