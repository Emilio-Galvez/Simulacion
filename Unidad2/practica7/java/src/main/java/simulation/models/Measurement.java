package simulation.models;

/** Una ejecucion individual del experimento Monte Carlo. */
public record Measurement(
        int n,
        int repetition,
        int inside,
        double piEstimate,
        double error,
        double timeSeconds) {
}
