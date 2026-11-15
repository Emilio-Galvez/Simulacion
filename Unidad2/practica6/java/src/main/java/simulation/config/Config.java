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
        long multiplier,
        long increment,
        long modulus,
        double alpha,
        int bins,
        List<Integer> sampleSizes,
        Path configPath,
        Path projectRoot) {

    public Config {
        sampleSizes = List.copyOf(sampleSizes);
        validate(seed, multiplier, increment, modulus, alpha, bins, sampleSizes);
    }

    private static void validate(
            long seed,
            long multiplier,
            long increment,
            long modulus,
            double alpha,
            int bins,
            List<Integer> sampleSizes) {
        if (modulus <= 1) {
            throw new IllegalArgumentException("El modulo debe ser mayor que 1.");
        }
        if (seed < 0 || seed >= modulus) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < modulo.");
        }
        if (multiplier <= 0 || multiplier >= modulus) {
            throw new IllegalArgumentException("El multiplicador debe cumplir 0 < a < modulo.");
        }
        if (increment < 0 || increment >= modulus) {
            throw new IllegalArgumentException("El incremento debe cumplir 0 <= c < modulo.");
        }
        if (alpha <= 0.0 || alpha >= 1.0) {
            throw new IllegalArgumentException("alpha debe estar en (0, 1).");
        }
        if (bins <= 1) {
            throw new IllegalArgumentException("El numero de intervalos debe ser mayor que 1.");
        }
        if (sampleSizes.isEmpty() || sampleSizes.stream().anyMatch(n -> n <= 0)) {
            throw new IllegalArgumentException("Los tamanos de muestra deben ser positivos.");
        }
    }

    public Path resultsDir() {
        return projectRoot.resolve("java").resolve("results");
    }

    public static Config load() {
        String configured = System.getProperty("sim.config");
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
                "No se encontro config/simulation.properties. Use -Dsim.config=<ruta>.");
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
                    Long.parseLong(properties.getProperty("multiplier").trim()),
                    Long.parseLong(properties.getProperty("increment").trim()),
                    Long.parseLong(properties.getProperty("modulus").trim()),
                    Double.parseDouble(properties.getProperty("alpha").trim()),
                    Integer.parseInt(properties.getProperty("bins").trim()),
                    sizes,
                    absolute,
                    absolute.getParent().getParent());
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Valor numerico invalido en " + absolute, exception);
        }
    }
}
