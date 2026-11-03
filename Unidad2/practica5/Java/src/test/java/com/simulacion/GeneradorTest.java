package com.simulacion;

import com.simulacion.estrategias.EstrategiaLCG;
import com.simulacion.estrategias.Generador;
import com.simulacion.estrategias.ParametrosInvalidosException;
import com.simulacion.fabricas.FabricaGenerador;
import com.simulacion.servicios.ServicioLCG;
import com.simulacion.datos.Configuracion;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DisplayName("Estrategia LCG, fabricas y servicio de dominio")
class GeneradorTest {

    private static final int CANTIDAD_ESPERADA = 10000;
    private static final long MODULO = 4294967296L;
    private static final long[] PRIMEROS_ESTADOS_ESPERADOS =
            {87628868L, 71072467L, 2332836374L, 2726892157L, 3908547000L};

    @Test
    @DisplayName("Los parametros por defecto son los exigidos por la practica")
    void parametrosPorDefecto() {
        EstrategiaLCG generador = new EstrategiaLCG();
        assertEquals(1664525L, generador.getMultiplicador());
        assertEquals(1013904223L, generador.getIncremento());
        assertEquals(MODULO, generador.getModulo());
        assertEquals(12345L, generador.getSemilla());
    }

    @Test
    @DisplayName("Los parametros invalidos se rechazan")
    void parametrosInvalidos() {
        assertThrows(ParametrosInvalidosException.class, () -> new EstrategiaLCG(0, 1013904223L, MODULO, 1));
        assertThrows(ParametrosInvalidosException.class,
                () -> new EstrategiaLCG(1664525L, 1013904223L, 1, 1));
        assertThrows(ParametrosInvalidosException.class,
                () -> new EstrategiaLCG(1664525L, MODULO, MODULO, 1));
        assertThrows(ParametrosInvalidosException.class,
                () -> new EstrategiaLCG(1664525L, 1013904223L, MODULO, MODULO));
        assertThrows(ParametrosInvalidosException.class, () -> new EstrategiaLCG().generar(-1));
    }

    @Test
    @DisplayName("Se generan exactamente 10000 valores")
    void cantidadDeValores() {
        assertEquals(CANTIDAD_ESPERADA, new EstrategiaLCG().generar(CANTIDAD_ESPERADA).length);
    }

    @Test
    @DisplayName("Los primeros estados coinciden con los calculados por referencia")
    void primerosEstados() {
        long[] estados = new EstrategiaLCG().generar(5);
        assertArrayEquals(PRIMEROS_ESTADOS_ESPERADOS, estados);
    }

    @Test
    @DisplayName("Todos los valores normalizados pertenecen a [0, 1)")
    void valoresNormalizadosEnRango() {
        double[] normalizados = new EstrategiaLCG().generarNormalizados(CANTIDAD_ESPERADA);
        assertEquals(CANTIDAD_ESPERADA, normalizados.length);
        for (double valor : normalizados) {
            assertTrue(valor >= 0.0 && valor < 1.0, "Valor fuera de rango: " + valor);
        }
    }

    @Test
    @DisplayName("La normalizacion usa la relacion U(n) = X(n)/m")
    void relacionDeNormalizacion() {
        EstrategiaLCG generador = new EstrategiaLCG();
        long[] estados = generador.generar(10);
        double[] normalizados = generador.generarNormalizados(10);
        for (int indice = 0; indice < estados.length; indice++) {
            assertEquals((double) estados[indice] / (double) MODULO, normalizados[indice]);
        }
    }

    @Test
    @DisplayName("La generacion es determinista")
    void generacionDeterminista() {
        assertArrayEquals(new EstrategiaLCG().generar(100), new EstrategiaLCG().generar(100));
    }

    @Test
    @DisplayName("Cambiar la semilla produce una secuencia distinta")
    void semillaDistintaProduceSecuenciaDistinta() {
        long[] original = new EstrategiaLCG().generar(CANTIDAD_ESPERADA);
        long[] alternativa = new EstrategiaLCG(1664525L, 1013904223L, MODULO, 54321L)
                .generar(CANTIDAD_ESPERADA);
        assertNotEquals(original[0], alternativa[0]);
        assertFalse(java.util.Arrays.equals(original, alternativa));
    }

    @Test
    @DisplayName("La fabrica crea la estrategia LCG (patron Factory Method)")
    void fabricaCreaGenerador() {
        Generador generador = FabricaGenerador.crear("LCG");
        assertInstanceOf(EstrategiaLCG.class, generador);
        assertInstanceOf(Generador.class, generador);
    }

    @Test
    @DisplayName("La fabrica aplica los parametros recibidos")
    void fabricaAplicaParametros() {
        Generador generador = FabricaGenerador.crear("LCG",
                new com.simulacion.estrategias.ParametrosGenerador(1664525L, 1013904223L, MODULO, 777L));
        assertEquals(777L, generador.getSemilla());
    }

    @Test
    @DisplayName("Un tipo de generador desconocido produce un error de negocio")
    void tipoDesconocido() {
        assertThrows(FabricaGenerador.TipoGeneradorDesconocidoException.class,
                () -> FabricaGenerador.crear("MERSENNE"));
    }

    @Test
    @DisplayName("El servicio de dominio genera la cantidad configurada")
    void servicioDeDominio() {
        ServicioLCG servicio = new ServicioLCG(Configuracion.porDefecto());
        assertEquals(CANTIDAD_ESPERADA, servicio.simular(null).length);
        assertEquals(CANTIDAD_ESPERADA, servicio.simularNormalizados(null).length);
        assertEquals(12345L, servicio.crearGenerador(null).getSemilla());
    }
}
