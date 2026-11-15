package simulation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;

import org.junit.jupiter.api.Test;

import simulation.models.StatisticalTestResult;
import simulation.statistics.KolmogorovSmirnovTest;

class KolmogorovSmirnovStrategyTest {

    @Test
    void muestraEnRejillaUniforme() {
        int n = 10_000;
        double[] sample = new double[n];
        for (int index = 0; index < n; index++) {
            sample[index] = (double) index / n;
        }

        StatisticalTestResult result = new KolmogorovSmirnovTest().run(sample, 0.05);
        assertEquals(1.0 / n, result.statistic(), 1e-12);
        assertEquals(0.0, (Double) result.details().get("d_minus"), 1e-12);
        assertTrue(result.pValue() > 0.05);
        assertFalse(result.rejectNull());
    }

    @Test
    void muestraConstanteRechazaUniformidad() {
        double[] sample = new double[1_000];
        Arrays.fill(sample, 0.5);
        StatisticalTestResult result = new KolmogorovSmirnovTest().run(sample, 0.05);

        assertEquals(0.5, result.statistic(), 1e-3);
        assertTrue(result.pValue() < 0.05);
        assertTrue(result.rejectNull());
    }

    @Test
    void estadisticoEsElMaximoDeLasDiferencias() {
        double[] sample = new double[1_000];
        for (int index = 0; index < sample.length; index++) {
            sample[index] = ((double) index + 0.5) / sample.length;
        }
        StatisticalTestResult result = new KolmogorovSmirnovTest().run(sample, 0.05);
        double dPlus = (Double) result.details().get("d_plus");
        double dMinus = (Double) result.details().get("d_minus");

        assertTrue(dPlus >= 0.0);
        assertTrue(dMinus >= 0.0);
        assertEquals(Math.max(dPlus, dMinus), result.statistic(), 1e-15);
        assertTrue(result.pValue() >= 0.0 && result.pValue() <= 1.0);
    }
}
