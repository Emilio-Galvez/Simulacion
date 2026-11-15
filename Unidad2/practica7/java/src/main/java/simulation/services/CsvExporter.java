package simulation.services;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import simulation.models.Measurement;
import simulation.models.Summary;

/** Exportacion de resultados a CSV con el mismo formato que Python. */
public final class CsvExporter {

    private final Path resultsDir;

    public CsvExporter(Path resultsDir) {
        this.resultsDir = resultsDir;
    }

    public void exportAll(List<Summary> summaries) throws IOException {
        Files.createDirectories(resultsDir);
        exportMeasurements(summaries);
        exportSummary(summaries);
    }

    private void exportMeasurements(List<Summary> summaries) throws IOException {
        Path path = resultsDir.resolve("mediciones.csv");
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write("N,repeticion,dentro,pi_estimado,error,tiempo_s\n");
            for (Summary summary : summaries) {
                for (Measurement measurement : summary.measurements()) {
                    writer.write(Integer.toString(measurement.n()));
                    writer.write(',');
                    writer.write(Integer.toString(measurement.repetition()));
                    writer.write(',');
                    writer.write(Integer.toString(measurement.inside()));
                    writer.write(',');
                    writer.write(Double.toString(measurement.piEstimate()));
                    writer.write(',');
                    writer.write(Double.toString(measurement.error()));
                    writer.write(',');
                    writer.write(Double.toString(measurement.timeSeconds()));
                    writer.write('\n');
                }
            }
        }
    }

    private void exportSummary(List<Summary> summaries) throws IOException {
        Path path = resultsDir.resolve("resumen.csv");
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write(
                    "N,dentro,pi_estimado,error,tiempo_mediana_s,"
                            + "tiempo_media_s,tiempo_min_s,tiempo_max_s\n");
            for (Summary summary : summaries) {
                writer.write(Integer.toString(summary.n()));
                writer.write(',');
                writer.write(Integer.toString(summary.inside()));
                writer.write(',');
                writer.write(Double.toString(summary.piEstimate()));
                writer.write(',');
                writer.write(Double.toString(summary.error()));
                writer.write(',');
                writer.write(Double.toString(summary.medianTimeSeconds()));
                writer.write(',');
                writer.write(Double.toString(summary.meanTimeSeconds()));
                writer.write(',');
                writer.write(Double.toString(summary.minTimeSeconds()));
                writer.write(',');
                writer.write(Double.toString(summary.maxTimeSeconds()));
                writer.write('\n');
            }
        }
    }
}
