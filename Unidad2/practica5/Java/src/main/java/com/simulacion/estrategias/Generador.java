package com.simulacion.estrategias;

/**
 * Contrato Strategy para las estrategias de generacion de numeros pseudoaleatorios.
 *
 * <p>Permite que la logica de negocio trabaje con cualquier algoritmo de generacion
 * sin conocer sus detalles internos. Implementaciones concretas: {@link EstrategiaLCG}.</p>
 */
public interface Generador {

    /**
     * Genera la cantidad indicada de estados crudos X(n).
     *
     * @param cantidad numero de valores a generar
     * @return arreglo con los estados X(1), X(2), ... X(cantidad)
     */
    long[] generar(int cantidad);

    /**
     * Normaliza un estado crudo mediante U(n) = X(n) / m.
     *
     * @param estado estado crudo X(n)
     * @return valor pseudoaleatorio en el intervalo [0, 1)
     */
    double normalizar(long estado);

    /**
     * Genera la cantidad indicada de valores normalizados U(n).
     *
     * @param cantidad numero de valores a generar
     * @return arreglo con los valores normalizados
     */
    default double[] generarNormalizados(int cantidad) {
        long[] estados = generar(cantidad);
        double[] normalizados = new double[cantidad];
        for (int indice = 0; indice < cantidad; indice++) {
            normalizados[indice] = normalizar(estados[indice]);
        }
        return normalizados;
    }

    long getMultiplicador();

    long getIncremento();

    long getModulo();

    long getSemilla();

    /**
     * @return nombre descriptivo de la estrategia
     */
    default String getNombre() {
        return getClass().getSimpleName();
    }
}
