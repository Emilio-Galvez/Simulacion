package simulation.config;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

/** Configuracion compartida leida desde config/simulation.properties. */
public record Config(
        long seed,
        List<Integer> sampleSizes,
        int repetitions,
        int warmupSize,
        double realPi,
        Path configPath,
        Path projectRoot) {

    public Config {
        sampleSizes = List.copyOf(sampleSizes);
        validate(sampleSizes, repetitions, warmupSize, realPi);
    }

    private static void validate(
            List<Integer> sampleSizes, int repetitions, int warmupSize, double realPi) {
        if (sampleSizes.isEmpty() || sampleSizes.stream().anyMatch(n -> n <= 0)) {
            throw new IllegalArgumentException("Los tamanos de muestra deben ser positivos.");
        }
        if (repetitions <= 0) {
            throw new IllegalArgumentException("El numero de repeticiones debe ser positivo.");
        }
        if (warmupSize <= 0) {
            throw new IllegalArgumentException("El tamano de calentamiento debe ser positivo.");
        }
        if (realPi <= 3.0 || realPi >= 3.2) {
            throw new IllegalArgumentException("El valor de pi real no es plausible.");
        }
    }

    public Path resultsDir() {
        return projectRoot.resolve("results").resolve("java");
    }

    public static Config load() {
        String configured = System.getProperty("mc.config");
        if (configured != null && !configured.isBlank()) {
            return load(Path.of(configured));
        }

        List<Path> candidates = List.of(
                Path.of("config", "simulation.properties"),
                Path.of("..", "config", "simulation.properties"),
                Path.of("..", "..", "config", "simulation.properties"));
        for (Path candidate : candidates) {
            if (Files.exists(candidate)) {
                return load(candidate);
            }
        }
        throw new IllegalStateException(
                "No se encontro config/simulation.properties. Use -Dmc.config=<ruta>.");
    }

    public static Config load(Path path) {
        Path absolute = path.toAbsolutePath().normalize();
        if (!Files.exists(absolute)) {
            throw new IllegalArgumentException("No existe el archivo de configuracion: " + absolute);
        }

        Properties properties = new Properties();
        try (InputStream input = Files.newInputStream(absolute)) {
            properties.load(input);
        } catch (IOException exception) {
            throw new IllegalStateException("No se pudo leer " + absolute, exception);
        }

        try {
            List<Integer> sizes = new ArrayList<>();
            for (String token : properties.getProperty("sample.sizes").split(",")) {
                if (!token.isBlank()) {
                    sizes.add(Integer.parseInt(token.trim()));
                }
            }
            return new Config(
                    Long.parseLong(properties.getProperty("seed").trim()),
                    sizes,
                    Integer.parseInt(properties.getProperty("repetitions").trim()),
                    Integer.parseInt(properties.getProperty("warmup.size").trim()),
                    Double.parseDouble(properties.getProperty("real.pi").trim()),
                    absolute,
                    absolute.getParent().getParent());
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Valor numerico invalido en " + absolute, exception);
        }
    }
}
