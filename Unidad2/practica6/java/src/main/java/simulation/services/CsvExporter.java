package simulation.services;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import simulation.models.SimulationResult;
import simulation.models.StatisticalTestResult;
import simulation.models.TimingResult;

/** Exportacion de resultados a CSV con el mismo formato que Python. */
public final class CsvExporter {

    private final Path sequencesDir;
    private final Path statisticsDir;
    private final Path performanceDir;
    private final Path summaryDir;

    public CsvExporter(Path resultsDir) {
        sequencesDir = resultsDir.resolve("sequences");
        statisticsDir = resultsDir.resolve("statistics");
        performanceDir = resultsDir.resolve("performance");
        summaryDir = resultsDir.resolve("summary");
    }

    public void exportAll(List<SimulationResult> results) throws IOException {
        Files.createDirectories(sequencesDir);
        Files.createDirectories(statisticsDir);
        Files.createDirectories(performanceDir);
        Files.createDirectories(summaryDir);

        for (SimulationResult result : results) {
            exportSequence(result);
        }
        exportStatistics(results);
        exportPerformance(results);
        exportSummary(results);
    }

    private void exportSequence(SimulationResult result) throws IOException {
        Path path = sequencesDir.resolve("sequence_" + result.n() + ".csv");
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write("index,state,uniform\n");
            long[] states = result.generation().states();
            double[] uniforms = result.generation().uniforms();
            for (int index = 0; index < states.length; index++) {
                writer.write(Integer.toString(index + 1));
                writer.write(',');
                writer.write(Long.toString(states[index]));
                writer.write(',');
                writer.write(Double.toString(uniforms[index]));
                writer.write('\n');
            }
        }
    }

    private void exportStatistics(List<SimulationResult> results) throws IOException {
        Path chiPath = statisticsDir.resolve("chi_square.csv");
        try (BufferedWriter writer = Files.newBufferedWriter(chiPath, StandardCharsets.UTF_8)) {
            writer.write("N,statistic,degrees_of_freedom,p_value,alpha,decision");
            for (int index = 0; index < 10; index++) {
                writer.write(",observed_" + index);
            }
            for (int index = 0; index < 10; index++) {
                writer.write(",expected_" + index);
            }
            writer.write('\n');

            for (SimulationResult result : results) {
                StatisticalTestResult chi = result.chiSquare();
                int[] observed = (int[]) chi.details().get("observed");
                double[] expected = (double[]) chi.details().get("expected");
                writer.write(Integer.toString(result.n()));
                writer.write(',');
                writer.write(Double.toString(chi.statistic()));
                writer.write(',');
                writer.write(Integer.toString((Integer) chi.details().get("degrees_of_freedom")));
                writer.write(',');
                writer.write(Double.toString(chi.pValue()));
                writer.write(',');
                writer.write(Double.toString(chi.alpha()));
                writer.write(',');
                writer.write(chi.decision());
                for (int value : observed) {
                    writer.write(',');
                    writer.write(Integer.toString(value));
                }
                for (double value : expected) {
                    writer.write(',');
                    writer.write(Double.toString(value));
                }
                writer.write('\n');
            }
        }

        Path ksPath = statisticsDir.resolve("kolmogorov_smirnov.csv");
        try (BufferedWriter writer = Files.newBufferedWriter(ksPath, StandardCharsets.UTF_8)) {
            writer.write("N,statistic,d_plus,d_minus,p_value,alpha,decision\n");
            for (SimulationResult result : results) {
                StatisticalTestResult ks = result.kolmogorovSmirnov();
                writer.write(Integer.toString(result.n()));
                writer.write(',');
                writer.write(Double.toString(ks.statistic()));
                writer.write(',');
                writer.write(Double.toString((Double) ks.details().get("d_plus")));
                writer.write(',');
                writer.write(Double.toString((Double) ks.details().get("d_minus")));
                writer.write(',');
                writer.write(Double.toString(ks.pValue()));
                writer.write(',');
                writer.write(Double.toString(ks.alpha()));
                writer.write(',');
                writer.write(ks.decision());
                writer.write('\n');
            }
        }
    }

    private void exportPerformance(List<SimulationResult> results) throws IOException {
        Path path = performanceDir.resolve("timings.csv");
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write("N,generation_s,chi_square_s,kolmogorov_smirnov_s,pi_s,total_s\n");
            for (SimulationResult result : results) {
                TimingResult timing = result.timings();
                writer.write(Integer.toString(result.n()));
                writer.write(',');
                writer.write(Double.toString(timing.generationSeconds()));
                writer.write(',');
                writer.write(Double.toString(timing.chiSquareSeconds()));
                writer.write(',');
                writer.write(Double.toString(timing.kolmogorovSmirnovSeconds()));
                writer.write(',');
                writer.write(Double.toString(timing.piSeconds()));
                writer.write(',');
                writer.write(Double.toString(timing.totalSeconds()));
                writer.write('\n');
            }
        }
    }

    private void exportSummary(List<SimulationResult> results) throws IOException {
        Path path = summaryDir.resolve("pi_table.csv");
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write("N,pi_estimado,error,tiempo_s\n");
            for (SimulationResult result : results) {
                writer.write(Integer.toString(result.n()));
                writer.write(',');
                writer.write(Double.toString(result.piEstimate()));
                writer.write(',');
                writer.write(Double.toString(result.piError()));
                writer.write(',');
                writer.write(Double.toString(result.timings().totalSeconds()));
                writer.write('\n');
            }
        }
    }
}
