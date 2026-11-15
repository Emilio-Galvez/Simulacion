package simulation.models;

/** Resultado completo de una ejecucion para un tamano N. */
public record SimulationResult(
        int n,
        GenerationResult generation,
        StatisticalTestResult chiSquare,
        StatisticalTestResult kolmogorovSmirnov,
        double piEstimate,
        double piError,
        TimingResult timings) {
}
