package simulation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

import simulation.statistics.SpecialFunctions;

class SpecialFunctionsTest {

    @Test
    void logGammaValoresConocidos() {
        assertEquals(0.0, SpecialFunctions.logGamma(1.0), 1e-12);
        assertEquals(Math.log(24.0), SpecialFunctions.logGamma(5.0), 1e-12);
        assertEquals(
                Math.log(Math.sqrt(Math.PI)),
                SpecialFunctions.logGamma(0.5),
                1e-12);
    }

    @Test
    void chiCuadradoValorCritico() {
        assertEquals(0.05, SpecialFunctions.chiSquareSurvival(16.919, 9), 1e-4);
        assertEquals(1.0, SpecialFunctions.chiSquareSurvival(0.0, 9));
    }

    @Test
    void kolmogorovValorCritico() {
        assertEquals(0.05, SpecialFunctions.kolmogorovSurvival(1.36), 0.005);
        assertEquals(1.0, SpecialFunctions.kolmogorovSurvival(0.0));
    }
}
