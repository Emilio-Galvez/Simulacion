package simulation;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;

import simulation.config.Config;
import simulation.models.Summary;
import simulation.services.CsvExporter;
import simulation.services.SimulationService;

/** Punto de entrada de la implementacion Java de la Practica 7. */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) throws IOException {
        Path configPath = null;
        boolean warmup = true;
        for (String arg : args) {
            if ("--no-warmup".equals(arg)) {
                warmup = false;
            } else if (!arg.startsWith("--")) {
                configPath = Path.of(arg);
            }
        }

        Config config = configPath == null ? Config.load() : Config.load(configPath);
        SimulationService service = new SimulationService(config);
        if (warmup) {
            service.warmUp();
        }

        List<Summary> summaries = service.runAll();
        new CsvExporter(config.resultsDir()).exportAll(summaries);

        System.out.println("\nResultados Java");
        System.out.printf(
                Locale.ROOT,
                "%10s %12s %16s %14s %20s%n",
                "N", "dentro", "pi estimado", "error", "tiempo mediano (s)");
        for (Summary summary : summaries) {
            System.out.printf(
                    Locale.ROOT,
                    "%,10d %,12d %16.12f %14.6e %20.6f%n",
                    summary.n(),
                    summary.inside(),
                    summary.piEstimate(),
                    summary.error(),
                    summary.medianTimeSeconds());
        }
        System.out.println("\nResultados Java exportados en: " + config.resultsDir());
    }
}
