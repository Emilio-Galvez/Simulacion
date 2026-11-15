package simulation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import simulation.models.StatisticalTestResult;
import simulation.statistics.ChiSquareTest;

class ChiSquareStrategyTest {

    @Test
    void muestraPerfectamenteUniforme() {
        int n = 10_000;
        double[] sample = new double[n];
        for (int index = 0; index < n; index++) {
            sample[index] = (double) index / n;
        }

        StatisticalTestResult result = new ChiSquareTest(10).run(sample, 0.05);
        int[] observed = (int[]) result.details().get("observed");

        assertEquals(9, (Integer) result.details().get("degrees_of_freedom"));
        for (int value : observed) {
            assertEquals(n / 10, value);
        }
        assertEquals(0.0, result.statistic(), 1e-12);
        assertEquals(1.0, result.pValue(), 1e-12);
        assertFalse(result.rejectNull());
    }

    @Test
    void muestraConstanteRechazaUniformidad() {
        double[] sample = new double[10_000];
        java.util.Arrays.fill(sample, 0.05);
        StatisticalTestResult result = new ChiSquareTest(10).run(sample, 0.05);

        assertTrue(result.statistic() > 1000.0);
        assertTrue(result.pValue() < 0.05);
        assertTrue(result.rejectNull());
    }

    @Test
    void frecuenciasSumanElTotalYGradosDeLibertad() {
        double[] sample = new double[10_000];
        for (int index = 0; index < sample.length; index++) {
            sample[index] = ((double) index + 0.5) / sample.length;
        }
        StatisticalTestResult result = new ChiSquareTest(10).run(sample, 0.05);
        int[] observed = (int[]) result.details().get("observed");
        double[] expected = (double[]) result.details().get("expected");

        int total = 0;
        for (int value : observed) {
            total += value;
        }
        assertEquals(10_000, total);
        assertEquals(10, observed.length);
        assertEquals(10, expected.length);
        assertEquals(9, (Integer) result.details().get("degrees_of_freedom"));
        assertTrue(result.pValue() >= 0.0 && result.pValue() <= 1.0);
    }
}
