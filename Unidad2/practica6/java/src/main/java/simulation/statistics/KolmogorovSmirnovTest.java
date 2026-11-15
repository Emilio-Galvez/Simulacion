package simulation.statistics;

import java.util.Arrays;
import java.util.Map;

import simulation.models.StatisticalTestResult;

/** Estrategia Kolmogorov-Smirnov para una distribucion uniforme. */
public final class KolmogorovSmirnovTest implements StatisticalTest {

    @Override
    public String name() {
        return "Kolmogorov-Smirnov";
    }

    @Override
    public StatisticalTestResult run(double[] sample, double alpha) {
        StatisticalTest.validateInput(sample, alpha);
        int n = sample.length;
        double[] ordered = sample.clone();
        Arrays.sort(ordered);

        double dPlus = 0.0;
        double dMinus = 0.0;
        for (int position = 1; position <= n; position++) {
            double value = ordered[position - 1];
            double empiricalUpper = (double) position / n;
            double empiricalLower = (double) (position - 1) / n;
            dPlus = Math.max(dPlus, empiricalUpper - value);
            dMinus = Math.max(dMinus, value - empiricalLower);
        }

        double statistic = Math.max(dPlus, dMinus);
        double pValue = Math.min(
                1.0,
                Math.max(0.0, SpecialFunctions.kolmogorovSmirnovPValue(statistic, n)));
        boolean rejectNull = pValue < alpha;

        return new StatisticalTestResult(
                name(),
                statistic,
                pValue,
                alpha,
                rejectNull,
                Map.of(
                        "d_plus", dPlus,
                        "d_minus", dMinus,
                        "sample_size", n));
    }
}
