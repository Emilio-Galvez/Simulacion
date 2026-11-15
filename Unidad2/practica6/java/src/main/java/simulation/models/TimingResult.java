package simulation.models;

/** Tiempos en nanosegundos de cada etapa medida. */
public record TimingResult(
        long generationNs,
        long chiSquareNs,
        long kolmogorovSmirnovNs,
        long piNs) {

    public long totalNs() {
        return generationNs + chiSquareNs + kolmogorovSmirnovNs + piNs;
    }

    public double generationSeconds() {
        return generationNs / 1_000_000_000.0;
    }

    public double chiSquareSeconds() {
        return chiSquareNs / 1_000_000_000.0;
    }

    public double kolmogorovSmirnovSeconds() {
        return kolmogorovSmirnovNs / 1_000_000_000.0;
    }

    public double piSeconds() {
        return piNs / 1_000_000_000.0;
    }

    public double totalSeconds() {
        return totalNs() / 1_000_000_000.0;
    }
}
