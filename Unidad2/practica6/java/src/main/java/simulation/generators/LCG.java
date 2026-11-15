package simulation.generators;

import simulation.models.GenerationResult;

/**
 * Generador congruencial lineal.
 *
 * <p>X(n+1) = (a * X(n) + c) mod m, U(n) = X(n+1) / m.</p>
 */
public final class LCG {

    private final long seed;
    private final long multiplier;
    private final long increment;
    private final long modulus;
    private long state;

    public LCG(long seed, long multiplier, long increment, long modulus) {
        if (modulus <= 1) {
            throw new IllegalArgumentException("El modulo debe ser mayor que 1.");
        }
        if (seed < 0 || seed >= modulus) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < modulo.");
        }
        if (multiplier <= 0 || multiplier >= modulus) {
            throw new IllegalArgumentException("El multiplicador debe cumplir 0 < a < modulo.");
        }
        if (increment < 0 || increment >= modulus) {
            throw new IllegalArgumentException("El incremento debe cumplir 0 <= c < modulo.");
        }
        long maxState = modulus - 1;
        if (multiplier > (Long.MAX_VALUE - increment) / maxState) {
            throw new IllegalArgumentException(
                    "Los parametros pueden desbordar long; use parametros menores.");
        }

        this.seed = seed;
        this.multiplier = multiplier;
        this.increment = increment;
        this.modulus = modulus;
        this.state = seed;
    }

    public long seed() {
        return seed;
    }

    public long multiplier() {
        return multiplier;
    }

    public long increment() {
        return increment;
    }

    public long modulus() {
        return modulus;
    }

    public long state() {
        return state;
    }

    public long nextState() {
        state = (multiplier * state + increment) % modulus;
        return state;
    }

    public double nextUniform() {
        return (double) nextState() / (double) modulus;
    }

    public GenerationResult generate(int count) {
        if (count < 0) {
            throw new IllegalArgumentException("La cantidad de numeros no puede ser negativa.");
        }

        long[] states = new long[count];
        double[] uniforms = new double[count];
        long current = state;
        for (int index = 0; index < count; index++) {
            current = (multiplier * current + increment) % modulus;
            states[index] = current;
            uniforms[index] = (double) current / (double) modulus;
        }
        state = current;
        return new GenerationResult(states, uniforms);
    }
}
