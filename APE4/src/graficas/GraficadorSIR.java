package graficas;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import javax.imageio.ImageIO;

public class GraficadorSIR {
    private static final int ANCHO = 1100;
    private static final int ALTO = 650;

    private static final Color[] COLORES_VARIABLE = {
        new Color(46, 125, 50),
        new Color(198, 40, 40),
        new Color(97, 97, 97)
    };
    private static final String[] NOMBRES_VARIABLE = {
        "Susceptibles", "Infectados", "Recuperados"
    };
    private static final Color COLOR_JAVA = new Color(21, 101, 192);
    private static final Color COLOR_NETLOGO = new Color(106, 27, 154);
    private static final Color GRIS = new Color(210, 210, 210);
    private static final Color TEXTO = new Color(35, 35, 35);

    private static final Font FUENTE_TITULO = new Font("SansSerif", Font.BOLD, 24);
    private static final Font FUENTE_SUBTITULO = new Font("SansSerif", Font.BOLD, 17);
    private static final Font FUENTE_NORMAL = new Font("SansSerif", Font.PLAIN, 14);
    private static final Font FUENTE_PEQUENA = new Font("SansSerif", Font.PLAIN, 12);

    static class Serie {
        final String nombre;
        final List<int[]> filas;

        Serie(String nombre, List<int[]> filas) {
            this.nombre = nombre;
            this.filas = filas;
        }

        int[] fila(int indice) {
            return filas.get(indice);
        }

        int tamano() {
            return filas.size();
        }
    }

    static class Area {
        final int x0;
        final int y0;
        final int x1;
        final int y1;

        Area(int x0, int y0, int x1, int y1) {
            this.x0 = x0;
            this.y0 = y0;
            this.x1 = x1;
            this.y1 = y1;
        }

        int px(int tiempo) {
            return x0 + (x1 - x0) * tiempo / 100;
        }

        int py(int valor) {
            return y1 - (y1 - y0) * valor / 100;
        }
    }

    public static void main(String[] args) {
        System.setProperty("java.awt.headless", "true");
        Path raiz = Path.of("").toAbsolutePath();
        Path resultados = raiz.resolve("resultados");
        Path graficas = raiz.resolve("graficas");

        try {
            Files.createDirectories(graficas);
            Serie java = leerCsv("Java", resultados.resolve("resultados_java.csv"));
            Serie netlogo = leerCsv("NetLogo", resultados.resolve("resultados_netlogo.csv"));

            dibujarEvolucion(java, graficas.resolve("evolucion_java.png"));
            dibujarEvolucion(netlogo, graficas.resolve("evolucion_netlogo.png"));
            dibujarComparacion(java, netlogo, graficas.resolve("comparacion_java_netlogo.png"));
            dibujarInfectados(java, netlogo, graficas.resolve("comparacion_infectados.png"));
            dibujarEstadosFinales(java, netlogo, graficas.resolve("estados_finales.png"));
            guardarResumen(java, netlogo, resultados.resolve("comparacion_resultados.csv"));

            System.out.println("Gráficas generadas en: " + graficas.toAbsolutePath());
            System.out.println("Resumen generado en: "
                    + resultados.resolve("comparacion_resultados.csv").toAbsolutePath());
        } catch (IOException e) {
            System.err.println("No se pudieron generar las gráficas: " + e.getMessage());
            System.exit(1);
        }
    }

    private static Serie leerCsv(String nombre, Path ruta) throws IOException {
        List<String> lineas = Files.readAllLines(ruta, StandardCharsets.UTF_8);
        List<int[]> filas = new ArrayList<>();

        for (int i = 1; i < lineas.size(); i++) {
            String linea = lineas.get(i).trim();
            if (linea.isEmpty()) {
                continue;
            }
            String[] partes = linea.split(",");
            filas.add(new int[] {
                Integer.parseInt(partes[0].trim()),
                Integer.parseInt(partes[1].trim()),
                Integer.parseInt(partes[2].trim()),
                Integer.parseInt(partes[3].trim())
            });
        }
        return new Serie(nombre, filas);
    }

    private static void dibujarEvolucion(Serie serie, Path salida) throws IOException {
        BufferedImage imagen = nuevaImagen(ANCHO, ALTO);
        Graphics2D g = preparar(imagen);
        Area area = new Area(100, 90, ANCHO - 60, ALTO - 90);

        dibujarTitulo(g, "Evolución del modelo SIR en " + serie.nombre, ANCHO / 2, 45);
        dibujarEjes(g, area);

        for (int variable = 0; variable < 3; variable++) {
            dibujarLinea(g, area, serie, variable + 1,
                    COLORES_VARIABLE[variable], trazoSolido(), false);
        }

        int leyendaX = area.x1 - 210;
        int leyendaY = area.y0 + 25;
        for (int variable = 0; variable < 3; variable++) {
            dibujarEntradaLeyenda(g, leyendaX, leyendaY + variable * 24,
                    COLORES_VARIABLE[variable], trazoSolido(), NOMBRES_VARIABLE[variable]);
        }

        g.dispose();
        ImageIO.write(imagen, "png", salida.toFile());
    }

    private static void dibujarComparacion(Serie java, Serie netlogo, Path salida) throws IOException {
        int alto = 1050;
        BufferedImage imagen = nuevaImagen(ANCHO, alto);
        Graphics2D g = preparar(imagen);

        dibujarTitulo(g, "Comparación del modelo SIR: Java vs NetLogo", ANCHO / 2, 42);

        int altoPanel = 280;
        int separacion = 45;
        int inicio = 80;

        for (int variable = 0; variable < 3; variable++) {
            int y0 = inicio + variable * (altoPanel + separacion);
            Area area = new Area(100, y0 + 35, ANCHO - 60, y0 + altoPanel);
            dibujarSubtitulo(g, NOMBRES_VARIABLE[variable], area.x0, y0 + 22);
            dibujarEjes(g, area);

            dibujarLinea(g, area, java, variable + 1, COLOR_JAVA, trazoSolido(), false);
            dibujarLinea(g, area, netlogo, variable + 1, COLOR_NETLOGO, trazoPunteado(), true);
        }

        int leyendaX = ANCHO - 260;
        int leyendaY = 78;
        dibujarEntradaLeyenda(g, leyendaX, leyendaY, COLOR_JAVA, trazoSolido(), "Java");
        dibujarEntradaLeyenda(g, leyendaX, leyendaY + 24, COLOR_NETLOGO, trazoPunteado(), "NetLogo");

        g.dispose();
        ImageIO.write(imagen, "png", salida.toFile());
    }

    private static void dibujarInfectados(Serie java, Serie netlogo, Path salida) throws IOException {
        BufferedImage imagen = nuevaImagen(ANCHO, ALTO);
        Graphics2D g = preparar(imagen);
        Area area = new Area(100, 90, ANCHO - 60, ALTO - 90);

        dibujarTitulo(g, "Infectados en cada paso: Java vs NetLogo", ANCHO / 2, 45);
        dibujarEjes(g, area);
        dibujarLinea(g, area, java, 2, COLOR_JAVA, trazoSolido(), false);
        dibujarLinea(g, area, netlogo, 2, COLOR_NETLOGO, trazoPunteado(), true);

        int leyendaX = area.x1 - 210;
        int leyendaY = area.y0 + 25;
        dibujarEntradaLeyenda(g, leyendaX, leyendaY, COLOR_JAVA, trazoSolido(), "Java");
        dibujarEntradaLeyenda(g, leyendaX, leyendaY + 24, COLOR_NETLOGO, trazoPunteado(), "NetLogo");

        g.dispose();
        ImageIO.write(imagen, "png", salida.toFile());
    }

    private static void dibujarEstadosFinales(Serie java, Serie netlogo, Path salida) throws IOException {
        BufferedImage imagen = nuevaImagen(950, 600);
        Graphics2D g = preparar(imagen);
        Area area = new Area(100, 90, 900, 510);

        dibujarTitulo(g, "Estado final de la población", 950 / 2, 45);
        dibujarEjes(g, area);

        int[] finalJava = java.fila(java.tamano() - 1);
        int[] finalNetlogo = netlogo.fila(netlogo.tamano() - 1);
        int anchoBarra = 70;
        int separacion = 18;
        int centroCategoria = (area.x1 - area.x0) / 3;

        for (int variable = 0; variable < 3; variable++) {
            int centro = area.x0 + centroCategoria * variable + centroCategoria / 2;
            int valorJava = finalJava[variable + 1];
            int valorNetlogo = finalNetlogo[variable + 1];

            dibujarBarra(g, centro - separacion / 2 - anchoBarra, area, valorJava,
                    COLOR_JAVA, String.valueOf(valorJava), anchoBarra);
            dibujarBarra(g, centro + separacion / 2, area, valorNetlogo,
                    COLOR_NETLOGO, String.valueOf(valorNetlogo), anchoBarra);

            g.setColor(TEXTO);
            g.setFont(FUENTE_NORMAL);
            String etiqueta = NOMBRES_VARIABLE[variable];
            int anchoTexto = g.getFontMetrics().stringWidth(etiqueta);
            g.drawString(etiqueta, centro - anchoTexto / 2, area.y1 + 28);
        }

        int leyendaX = area.x1 - 230;
        int leyendaY = area.y0 + 20;
        dibujarEntradaLeyenda(g, leyendaX, leyendaY, COLOR_JAVA, trazoSolido(), "Java");
        dibujarEntradaLeyenda(g, leyendaX, leyendaY + 24, COLOR_NETLOGO, trazoSolido(), "NetLogo");

        g.dispose();
        ImageIO.write(imagen, "png", salida.toFile());
    }

    private static void dibujarBarra(Graphics2D g, int x, Area area, int valor,
            Color color, String etiqueta, int ancho) {
        int altura = area.y1 - area.py(valor);
        g.setColor(color);
        g.fillRect(x, area.py(valor), ancho, altura);
        g.setColor(TEXTO);
        g.setFont(FUENTE_PEQUENA);
        int anchoTexto = g.getFontMetrics().stringWidth(etiqueta);
        g.drawString(etiqueta, x + ancho / 2 - anchoTexto / 2, area.py(valor) - 6);
    }

    private static void dibujarLinea(Graphics2D g, Area area, Serie serie, int columna,
            Color color, BasicStroke trazo, boolean punteado) {
        g.setColor(color);
        g.setStroke(trazo);
        int anteriorX = 0;
        int anteriorY = 0;
        boolean primero = true;

        for (int i = 0; i < serie.tamano(); i++) {
            int[] fila = serie.fila(i);
            int x = area.px(fila[0]);
            int y = area.py(fila[columna]);
            if (!primero) {
                g.drawLine(anteriorX, anteriorY, x, y);
            }
            anteriorX = x;
            anteriorY = y;
            primero = false;
        }
    }

    private static void dibujarEjes(Graphics2D g, Area area) {
        g.setFont(FUENTE_PEQUENA);
        g.setStroke(new BasicStroke(1f));

        for (int valor = 0; valor <= 100; valor += 10) {
            int x = area.px(valor);
            int y = area.py(valor);

            g.setColor(GRIS);
            g.drawLine(x, area.y0, x, area.y1);
            g.drawLine(area.x0, y, area.x1, y);

            g.setColor(TEXTO);
            String etiquetaX = String.valueOf(valor);
            g.drawString(etiquetaX, x - g.getFontMetrics().stringWidth(etiquetaX) / 2,
                    area.y1 + 20);
            String etiquetaY = String.valueOf(valor);
            g.drawString(etiquetaY, area.x0 - 12 - g.getFontMetrics().stringWidth(etiquetaY),
                    y + 4);
        }

        g.setColor(new Color(80, 80, 80));
        g.setStroke(new BasicStroke(1.5f));
        g.drawLine(area.x0, area.y0, area.x0, area.y1);
        g.drawLine(area.x0, area.y1, area.x1, area.y1);

        g.setFont(FUENTE_NORMAL);
        g.setColor(TEXTO);
        String etiquetaX = "Tiempo";
        g.drawString(etiquetaX, (area.x0 + area.x1) / 2
                - g.getFontMetrics().stringWidth(etiquetaX) / 2, area.y1 + 48);

        Graphics2D copia = (Graphics2D) g.create();
        copia.setFont(FUENTE_NORMAL);
        String etiquetaY = "Número de personas";
        int ancho = copia.getFontMetrics().stringWidth(etiquetaY);
        int centroY = (area.y0 + area.y1) / 2;
        copia.translate(30, centroY + ancho / 2);
        copia.rotate(-Math.PI / 2);
        copia.drawString(etiquetaY, 0, 0);
        copia.dispose();
    }

    private static void dibujarEntradaLeyenda(Graphics2D g, int x, int y,
            Color color, BasicStroke trazo, String texto) {
        g.setColor(Color.WHITE);
        g.fillRoundRect(x - 10, y - 16, 210, 22, 8, 8);
        g.setColor(color);
        g.setStroke(trazo);
        g.drawLine(x, y - 5, x + 32, y - 5);
        g.setColor(TEXTO);
        g.setFont(FUENTE_NORMAL);
        g.drawString(texto, x + 42, y);
    }

    private static BasicStroke trazoSolido() {
        return new BasicStroke(2.6f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND);
    }

    private static BasicStroke trazoPunteado() {
        return new BasicStroke(2.6f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND,
                10f, new float[] {10f, 6f}, 0f);
    }

    private static void dibujarTitulo(Graphics2D g, String texto, int x, int y) {
        g.setColor(TEXTO);
        g.setFont(FUENTE_TITULO);
        g.drawString(texto, x - g.getFontMetrics().stringWidth(texto) / 2, y);
    }

    private static void dibujarSubtitulo(Graphics2D g, String texto, int x, int y) {
        g.setColor(TEXTO);
        g.setFont(FUENTE_SUBTITULO);
        g.drawString(texto, x, y);
    }

    private static BufferedImage nuevaImagen(int ancho, int alto) {
        BufferedImage imagen = new BufferedImage(ancho, alto, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = imagen.createGraphics();
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, ancho, alto);
        g.dispose();
        return imagen;
    }

    private static Graphics2D preparar(BufferedImage imagen) {
        Graphics2D g = imagen.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        return g;
    }

    private static void guardarResumen(Serie java, Serie netlogo, Path salida) throws IOException {
        List<String> lineas = new ArrayList<>();
        lineas.add("herramienta,susceptibles_finales,infectados_finales,recuperados_finales,"
                + "pico_infectados,tiempo_pico,total_infectados,primer_tiempo_sin_infectados");
        lineas.add(resumen(java));
        lineas.add(resumen(netlogo));
        Files.write(salida, lineas, StandardCharsets.UTF_8);
    }

    private static String resumen(Serie serie) {
        int pico = 0;
        int tiempoPico = 0;
        Integer primerCero = null;

        for (int[] fila : serie.filas) {
            if (fila[2] > pico) {
                pico = fila[2];
                tiempoPico = fila[0];
            }
        }
        for (int[] fila : serie.filas) {
            if (fila[0] > tiempoPico && fila[2] == 0) {
                primerCero = fila[0];
                break;
            }
        }

        int[] ultima = serie.fila(serie.tamano() - 1);
        return String.join(",",
                serie.nombre,
                String.valueOf(ultima[1]),
                String.valueOf(ultima[2]),
                String.valueOf(ultima[3]),
                String.valueOf(pico),
                String.valueOf(tiempoPico),
                String.valueOf(100 - ultima[1]),
                primerCero == null ? "no" : String.valueOf(primerCero));
    }
}
