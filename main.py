from abc import ABC, abstractmethod
import time

# Definición de la clase base abstracta Vehiculo
class Vehiculo(ABC):
    def __init__(self, velocidad_maxima, capacidad_gasolina, conductor):
        self.velocidad_maxima = velocidad_maxima
        self.capacidad_gasolina = capacidad_gasolina
        self.conductor = conductor
        self.velocidad_actual = 0
        self.gasolina_actual = capacidad_gasolina
        self.kilometraje = 0
        self.puntos = 0

    # Métodos abstractos que deben ser implementados por las clases hijas
    @abstractmethod
    def acelerar(self):
        pass

    @abstractmethod
    def frenar(self):
        pass

    @abstractmethod
    def recorrido(self, tiempo):
        pass

    # Método para repostar gasolina del vehículo
    def repostar_gasolina(self):
        self.gasolina_actual = self.capacidad_gasolina

# Definición de la clase Coche que hereda de Vehiculo
class Coche(Vehiculo):
    def acelerar(self):
        if self.gasolina_actual > 0:
            self.velocidad_actual += 10
            self.gasolina_actual -= 1

    def frenar(self):
        if self.velocidad_actual > 0:
            self.velocidad_actual -= 10

    def recorrido(self, tiempo):
        return self.velocidad_actual * tiempo

# Definición de la clase Moto que hereda de Vehiculo
class Moto(Vehiculo):
    def acelerar(self):
        if self.gasolina_actual > 0:
            self.velocidad_actual += 5
            self.gasolina_actual -= 0.5

    def frenar(self):
        if self.velocidad_actual > 0:
            self.velocidad_actual -= 5

    def recorrido(self, tiempo):
        return self.velocidad_actual * tiempo

# Definición de un decorador para agregar la funcionalidad de turbo a los vehículos
def turbo_decorator(vehiculo_class):
    class TurboVehiculo(vehiculo_class):
        def __init__(self, velocidad_maxima, capacidad_gasolina, conductor):
            super().__init__(velocidad_maxima, capacidad_gasolina, conductor)
            self.turbo_activado = False

        def activar_turbo(self):
            self.turbo_activado = True
            self.velocidad_maxima *= 2

        def desactivar_turbo(self):
            self.turbo_activado = False
            self.velocidad_maxima /= 2

        def acelerar(self):
            if self.gasolina_actual > 0:
                if self.turbo_activado:
                    self.velocidad_actual += 20
                else:
                    super().acelerar()

        def frenar(self):
            if self.velocidad_actual > 0:
                if self.turbo_activado:
                    self.velocidad_actual -= 20
                else:
                    super().frenar()

    return TurboVehiculo

# Definición de la clase Carrera
class Carrera:
    def __init__(self, distancia_pista, duracion_carrera):
        self.distancia_pista = distancia_pista
        self.duracion_carrera = duracion_carrera
        self.vehiculos = []
        self.ranking=[]

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def iniciar_carrera(self):
        tiempo_inicio = time.time()

        while time.time() - tiempo_inicio < self.duracion_carrera:
            for vehiculo in self.vehiculos:
                vehiculo.acelerar()
                vehiculo.frenar()
                distancia_recorrida = vehiculo.velocidad_maxima*(time.time() - tiempo_inicio)
                vehiculo.kilometraje += distancia_recorrida
                if vehiculo.kilometraje >= self.distancia_pista  and vehiculo.puntos == 0:
                    vehiculo.puntos = time.time() - tiempo_inicio
                    self.ranking.append((vehiculo.conductor, vehiculo.puntos))

            time.sleep(1)

        # Después de que la carrera termine, verificar si algún vehículo ha completado la carrera y otorgar puntos
        for vehiculo in self.vehiculos:
            if vehiculo.kilometraje >= self.distancia_pista  and vehiculo.puntos == 0:
                vehiculo.puntos = time.time() - tiempo_inicio
                self.ranking.append((vehiculo.conductor, vehiculo.puntos))

# Aplica el decorador directamente a la clase Coche
Coche = turbo_decorator(Coche)

# Ejemplo de uso
coche1 = Coche(1000, 50, "carlos")
coche2 = Coche(180, 40, "Julian")
moto1 = Moto(150, 30, "Juan pablo")

carrera = Carrera(1000, 3)  # Distancia de la pista: 1000 metros, Duración de la carrera: 3 segundos
carrera.agregar_vehiculo(coche1)
carrera.agregar_vehiculo(coche2)
carrera.agregar_vehiculo(moto1)

carrera.iniciar_carrera()

# Imprimir el ranking de la carrera
for i in range(len(carrera.ranking)):
    print("Lugar", i+1, "-->", "Corredor:", carrera.ranking[i][0], ", Tiempo de Carrera:", carrera.ranking[i][1])

