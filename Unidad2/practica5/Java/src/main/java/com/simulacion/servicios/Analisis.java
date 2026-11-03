package com.simulacion.servicios;

import com.simulacion.estrategias.Generador;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Servicio de analisis matematico y estadistico de las simulaciones.
 *
 * <p>Incluye la verificacion de las condiciones de Hull-Dobell, el calculo del
 * periodo teorico, la deteccion empirica de ciclos y las pruebas de uniformidad.</p>
 */
public final class Analisis {

    private static final double VALOR_CRITICO_CHI_CUADRADO_19 = 30.144;
    private static final double VALOR_CRITICO_CHI_CUADRADO_10 = 18.307;
    private static final double VALOR_CRITICO_CHI_CUADRADO_05 = 11.070;
    private static final double VALOR_CRITICO_CHI_CUADRADO_01 = 7.779;

    private Analisis() {
    }

    /** Condicion del teorema de Hull-Dobell. */
    public record CondicionHullDobell(String descripcion, boolean cumple, String detalle) {
    }

    /** Resultado de la verificacion de las condiciones de Hull-Dobell. */
    public record ResultadoHullDobell(long multiplicador, long incremento, long modulo,
                                      List<CondicionHullDobell> condiciones, long periodoTeorico) {

        public boolean cumplePeriodoCompleto() {
            return condiciones.stream().allMatch(CondicionHullDobell::cumple);
        }

        public String resumen() {
            return "Condiciones de Hull-Dobell: " + (cumplePeriodoCompleto() ? "CUMPLE" : "NO CUMPLE")
                    + " | Periodo teorico = " + String.format("%,d", periodoTeorico);
        }
    }

    /** Estadisticas descriptivas de una secuencia normalizada. */
    public record Estadisticas(int cantidad, double minimo, double maximo, double media,
                                double varianza, double desviacionEstandar, double suma) {
    }

    /** Resultado de la prueba de bondad de ajuste chi-cuadrado. */
    public record ResultadoChiCuadrado(double intervaloConfianza, int bins, int[] frecuenciasObservadas,
                                        double[] frecuenciasEsperadas, double estadistico,
                                        double valorCritico, int gradosLibertad, boolean rechazaHipotesis) {
    }

    /**
     * Devuelve los factores primos distintos de un numero.
     *
     * @param numero numero a factorizar
     * @return lista de factores primos
     */
    public static List<Long> factoresPrimos(long numero) {
        List<Long> factores = new ArrayList<>();
        if (numero < 2) {
            return factores;
        }
        long restante = numero;
        for (long divisor = 2; divisor * divisor <= restante; divisor += (divisor == 2 ? 1 : 2)) {
            if (restante % divisor == 0) {
                factores.add(divisor);
                while (restante % divisor == 0) {
                    restante /= divisor;
                }
            }
        }
        if (restante > 1) {
            factores.add(restante);
        }
        return factores;
    }

    /**
     * Verifica las tres condiciones de Hull-Dobell para alcanzar el periodo completo m.
     *
     * @param multiplicador coeficiente a
     * @param incremento    constante aditiva c
     * @param modulo        modulo m
     * @return resultado de la verificacion
     */
    public static ResultadoHullDobell verificarHullDobell(long multiplicador, long incremento, long modulo) {
        List<Long> factores = factoresPrimos(modulo);
        List<CondicionHullDobell> condiciones = new ArrayList<>();

        boolean cumpleIncremento = factores.stream().allMatch(factor -> incremento % factor == 1);
        condiciones.add(new CondicionHullDobell(
                "c - 1 debe ser divisible por cada factor primo de m",
                cumpleIncremento,
                "c = " + incremento + ", factores primos de m = " + factores
                        + ", c mod p = " + residuos(incremento, factores)));

        boolean cumpleMultiplicador = factores.stream().allMatch(factor -> multiplicador % factor == 1);
        condiciones.add(new CondicionHullDobell(
                "a - 1 debe ser divisible por cada factor primo de m",
                cumpleMultiplicador,
                "a = " + multiplicador + ", a mod p = " + residuos(multiplicador, factores)));

        if (modulo % 4 == 0) {
            condiciones.add(new CondicionHullDobell(
                    "a debe ser congruente con 1 modulo 4 (m divisible por 4)",
                    multiplicador % 4 == 1,
                    "a mod 4 = " + (multiplicador % 4)));
        }

        long periodo = condiciones.stream().allMatch(CondicionHullDobell::cumple) ? modulo : 0L;
        return new ResultadoHullDobell(multiplicador, incremento, modulo, List.copyOf(condiciones), periodo);
    }

    private static List<Long> residuos(long valor, List<Long> factores) {
        List<Long> residuos = new ArrayList<>();
        for (Long factor : factores) {
            residuos.add(valor % factor);
        }
        return residuos;
    }

    /**
     * Detecta empiricamente el ciclo del generador.
     *
     * @param generador generador bajo analisis
     * @param limite    maxima cantidad de estados a evaluar
     * @return longitud del ciclo o {@code null} si no se detecta repeticion
     */
    public static Long periodoEmpirico(Generador generador, int limite) {
        Map<Long, Integer> vistos = new LinkedHashMap<>();
        long estado = generador.getSemilla();
        for (int indice = 0; indice < limite; indice++) {
            Integer anterior = vistos.put(estado, indice);
            if (anterior != null) {
                return (long) (indice - anterior);
            }
            estado = (generador.getMultiplicador() * estado + generador.getIncremento()) % generador.getModulo();
        }
        return null;
    }

    /**
     * Calcula estadisticas descriptivas de los valores normalizados.
     *
     * @param valores secuencia normalizada
     * @return estadisticas calculadas
     */
    public static Estadisticas estadisticas(double[] valores) {
        if (valores.length == 0) {
            return new Estadisticas(0, Double.NaN, Double.NaN, Double.NaN, Double.NaN, Double.NaN, 0.0);
        }
        double minimo = valores[0];
        double maximo = valores[0];
        double suma = 0.0;
        for (double valor : valores) {
            minimo = Math.min(minimo, valor);
            maximo = Math.max(maximo, valor);
            suma += valor;
        }
        double media = suma / valores.length;
        double varianza = 0.0;
        for (double valor : valores) {
            varianza += Math.pow(valor - media, 2);
        }
        varianza /= valores.length;
        return new Estadisticas(valores.length, minimo, maximo, media, varianza, Math.sqrt(varianza), suma);
    }

    /**
     * Prueba de uniformidad chi-cuadrado sobre el intervalo [0, 1).
     *
     * @param valores             secuencia normalizada
     * @param bins                cantidad de intervalos
     * @param intervaloConfianza  nivel de confianza (0.95)
     * @return resultado de la prueba
     */
    public static ResultadoChiCuadrado pruebaChiCuadrado(double[] valores, int bins, double intervaloConfianza) {
        if (bins < 2) {
            throw new IllegalArgumentException("El numero de intervalos debe ser mayor o igual a 2.");
        }
        if (valores.length == 0) {
            throw new IllegalArgumentException("La secuencia debe contener al menos un valor.");
        }
        int[] frecuencias = new int[bins];
        for (double valor : valores) {
            int indice = (int) Math.min(Math.floor(valor * bins), bins - 1);
            frecuencias[indice]++;
        }
        double esperada = (double) valores.length / bins;
        double estadistico = 0.0;
        for (int frecuencia : frecuencias) {
            estadistico += Math.pow(frecuencia - esperada, 2) / esperada;
        }
        int gradosLibertad = bins - 1;
        double valorCritico = valorCritico(gradosLibertad, intervaloConfianza);
        double[] esperadas = new double[bins];
        java.util.Arrays.fill(esperadas, esperada);
        return new ResultadoChiCuadrado(intervaloConfianza, bins, frecuencias, esperadas,
                estadistico, valorCritico, gradosLibertad, estadistico > valorCritico);
    }

    private static double valorCritico(int gradosLibertad, double intervaloConfianza) {
        if (intervaloConfianza == 0.95) {
            if (gradosLibertad >= 19) {
                return VALOR_CRITICO_CHI_CUADRADO_19;
            }
            if (gradosLibertad >= 9) {
                return VALOR_CRITICO_CHI_CUADRADO_10;
            }
            if (gradosLibertad >= 4) {
                return VALOR_CRITICO_CHI_CUADRADO_05;
            }
            return VALOR_CRITICO_CHI_CUADRADO_01;
        }
        return gradosLibertad >= 19 ? VALOR_CRITICO_CHI_CUADRADO_19 : VALOR_CRITICO_CHI_CUADRADO_05;
    }
}
