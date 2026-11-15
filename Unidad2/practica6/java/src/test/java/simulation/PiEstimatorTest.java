package simulation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import simulation.simulation.PiEstimator;

class PiEstimatorTest {

    @Test
    void errorAbsoluto() {
        assertEquals(0.141592653589793, PiEstimator.absoluteError(3.0), 1e-15);
    }

    @Test
    void serieDeLeibnizConvergeLentamente() {
        double estimate = PiEstimator.estimate(1_000_000);
        assertTrue(PiEstimator.absoluteError(estimate) < 1e-5);
    }

    @Test
    void estimacionEnRango() {
        double estimate = PiEstimator.estimate(1_000);
        assertTrue(estimate > 3.14 && estimate < 3.142);
    }

    @Test
    void terminosInvalidos() {
        assertThrows(IllegalArgumentException.class, () -> PiEstimator.estimate(0));
    }
}
