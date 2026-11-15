package simulation.models;

import java.util.Map;

/** Resultado generico de una prueba de bondad de ajuste. */
public record StatisticalTestResult(
        String name,
        double statistic,
        double pValue,
        double alpha,
        boolean rejectNull,
        Map<String, Object> details) {

    public StatisticalTestResult {
        details = Map.copyOf(details);
    }

    public String decision() {
        return rejectNull ? "Se rechaza H0" : "No se rechaza H0";
    }
}
