from observer.observer import Observer


class Tabla(Observer): # Nuestra tabla hereda de observer

    def actualizar(self, resultados):
        print("\nTABLA DE RESULTADOS")
        print("-" * 30)
        print(f"{'Tiempo':<10}{'Población':<15}")

        for tiempo, poblacion in enumerate(resultados):
            print(f"{tiempo:<10}{poblacion:<15.2f}")