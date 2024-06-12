import tkinter as tk
import random

# Dimensiones de la pantalla y la cuadrícula
width, height = 800, 800
grid_size = 8
cell_size = width // grid_size

# Posiciones iniciales aleatorias
gato_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
raton_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]

# Asegurarse de que el gato y el ratón no empiecen en la misma posición
while gato_pos == raton_pos:
    raton_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]

# Profundidad del algoritmo Minimax
profundidad = 3

def evaluar_posicion(gato, raton):
    # Calculamos la distancia de Manhattan entre el gato y el ratón
    return abs(gato[0] - raton[0]) + abs(gato[1] - raton[1])

def generar_movimientos(pos):
    movimientos = []
    # Definimos los posibles movimientos (arriba, derecha, abajo, izquierda)
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nueva_pos = [pos[0] + dx, pos[1] + dy]  # Calculamos la nueva posición
        # Verificamos que la nueva posición esté dentro de los límites de la cuadrícula
        if 0 <= nueva_pos[0] < grid_size and 0 <= nueva_pos[1] < grid_size:
            movimientos.append(nueva_pos)
    return movimientos

def minimax(gato, raton, profundidad, es_turno_del_gato):
    if profundidad == 0 or gato == raton:
        return evaluar_posicion(gato, raton)

    if es_turno_del_gato:
        mejor_valor = -float('inf')
        for mov in generar_movimientos(gato):
            valor = minimax(mov, raton, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for mov in generar_movimientos(raton):
            valor = minimax(gato, mov, profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def mejor_movimiento_gato(gato, raton, profundidad):
    mejor_valor = -float('inf')
    mejor_mov = gato
    for mov in generar_movimientos(gato):
        valor = minimax(mov, raton, profundidad - 1, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov

def mejor_movimiento_raton(raton, gato, profundidad):
    mejor_valor = float('inf')
    mejor_mov = raton
    posibles_movimientos = generar_movimientos(raton)
    random.shuffle(posibles_movimientos)  # Mezclamos los movimientos posibles para añadir aleatoriedad
    for mov in posibles_movimientos:
        valor = minimax(gato, mov, profundidad - 1, True)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov

class GatoRatonJuego(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gato y Ratón")
        self.geometry(f"{width}x{height}")
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.font = ("Arial Unicode MS", 36)

        self.gato_pos = gato_pos[:]
        self.raton_pos = raton_pos[:]
        
        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        self.canvas.delete("all")
        self.canvas.create_text(width // 2, height // 3, text="Gato y Ratón", font=self.font)
        self.canvas.create_text(width // 2, height // 2, text="Presiona cualquier tecla para comenzar", font=self.font)
        self.bind("<Key>", self.iniciar_juego)

    def iniciar_juego(self, event):
        self.unbind("<Key>")
        self.juego_activo = True
        self.actualizar_juego()

    def mostrar_pantalla_fin(self):
        self.canvas.delete("all")
        self.canvas.create_text(width // 2, height // 3, text="¡El gato atrapó al ratón!", font=self.font)
        self.canvas.create_text(width // 2, height // 2, text="Presiona cualquier tecla para salir", font=self.font)
        self.bind("<Key>", self.salir_juego)

    def salir_juego(self, event):
        self.quit()

    def actualizar_juego(self):
        if not self.juego_activo:
            return

        self.canvas.delete("all")
        for x in range(0, width, cell_size):
            for y in range(0, height, cell_size):
                self.canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline="black")

        self.canvas.create_text(self.gato_pos[0] * cell_size + cell_size//2, self.gato_pos[1] * cell_size + cell_size//2, text="X", font=self.font, fill="black")
        self.canvas.create_text(self.raton_pos[0] * cell_size + cell_size//2, self.raton_pos[1] * cell_size + cell_size//2, text="Y", font=self.font, fill="black")

        if self.gato_pos != self.raton_pos:
            self.gato_pos = mejor_movimiento_gato(self.gato_pos, self.raton_pos, profundidad)
            if self.gato_pos == self.raton_pos:
                self.mostrar_pantalla_fin()
                return
            self.raton_pos = mejor_movimiento_raton(self.raton_pos, self.gato_pos, profundidad)
            if self.gato_pos == self.raton_pos:
                self.mostrar_pantalla_fin()
                return

        self.after(200, self.actualizar_juego)

if __name__ == "__main__":
    juego = GatoRatonJuego()
    juego.mainloop()
