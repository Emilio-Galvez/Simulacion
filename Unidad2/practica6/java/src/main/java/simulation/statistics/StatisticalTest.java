package simulation.statistics;

import simulation.models.StatisticalTestResult;

/** Contrato comun para las pruebas estadisticas (patron Strategy). */
public interface StatisticalTest {

    String name();

    StatisticalTestResult run(double[] sample, double alpha);

    static void validateInput(double[] sample, double alpha) {
        if (sample == null || sample.length == 0) {
            throw new IllegalArgumentException("La muestra no puede estar vacia.");
        }
        if (alpha <= 0.0 || alpha >= 1.0) {
            throw new IllegalArgumentException("alpha debe estar en (0, 1).");
        }
        for (double value : sample) {
            if (value < 0.0 || value >= 1.0) {
                throw new IllegalArgumentException("Valor fuera del intervalo [0, 1): " + value);
            }
        }
    }
}
