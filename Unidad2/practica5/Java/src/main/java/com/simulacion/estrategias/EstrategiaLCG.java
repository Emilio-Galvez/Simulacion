package com.simulacion.estrategias;

/**
 * Estrategia concreta del Generador Congruencial Lineal (LCG).
 *
 * <p>Implementa la recurrencia clasica:</p>
 *
 * <pre>X(n+1) = (a * X(n) + c) mod m</pre>
 *
 * <p><b>Desbordamiento numerico:</b> el producto a * X(n) puede superar los 32 bits
 * (1664525 * 4294967295 = 7.149e15), por lo que la aritmetica se realiza en
 * {@code long} (64 bits con signo). Ese valor maximo es inferior a
 * Long.MAX_VALUE (9.22e18), de modo que no hay desbordamiento. Para modulos que
 * son potencias de dos (como m = 2^32) se aplica una mascara de 32 bits, que
 * reproduce exactamente el comportamiento modular requerido.</p>
 */
public final class EstrategiaLCG implements Generador {

    private static final long MASCARA_32_BITS = 0xFFFFFFFFL;

    private final long multiplicador;
    private final long incremento;
    private final long modulo;
    private final long semilla;

    public EstrategiaLCG(long multiplicador, long incremento, long modulo, long semilla) {
        validar(multiplicador, incremento, modulo, semilla);
        this.multiplicador = multiplicador;
        this.incremento = incremento;
        this.modulo = modulo;
        this.semilla = semilla;
    }

    public EstrategiaLCG() {
        this(ParametrosGenerador.porDefecto());
    }

    public EstrategiaLCG(ParametrosGenerador parametros) {
        this(parametros.multiplicador(), parametros.incremento(),
                parametros.modulo(), parametros.semilla());
    }

    private static void validar(long multiplicador, long incremento, long modulo, long semilla) {
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
    }

    @Override
    public long[] generar(int cantidad) {
        if (cantidad < 0) {
            throw new ParametrosInvalidosException(
                    "La cantidad generada debe ser un entero no negativo.");
        }
        long[] estados = new long[cantidad];
        long estado = semilla;
        for (int indice = 0; indice < cantidad; indice++) {
            estado = siguienteEstado(estado);
            estados[indice] = estado;
        }
        return estados;
    }

    /**
     * Calcula X(n+1) aplicando la congruencia de forma exacta para 32 bits.
     *
     * @param estado estado actual X(n)
     * @return estado siguiente X(n+1) en el intervalo [0, m)
     */
    private long siguienteEstado(long estado) {
        long producto = multiplicador * estado + incremento;
        if (esPotenciaDeDos(modulo)) {
            return producto & (modulo - 1);
        }
        return Math.floorMod(producto, modulo);
    }

    private static boolean esPotenciaDeDos(long valor) {
        return valor > 0 && (valor & (valor - 1)) == 0;
    }

    @Override
    public double normalizar(long estado) {
        if (estado < 0 || estado >= modulo) {
            throw new ParametrosInvalidosException("El estado a normalizar esta fuera del rango [0, m).");
        }
        return (double) estado / (double) modulo;
    }

    @Override
    public long getMultiplicador() {
        return multiplicador;
    }

    @Override
    public long getIncremento() {
        return incremento;
    }

    @Override
    public long getModulo() {
        return modulo;
    }

    @Override
    public long getSemilla() {
        return semilla;
    }

    @Override
    public String getNombre() {
        return "LCG";
    }
}
