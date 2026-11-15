package simulation.services;

import java.util.ArrayList;
import java.util.List;

import simulation.config.Config;
import simulation.generators.LCG;
import simulation.models.GenerationResult;
import simulation.models.SimulationResult;
import simulation.models.StatisticalTestResult;
import simulation.models.TimingResult;
import simulation.simulation.PiEstimator;
import simulation.statistics.ChiSquareTest;
import simulation.statistics.KolmogorovSmirnovTest;
import simulation.statistics.StatisticalTest;

/** Orquestacion de generacion, pruebas estadisticas y medicion de tiempos. */
public final class SimulationService {

    private final Config config;
    private final List<StatisticalTest> tests;

    public SimulationService(Config config) {
        this(config, List.of(new ChiSquareTest(config.bins()), new KolmogorovSmirnovTest()));
    }

    public SimulationService(Config config, List<StatisticalTest> tests) {
        this.config = config;
        this.tests = List.copyOf(tests);
    }

    public void warmUp() {
        run(1000);
    }

    public SimulationResult run(int n) {
        if (n <= 0) {
            throw new IllegalArgumentException("n debe ser positivo.");
        }

        long startGeneration = System.nanoTime();
        LCG lcg = new LCG(config.seed(), config.multiplier(), config.increment(), config.modulus());
        GenerationResult generation = lcg.generate(n);
        long endGeneration = System.nanoTime();

        StatisticalTestResult chiSquare = null;
        StatisticalTestResult kolmogorovSmirnov = null;
        long chiSquareNs = 0L;
        long kolmogorovSmirnovNs = 0L;

        for (StatisticalTest test : tests) {
            long start = System.nanoTime();
            StatisticalTestResult result = test.run(generation.uniforms(), config.alpha());
            long elapsed = System.nanoTime() - start;
            if (test instanceof ChiSquareTest) {
                chiSquare = result;
                chiSquareNs = elapsed;
            } else if (test instanceof KolmogorovSmirnovTest) {
                kolmogorovSmirnov = result;
                kolmogorovSmirnovNs = elapsed;
            }
        }

        if (chiSquare == null || kolmogorovSmirnov == null) {
            throw new IllegalStateException(
                    "Se requieren las estrategias Chi-cuadrado y Kolmogorov-Smirnov.");
        }

        long startPi = System.nanoTime();
        double piEstimate = PiEstimator.estimate(n);
        long piNs = System.nanoTime() - startPi;

        TimingResult timings = new TimingResult(
                endGeneration - startGeneration,
                chiSquareNs,
                kolmogorovSmirnovNs,
                piNs);

        return new SimulationResult(
                n,
                generation,
                chiSquare,
                kolmogorovSmirnov,
                piEstimate,
                PiEstimator.absoluteError(piEstimate),
                timings);
    }

    public List<SimulationResult> runAll() {
        List<SimulationResult> results = new ArrayList<>();
        for (int n : config.sampleSizes()) {
            results.add(run(n));
        }
        return results;
    }
}
