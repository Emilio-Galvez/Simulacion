package simulation;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import simulation.generators.LCG;

class EquivalenceTest {

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
    void primerosEstadosCoincidenConLaReferencia() {
        assertArrayEquals(EXPECTED_STATES, makeLcg().generate(10).states());
    }

    @Test
    void secuenciaJavaYPythonSonIdenticas() throws IOException {
        Path pythonSequence = findPythonSequence();
        Assumptions.assumeTrue(
                pythonSequence != null,
                "Ejecute primero la implementacion Python para comparar las secuencias.");

        List<String> lines = Files.readAllLines(pythonSequence);
        long[] pythonStates = new long[lines.size() - 1];
        for (int index = 1; index < lines.size(); index++) {
            String[] parts = lines.get(index).split(",");
            pythonStates[index - 1] = Long.parseLong(parts[1]);
        }

        assertArrayEquals(pythonStates, makeLcg().generate(pythonStates.length).states());
    }

    private Path findPythonSequence() {
        List<Path> candidates = List.of(
                Path.of("..", "python", "results", "sequences", "sequence_1000.csv"),
                Path.of("python", "results", "sequences", "sequence_1000.csv"));
        for (Path candidate : candidates) {
            if (Files.exists(candidate)) {
                return candidate;
            }
        }
        return null;
    }
}
