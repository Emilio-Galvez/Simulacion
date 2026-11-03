package com.simulacion;

import com.simulacion.datos.ExportadorCSV;
import com.simulacion.datos.FilaComparacion;
import com.simulacion.estrategias.EstrategiaLCG;
import com.simulacion.servicios.Analisis;
import com.simulacion.servicios.Comparador;
import com.simulacion.servicios.ServicioLCG;
import com.simulacion.datos.Configuracion;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DisplayName("Analisis, comparacion y capa de datos")
class ServiciosTest {

    private static final int CANTIDAD_ESPERADA = 10000;
    private static final long MODULO = 4294967296L;

    @Test
    @DisplayName("Los parametros cumplen las condiciones de Hull-Dobell")
    void hullDobell() {
        Analisis.ResultadoHullDobell verificacion =
                Analisis.verificarHullDobell(1664525L, 1013904223L, MODULO);
        assertTrue(verificacion.cumplePeriodoCompleto());
        assertEquals(MODULO, verificacion.periodoTeorico());
        assertEquals(3, verificacion.condiciones().size());
    }

    @Test
    @DisplayName("Un incremento par impide alcanzar el periodo completo")
    void hullDobellIncumple() {
        Analisis.ResultadoHullDobell verificacion =
                Analisis.verificarHullDobell(1664525L, 1013904222L, MODULO);
        assertFalse(verificacion.cumplePeriodoCompleto());
        assertEquals(0L, verificacion.periodoTeorico());
    }

    @Test
    @DisplayName("Los factores primos de 2^32 son correctos")
    void factoresPrimos() {
        assertEquals(List.of(2L), Analisis.factoresPrimos(MODULO));
    }

    @Test
    @DisplayName("No se detecta ciclo empirico en 10000 muestras")
    void periodoEmpirico() {
        EstrategiaLCG generador = new EstrategiaLCG();
        assertNull(Analisis.periodoEmpirico(generador, CANTIDAD_ESPERADA));
    }

    @Test
    @DisplayName("Las estadisticas de la simulacion son razonables")
    void estadisticas() {
        ServicioLCG servicio = new ServicioLCG(Configuracion.porDefecto());
        Analisis.Estadisticas estadisticas = Analisis.estadisticas(servicio.simularNormalizados(null));
        assertEquals(CANTIDAD_ESPERADA, estadisticas.cantidad());
        assertTrue(Math.abs(estadisticas.media() - 0.5) < 0.02);
        assertTrue(Math.abs(estadisticas.varianza() - 1.0 / 12.0) < 0.01);
        assertTrue(estadisticas.minimo() >= 0.0 && estadisticas.maximo() < 1.0);
    }

    @Test
    @DisplayName("La prueba chi-cuadrado no rechaza la uniformidad")
    void chiCuadrado() {
        ServicioLCG servicio = new ServicioLCG(Configuracion.porDefecto());
        Analisis.ResultadoChiCuadrado prueba =
                Analisis.pruebaChiCuadrado(servicio.simularNormalizados(null), 20, 0.95);
        assertEquals(19, prueba.gradosLibertad());
        assertFalse(prueba.rechazaHipotesis());
        int total = 0;
        for (int frecuencia : prueba.frecuenciasObservadas()) {
            total += frecuencia;
        }
        assertEquals(CANTIDAD_ESPERADA, total);
    }

    @Test
    @DisplayName("Dos secuencias identicas se reportan como identicas")
    void comparacionIdentica() {
        long[] estados = new ServicioLCG(Configuracion.porDefecto()).simular(null);
        Comparador.ResultadoComparacion resultado = Comparador.compararSecuencias(estados, estados.clone());
        assertTrue(resultado.identicas());
        assertEquals(CANTIDAD_ESPERADA, resultado.totalComparadas());
    }

    @Test
    @DisplayName("Dos semillas distintas producen secuencias distintas")
    void comparacionSemillasDistintas() {
        ServicioLCG servicio = new ServicioLCG(Configuracion.porDefecto());
        Comparador.ResultadoComparacion resultado =
                Comparador.compararSecuencias(servicio.simular(12345L), servicio.simular(54321L));
        assertFalse(resultado.identicas());
        assertEquals(0, resultado.diferencias().get(0).indice());
    }

    @Test
    @DisplayName("El formato normalizado es exacto y coincide con Python")
    void formatoNormalizado() {
        assertEquals("0.000488281250", ExportadorCSV.formatearNormalizadoExacto(2097152L, MODULO));
        assertEquals("0.000000000000", ExportadorCSV.formatearNormalizadoExacto(0L, MODULO));
        assertEquals("0.999999999767", ExportadorCSV.formatearNormalizadoExacto(MODULO - 1, MODULO));

        BigDecimal esperado = BigDecimal.valueOf(87628868L)
                .divide(BigDecimal.valueOf(MODULO), 12, java.math.RoundingMode.DOWN);
        assertEquals(esperado.toPlainString(), ExportadorCSV.formatearNormalizadoExacto(87628868L, MODULO));
    }

    @Test
    @DisplayName("El CSV de resultados se genera correctamente")
    void exportarResultados(@TempDir Path temporal) throws IOException {
        long[] estados = new ServicioLCG(Configuracion.porDefecto()).simular(null);
        Path ruta = temporal.resolve("resultados_java.csv");
        ExportadorCSV.exportarResultados(ruta, estados, MODULO);
        assertTrue(Files.isRegularFile(ruta));

        List<String> lineas = Files.readAllLines(ruta);
        assertEquals("indice,x,normalizado", lineas.get(0));
        assertEquals(CANTIDAD_ESPERADA + 1, lineas.size());
        assertEquals("1," + estados[0] + "," + ExportadorCSV.formatearNormalizadoExacto(estados[0], MODULO),
                lineas.get(1));
    }

    @Test
    @DisplayName("El CSV se puede leer desde disco")
    void leerResultados(@TempDir Path temporal) throws IOException {
        long[] estados = new ServicioLCG(Configuracion.porDefecto()).simular(null);
        Path ruta = temporal.resolve("resultados_java.csv");
        ExportadorCSV.exportarResultados(ruta, estados, MODULO);
        assertArrayEqualsHelper(estados, ExportadorCSV.leerEstados(ruta));
    }

    @Test
    @DisplayName("El CSV de comparacion se genera correctamente")
    void exportarComparacion(@TempDir Path temporal) throws IOException {
        long[] estados = new ServicioLCG(Configuracion.porDefecto()).simular(null);
        List<FilaComparacion> tabla = Comparador.tablaPrimerasObservaciones(estados, estados.clone(), MODULO, 20);
        Path ruta = temporal.resolve("comparacion.csv");
        ExportadorCSV.exportarComparacion(ruta, tabla);
        List<String> lineas = Files.readAllLines(ruta);
        assertEquals("indice,x_python,x_java,u_python,u_java,coincide", lineas.get(0));
        assertEquals(21, lineas.size());
        assertTrue(lineas.get(1).endsWith(",si"));
    }

    private static void assertArrayEqualsHelper(long[] esperado, long[] obtenido) {
        assertEquals(esperado.length, obtenido.length);
        for (int indice = 0; indice < esperado.length; indice++) {
            assertEquals(esperado[indice], obtenido[indice], "Diferencia en el indice " + indice);
        }
    }
}
