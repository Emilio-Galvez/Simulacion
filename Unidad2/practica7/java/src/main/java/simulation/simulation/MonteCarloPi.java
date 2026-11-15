package simulation.simulation;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import simulation.models.Measurement;
import simulation.models.Summary;

/**
 * Estimacion de pi mediante el metodo Monte Carlo.
 *
 * <p>Se generan N puntos uniformes en el cuadrado [0, 1) x [0, 1) y se cuentan
 * los que caen dentro del circulo unitario x^2 + y^2 <= 1. La estimacion es</p>
 *
 * <pre>pi_estimado = 4 * (Nc / N)</pre>
 *
 * <p>Se usa el RNG nativo {@link Random} con la misma semilla que Python. El
 * procedimiento es comparable, aunque las secuencias de ambos lenguajes no son
 * identicas porque los algoritmos de generacion son distintos.</p>
 */
public final class MonteCarloPi {

    public static final double REAL_PI = 3.141592653589793;

    private final long seed;
    private final double realPi;

    public MonteCarloPi(long seed, double realPi) {
        this.seed = seed;
        this.realPi = realPi;
    }

    public Measurement measure(int n, int repetition) {
        if (n <= 0) {
            throw new IllegalArgumentException("La cantidad de puntos debe ser positiva.");
        }

        Random random = new Random(seed);
        int inside = 0;
        long start = System.nanoTime();
        for (int i = 0; i < n; i++) {
            double x = random.nextDouble();
            double y = random.nextDouble();
            if (x * x + y * y <= 1.0) {
                inside++;
            }
        }
        double elapsedSeconds = (System.nanoTime() - start) / 1_000_000_000.0;

        double estimate = 4.0 * inside / n;
        return new Measurement(
                n,
                repetition,
                inside,
                estimate,
                Math.abs(realPi - estimate),
                elapsedSeconds);
    }

    public Summary run(int n, int repetitions) {
        if (repetitions <= 0) {
            throw new IllegalArgumentException("El numero de repeticiones debe ser positivo.");
        }

        List<Measurement> measurements = new ArrayList<>();
        for (int repetition = 1; repetition <= repetitions; repetition++) {
            measurements.add(measure(n, repetition));
        }
        Measurement first = measurements.get(0);
        return new Summary(
                n,
                first.inside(),
                first.piEstimate(),
                first.error(),
                measurements);
    }
}
