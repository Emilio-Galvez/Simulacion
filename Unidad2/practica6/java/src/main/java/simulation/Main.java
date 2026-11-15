package simulation;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;

import simulation.config.Config;
import simulation.models.SimulationResult;
import simulation.services.CsvExporter;
import simulation.services.SimulationService;

/** Punto de entrada de la implementacion Java de la Practica 6. */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) throws IOException {
        Config config = args.length > 0 ? Config.load(Path.of(args[0])) : Config.load();
        SimulationService service = new SimulationService(config);
        service.warmUp();

        List<SimulationResult> results = service.runAll();
        new CsvExporter(config.resultsDir()).exportAll(results);

        System.out.println("\nResultados Java");
        System.out.printf(
                Locale.ROOT,
                "%10s %16s %14s %14s %12s %12s%n",
                "N", "pi estimado", "error", "tiempo (s)", "p Chi2", "p KS");
        for (SimulationResult result : results) {
            System.out.printf(
                    Locale.ROOT,
                    "%10d %16.12f %14.6e %14.6f %12.6f %12.6f%n",
                    result.n(),
                    result.piEstimate(),
                    result.piError(),
                    result.timings().totalSeconds(),
                    result.chiSquare().pValue(),
                    result.kolmogorovSmirnov().pValue());
        }
        System.out.println("\nResultados Java exportados en: " + config.resultsDir());
    }
}
