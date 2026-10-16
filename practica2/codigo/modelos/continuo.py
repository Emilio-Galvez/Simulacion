from datos.datos_poblacion import P0, r, dt, tiempo

class ModeloContinuo:
     def simular(self):
          resultados = []
          poblacion = P0

          pasos = int(tiempo / dt) # Calculamos el numero de pasos que necesitamos

          for paso in range(pasos + 1):
               resultados.append(poblacion)

               cambio = r * poblacion
               poblacion = poblacion + dt * cambio
            
          return resultados