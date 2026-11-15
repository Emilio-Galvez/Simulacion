package simulation.statistics;

/** Funciones numericas equivalentes a las de la implementacion Python. */
public final class SpecialFunctions {

    private static final double EPS = 3.0e-14;
    private static final double FPMIN = 1.0e-300;
    private static final int ITMAX = 1000;
    private static final double[] LANCZOS = {
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    };

    private SpecialFunctions() {
    }

    public static double logGamma(double z) {
        if (z < 0.5) {
            return Math.log(Math.PI)
                    - Math.log(Math.sin(Math.PI * z))
                    - logGamma(1.0 - z);
        }

        z -= 1.0;
        double x = LANCZOS[0];
        for (int i = 1; i < 9; i++) {
            x += LANCZOS[i] / (z + i);
        }
        double t = z + 7.5;
        return 0.5 * Math.log(2.0 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }

    private static double gammaSeries(double a, double x) {
        double ap = a;
        double summation = 1.0 / a;
        double delta = summation;
        for (int i = 0; i < ITMAX; i++) {
            ap += 1.0;
            delta *= x / ap;
            summation += delta;
            if (Math.abs(delta) < Math.abs(summation) * EPS) {
                break;
            }
        }
        return summation * Math.exp(-x + a * Math.log(x) - logGamma(a));
    }

    private static double gammaContinuedFraction(double a, double x) {
        double b = x + 1.0 - a;
        double c = 1.0 / FPMIN;
        double d = 1.0 / b;
        double h = d;
        for (int i = 1; i <= ITMAX; i++) {
            double an = -i * (i - a);
            b += 2.0;
            d = an * d + b;
            if (Math.abs(d) < FPMIN) {
                d = FPMIN;
            }
            c = b + an / c;
            if (Math.abs(c) < FPMIN) {
                c = FPMIN;
            }
            d = 1.0 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1.0) < EPS) {
                break;
            }
        }
        return Math.exp(-x + a * Math.log(x) - logGamma(a)) * h;
    }

    public static double regularizedGammaQ(double a, double x) {
        if (a <= 0.0) {
            throw new IllegalArgumentException("a debe ser positiva.");
        }
        if (x < 0.0) {
            throw new IllegalArgumentException("x no puede ser negativo.");
        }
        if (x == 0.0) {
            return 1.0;
        }
        if (x < a + 1.0) {
            return 1.0 - gammaSeries(a, x);
        }
        return gammaContinuedFraction(a, x);
    }

    public static double chiSquareSurvival(double statistic, int degreesOfFreedom) {
        if (degreesOfFreedom <= 0) {
            throw new IllegalArgumentException("Los grados de libertad deben ser positivos.");
        }
        if (statistic <= 0.0) {
            return 1.0;
        }
        return regularizedGammaQ(degreesOfFreedom / 2.0, statistic / 2.0);
    }

    public static double kolmogorovSurvival(double lambda) {
        if (lambda <= 0.0 || lambda < 0.1) {
            return 1.0;
        }

        double a2 = -2.0 * lambda * lambda;
        double fac = 2.0;
        double total = 0.0;
        double term = 1.0;
        double previous = 0.0;

        for (int i = 0; i < 1000; i++) {
            term *= Math.exp(a2);
            total += fac * term;
            fac = -fac;
            if (Math.abs(term) <= 1.0e-6 * previous || Math.abs(term) <= 1.0e-16 * Math.abs(total)) {
                break;
            }
            previous = Math.abs(term);
        }
        return Math.min(1.0, Math.max(0.0, total));
    }

    public static double kolmogorovSmirnovPValue(double statistic, int sampleSize) {
        if (sampleSize <= 0) {
            throw new IllegalArgumentException("El tamano de muestra debe ser positivo.");
        }
        double rootN = Math.sqrt(sampleSize);
        double lambda = (rootN + 0.12 + 0.11 / rootN) * statistic;
        return kolmogorovSurvival(lambda);
    }
}
