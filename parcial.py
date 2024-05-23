import numpy as np
import matplotlib.pyplot as plt

class ProblemaRectangulos:
    def __init__(self, superrectangulo, subrectangulos):
        self.superrectangulo = superrectangulo
        self.subrectangulos = subrectangulos

    def calcular_desperdicio(self, solucion):
        area_superrectangulo = self.superrectangulo[0] * self.superrectangulo[1]
        area_ocupada = sum([alto * ancho for _, _, alto, ancho in solucion])
        desperdicio = max(0, area_superrectangulo - area_ocupada)  # Asegurarse de que el desperdicio no sea negativo
        return desperdicio

    def generar_solucion_aleatoria(self):
        solucion = []
        for alto, ancho in self.subrectangulos:
            x = np.random.randint(0, self.superrectangulo[0] - alto + 1)
            y_max = max(1, self.superrectangulo[1] - ancho + 1)  # Asegurarse de que la altura mínima sea al menos 1
            y = np.random.randint(0, y_max)
            solucion.append((x, y, alto, ancho))
        return solucion

    def evaluar(self, solucion):
        return self.calcular_desperdicio(solucion)

# Parámetros
n_subrectangulos = 10
ancho_superrectangulo = 100
max_generaciones = 1000

# Generar subrectángulos aleatorios
subrectangulos = [(np.random.randint(1, 11), ancho_superrectangulo) for _ in range(n_subrectangulos)]

# Función para graficar la solución
def graficar_solucion(solucion, superrectangulo):
    fig, ax = plt.subplots()
    ax.set_xlim(0, superrectangulo[0])
    ax.set_ylim(0, superrectangulo[1])
    for x, y, alto, ancho in solucion:
        rect = plt.Rectangle((x, y), alto, ancho, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Función para calcular la altura mínima requerida
def altura_minima_requerida(subrectangulos):
    return max([y + alto for _, y, alto, _ in subrectangulos])

# Ejemplo de búsqueda aleatoria
mejor_solucion = None
mejor_desperdicio = float('inf')
historial_desperdicio = []

for _ in range(max_generaciones):
    altura_superrectangulo = max(1, altura_minima_requerida(mejor_solucion) if mejor_solucion else ancho_superrectangulo)
    problema = ProblemaRectangulos((ancho_superrectangulo, altura_superrectangulo), subrectangulos)
    solucion_actual = problema.generar_solucion_aleatoria()
    desperdicio_actual = problema.evaluar(solucion_actual)
    historial_desperdicio.append(desperdicio_actual)
    if desperdicio_actual < mejor_desperdicio:
        mejor_desperdicio = desperdicio_actual
        mejor_solucion = solucion_actual

# Visualizar la mejor solución encontrada
print("Mejor solución encontrada:")
print(mejor_solucion)
print("Desperdicio:", mejor_desperdicio)

graficar_solucion(mejor_solucion, (ancho_superrectangulo, altura_superrectangulo))

# Visualizar historial de desperdicio
plt.plot(historial_desperdicio)
plt.xlabel('Generación')
plt.ylabel('Desperdicio')
plt.title('Desperdicio de área a lo largo de las generaciones')
plt.show()
