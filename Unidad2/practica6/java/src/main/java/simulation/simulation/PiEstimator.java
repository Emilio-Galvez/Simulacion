package simulation.simulation;

/**
 * Estimacion determinista de pi para completar la tabla de la guia.
 *
 * <p>La guia no define el procedimiento. Para no usar Monte Carlo se emplea la
 * serie alterna de Leibniz con N terminos, igual que en Python:</p>
 *
 * <pre>pi = 4 * sum_{k=0}^{N-1} (-1)^k / (2k + 1)</pre>
 */
public final class PiEstimator {

    public static final double REAL_PI = 3.141592653589793;

    private PiEstimator() {
    }

    public static double estimate(long terms) {
        if (terms <= 0) {
            throw new IllegalArgumentException("La cantidad de terminos debe ser positiva.");
        }

        double total = 0.0;
        double sign = 1.0;
        for (long k = 0; k < terms; k++) {
            total += sign / (2.0 * k + 1.0);
            sign = -sign;
        }
        return 4.0 * total;
    }

    public static double absoluteError(double estimate) {
        return Math.abs(REAL_PI - estimate);
    }

    public static double referenceValue() {
        return REAL_PI;
    }
}
