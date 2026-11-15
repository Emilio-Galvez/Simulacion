package simulation.models;

/** Estados enteros y valores uniformes generados por el LCG. */
public record GenerationResult(long[] states, double[] uniforms) {

    public int count() {
        return states.length;
    }
}
