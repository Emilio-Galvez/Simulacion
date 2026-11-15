package simulation;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

import simulation.generators.LCG;
import simulation.models.GenerationResult;

class LCGTest {

    private static final long[] EXPECTED_STATES = {
        87628868L,
        71072467L,
        2332836374L,
        2726892157L,
        3908547000L,
        483019191L,
        2129828778L,
        2355140353L,
        2560230508L,
        3364893915L
    };

    private LCG makeLcg() {
        return new LCG(12345L, 1664525L, 1013904223L, 4294967296L);
    }

    @Test
    void primerosEstadosConocidos() {
        assertArrayEquals(EXPECTED_STATES, makeLcg().generate(10).states());
    }

    @Test
    void valoresEnIntervaloUnitario() {
        GenerationResult result = makeLcg().generate(10_000);
        assertEquals(10_000, result.uniforms().length);
        for (int index = 0; index < result.uniforms().length; index++) {
            double value = result.uniforms()[index];
            assertEquals(true, value >= 0.0 && value < 1.0);
            assertEquals(
                    result.states()[index] / 4294967296.0,
                    value,
                    0.0);
        }
    }

    @Test
    void reproducibilidad() {
        assertArrayEquals(
                makeLcg().generate(1_000).states(),
                makeLcg().generate(1_000).states());
    }

    @Test
    void elGeneradorAvanzaSuEstado() {
        LCG lcg = makeLcg();
        assertEquals(12345L, lcg.state());
        lcg.nextState();
        assertEquals(EXPECTED_STATES[0], lcg.state());
    }

    @Test
    void parametrosInvalidos() {
        assertThrows(IllegalArgumentException.class,
                () -> new LCG(-1L, 1664525L, 1013904223L, 4294967296L));
        assertThrows(IllegalArgumentException.class,
                () -> new LCG(12345L, 0L, 1013904223L, 4294967296L));
        assertThrows(IllegalArgumentException.class,
                () -> new LCG(12345L, 1664525L, -1L, 4294967296L));
        assertThrows(IllegalArgumentException.class,
                () -> new LCG(12345L, 1664525L, 1013904223L, 1L));
        assertThrows(IllegalArgumentException.class,
                () -> new LCG(4294967296L, 1664525L, 1013904223L, 4294967296L));
    }

    @Test
    void cantidadNegativa() {
        assertThrows(IllegalArgumentException.class, () -> makeLcg().generate(-1));
    }
}
