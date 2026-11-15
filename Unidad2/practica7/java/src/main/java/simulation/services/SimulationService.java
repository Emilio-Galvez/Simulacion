package simulation.services;

import java.util.ArrayList;
import java.util.List;

import simulation.config.Config;
import simulation.models.Summary;
import simulation.simulation.MonteCarloPi;

/** Orquestacion del experimento Monte Carlo y medicion de tiempos. */
public final class SimulationService {

    private final Config config;

    public SimulationService(Config config) {
        this.config = config;
    }

    private MonteCarloPi newExperiment() {
        return new MonteCarloPi(config.seed(), config.realPi());
    }

    public void warmUp() {
        newExperiment().measure(config.warmupSize(), 0);
    }

    public Summary run(int n) {
        return newExperiment().run(n, config.repetitions());
    }

    public List<Summary> runAll() {
        List<Summary> results = new ArrayList<>();
        for (int n : config.sampleSizes()) {
            results.add(run(n));
        }
        return results;
    }
}
