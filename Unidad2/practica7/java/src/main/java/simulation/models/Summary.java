package simulation.models;

import java.util.List;
import java.util.stream.Collectors;

/** Resumen de las repeticiones para un tamano de muestra N. */
public record Summary(
        int n,
        int inside,
        double piEstimate,
        double error,
        List<Measurement> measurements) {

    public Summary {
        measurements = List.copyOf(measurements);
    }

    public List<Double> times() {
        return measurements.stream().map(Measurement::timeSeconds).collect(Collectors.toList());
    }

    public double medianTimeSeconds() {
        List<Double> sorted = times().stream().sorted().toList();
        int size = sorted.size();
        if (size % 2 == 1) {
            return sorted.get(size / 2);
        }
        return (sorted.get(size / 2 - 1) + sorted.get(size / 2)) / 2.0;
    }

    public double meanTimeSeconds() {
        return times().stream().mapToDouble(Double::doubleValue).average().orElseThrow();
    }

    public double minTimeSeconds() {
        return times().stream().mapToDouble(Double::doubleValue).min().orElseThrow();
    }

    public double maxTimeSeconds() {
        return times().stream().mapToDouble(Double::doubleValue).max().orElseThrow();
    }
}
