import numpy as np
import matplotlib.pyplot as plt
import random

class ProblemaRectangulos:
    def __init__(self, superrectangulo, subrectangulos):
        self.superrectangulo = superrectangulo
        self.subrectangulos = subrectangulos
        self.penalizacion_solapamiento = 1000  # Valor de penalización alto

    def calcular_desperdicio(self, solucion):
        altura_utilizada = max(y + alto for _, y, alto, _ in solucion)
        area_superrectangulo = self.superrectangulo[0] * altura_utilizada
        area_ocupada = sum([alto * ancho for _, _, alto, ancho in solucion])
        desperdicio = max(0, area_superrectangulo - area_ocupada)

        if self.hay_solapamiento(solucion):
            desperdicio += self.penalizacion_solapamiento

        return desperdicio, altura_utilizada

    def generar_solucion_aleatoria(self):
        solucion = []
        for alto, ancho in self.subrectangulos:
            x = np.random.randint(0, self.superrectangulo[0] - ancho + 1)
            y_max = max(1, self.superrectangulo[1] - alto + 1)
            y = np.random.randint(0, y_max)
            solucion.append((x, y, alto, ancho))
        return solucion

    def generar_vecino(self, solucion):
        vecino = solucion.copy()
        idx = random.randint(0, len(vecino) - 1)
        alto, ancho = self.subrectangulos[idx]
        x = np.random.randint(0, self.superrectangulo[0] - ancho + 1)
        y_max = max(1, self.superrectangulo[1] - alto + 1)
        y = np.random.randint(0, y_max)
        vecino[idx] = (x, y, alto, ancho)
        return vecino

    def evaluar(self, solucion):
        desperdicio, altura_utilizada = self.calcular_desperdicio(solucion)
        penalizacion = self.calcular_penalizacion(solucion)
        return desperdicio, penalizacion, altura_utilizada


    def calcular_penalizacion(self, solucion):
        if self.hay_solapamiento(solucion):
            return self.penalizacion_solapamiento
        return 0

    def hay_solapamiento(self, solucion):
        for i in range(len(solucion)):
            x1, y1, alto1, ancho1 = solucion[i]
            for j in range(i + 1, len(solucion)):
                x2, y2, alto2, ancho2 = solucion[j]
                if not (x1 + ancho1 <= x2 or x2 + ancho2 <= x1 or y1 + alto1 <= y2 or y2 + alto2 <= y1):
                    return True
        return False

# Parámetros
n_subrectangulos = 5
ancho_superrectangulo = 100
alto_superrectangulo = 100
max_generaciones = 1000
tabu_tenure = 5

# Generar subrectángulos aleatorios
subrectangulos = [(np.random.randint(1, 50), np.random.randint(1, 50)) for _ in range(n_subrectangulos)]

# Función para graficar la solución
def graficar_solucion(solucion, superrectangulo):
    fig, ax = plt.subplots()
    ax.set_xlim(0, superrectangulo[0])
    ax.set_ylim(0, superrectangulo[1])
    for x, y, alto, ancho in solucion:
        rect = plt.Rectangle((x, y), ancho, alto, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    plt.show()

# Función para calcular la altura mínima requerida
def altura_minima_requerida(solucion):
    return max(y + alto for _, y, alto, _ in solucion)

# Ejemplo de búsqueda tabú
mejor_solucion = None
mejor_desperdicio = float('inf')
historial_desperdicio = []
historial_penalizacion = []
tabu_list = []

problema = ProblemaRectangulos((ancho_superrectangulo, alto_superrectangulo), subrectangulos)
solucion_actual = problema.generar_solucion_aleatoria()

for _ in range(max_generaciones):
    vecinos = [problema.generar_vecino(solucion_actual) for _ in range(10)]
    vecinos = [vec for vec in vecinos if vec not in tabu_list]
    
    if not vecinos:
        continue

    vecino_actual = min(vecinos, key=lambda vec: problema.evaluar(vec)[0])
    desperdicio_actual, penalizacion_actual, altura_utilizada_actual = problema.evaluar(vecino_actual)
    historial_desperdicio.append(desperdicio_actual)
    historial_penalizacion.append(penalizacion_actual)

    if desperdicio_actual < mejor_desperdicio:
        mejor_desperdicio = desperdicio_actual
        mejor_solucion = vecino_actual
        mejor_penalizacion = penalizacion_actual

    tabu_list.append(vecino_actual)
    if len(tabu_list) > tabu_tenure:
        tabu_list.pop(0)

    solucion_actual = vecino_actual
    problema.superrectangulo = (ancho_superrectangulo, altura_utilizada_actual)  # Ajustar la altura del superrectángulo dinámicamente

# Visualizar la mejor solución encontrada
print("Mejor solución encontrada:")
print(mejor_solucion)
# Estructura mejor solucion (super rectangulo formado por subrectangulos)
# Cada subrectangulo es una tupla del tipo (x,y,alto,ancho)
# x e y son las coordenadas horizontal y vertical de la esquina inferior izquierda del subrectángulo dentro del superrectángulo.
# alto y ancho son la altura y anchura del subrectangulo..


print("Desperdicio:", mejor_desperdicio)
print("Penalización por solapamiento:", mejor_penalizacion)

graficar_solucion(mejor_solucion, (ancho_superrectangulo, altura_minima_requerida(mejor_solucion)))

# Visualizar historial de desperdicio
plt.plot(historial_desperdicio, label='Desperdicio')
plt.plot(historial_penalizacion, label='Penalización')
plt.xlabel('Generación')
plt.ylabel('Desperdicio / Penalización')
plt.title('Desperdicio y Penalización a lo largo de las generaciones')
plt.legend()
plt.show()
