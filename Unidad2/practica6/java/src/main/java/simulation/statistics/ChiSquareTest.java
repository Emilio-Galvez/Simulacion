package simulation.statistics;

import java.util.Map;

import simulation.models.StatisticalTestResult;

/** Estrategia Chi-cuadrado para una distribucion uniforme en [0, 1). */
public final class ChiSquareTest implements StatisticalTest {

    private final int bins;

    public ChiSquareTest(int bins) {
        if (bins <= 1) {
            throw new IllegalArgumentException("El numero de intervalos debe ser mayor que 1.");
        }
        this.bins = bins;
    }

    public int bins() {
        return bins;
    }

    @Override
    public String name() {
        return "Chi-cuadrado";
    }

    @Override
    public StatisticalTestResult run(double[] sample, double alpha) {
        StatisticalTest.validateInput(sample, alpha);
        int n = sample.length;
        int[] observed = new int[bins];

        for (double value : sample) {
            int index = (int) (value * bins);
            if (index >= bins) {
                index = bins - 1;
            }
            observed[index]++;
        }

        double expectedValue = (double) n / bins;
        double[] expected = new double[bins];
        double statistic = 0.0;
        for (int i = 0; i < bins; i++) {
            expected[i] = expectedValue;
            double difference = observed[i] - expected[i];
            statistic += (difference * difference) / expected[i];
        }

        int degreesOfFreedom = bins - 1;
        double pValue = Math.min(
                1.0,
                Math.max(0.0, SpecialFunctions.chiSquareSurvival(statistic, degreesOfFreedom)));
        boolean rejectNull = pValue < alpha;

        return new StatisticalTestResult(
                name(),
                statistic,
                pValue,
                alpha,
                rejectNull,
                Map.of(
                        "observed", observed,
                        "expected", expected,
                        "degrees_of_freedom", degreesOfFreedom,
                        "bins", bins,
                        "sample_size", n));
    }
}
