import numpy as np
import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gato y Ratón")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dimensiones de la cuadrícula
grid_size = 8
cell_size = width // grid_size

# Posiciones iniciales aleatorias
gato_pos = np.array([random.randint(0, grid_size-1), random.randint(0, grid_size-1)])
raton_pos = np.array([random.randint(0, grid_size-1), random.randint(0, grid_size-1)])

# Asegurarse de que el gato y el ratón no empiecen en la misma posición
while np.array_equal(gato_pos, raton_pos):
    raton_pos = np.array([random.randint(0, grid_size-1), random.randint(0, grid_size-1)])

# Profundidad del algoritmo Minimax
profundidad = 3

# Fuente para el cronómetro
font = pygame.font.SysFont("Arial Unicode MS", 36)

def evaluar_posicion(gato, raton):
    # Calculamos la distancia de Manhattan entre el gato y el ratón
    return np.abs(gato[0] - raton[0]) + np.abs(gato[1] - raton[1])

def generar_movimientos(pos):
    movimientos = []
    # Definimos los posibles movimientos (arriba, derecha, abajo, izquierda)
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nueva_pos = pos + np.array([dx, dy])  # Calculamos la nueva posición
        # Verificamos que la nueva posición esté dentro de los límites de la cuadrícula
        if 0 <= nueva_pos[0] < grid_size and 0 <= nueva_pos[1] < grid_size:
            movimientos.append(nueva_pos)
    return movimientos

def minimax_ab(gato, raton, profundidad, es_turno_del_gato, alpha, beta):
    if profundidad == 0 or np.array_equal(gato, raton):
        return evaluar_posicion(gato, raton)

    if es_turno_del_gato:
        mejor_valor = -float('inf')
        for mov in generar_movimientos(gato):
            valor = minimax_ab(mov, raton, profundidad - 1, False, alpha, beta)
            mejor_valor = max(mejor_valor, valor)
            alpha = max(alpha, valor)
            if beta <= alpha:
                break
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for mov in generar_movimientos(raton):
            valor = minimax_ab(gato, mov, profundidad - 1, True, alpha, beta)
            mejor_valor = min(mejor_valor, valor)
            beta = min(beta, valor)
            if beta <= alpha:
                break
        return mejor_valor

def mejor_movimiento_gato(gato, raton, profundidad):
    mejor_valor = -float('inf')
    mejor_mov = gato
    for mov in generar_movimientos(gato):
        valor = minimax_ab(mov, raton, profundidad - 1, False, -float('inf'), float('inf'))
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
        valor = minimax_ab(gato, mov, profundidad - 1, True, -float('inf'), float('inf'))
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov

def mostrar_pantalla_inicio():
    screen.fill(WHITE)
    titulo = font.render("Gato y Ratón", True, BLACK)
    instrucciones = font.render("Presiona cualquier tecla para comenzar", True, BLACK)
    screen.blit(titulo, (width // 2 - titulo.get_width() // 2, height // 3))
    screen.blit(instrucciones, (width // 2 - instrucciones.get_width() // 2, height // 2))
    pygame.display.flip()
    esperar_inicio()

def esperar_inicio():
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                esperando = False

def mostrar_pantalla_fin():
    screen.fill(WHITE)
    mensaje = font.render("¡El gato atrapó al ratón!", True, BLACK)
    instrucciones = font.render("Presiona cualquier tecla para salir", True, BLACK)
    screen.blit(mensaje, (width // 2 - mensaje.get_width() // 2, height // 3))
    screen.blit(instrucciones, (width // 2 - instrucciones.get_width() // 2, height // 2))
    pygame.display.flip()
    esperar_fin()

def esperar_fin():
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                esperando = False

def main():
    mostrar_pantalla_inicio()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        for x in range(0, width, cell_size):
            for y in range(0, height, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

        gato_text = font.render("🐱", True, BLACK)
        screen.blit(gato_text, (gato_pos[0] * cell_size, gato_pos[1] * cell_size))
        raton_text = font.render("🐭", True, BLACK)
        screen.blit(raton_text, (raton_pos[0] * cell_size, raton_pos[1] * cell_size))

        if not np.array_equal(gato_pos, raton_pos):
            gato_pos[:] = mejor_movimiento_gato(gato_pos, raton_pos, profundidad)
            if np.array_equal(gato_pos, raton_pos):
                mostrar_pantalla_fin()
                break
            raton_pos[:] = mejor_movimiento_raton(raton_pos, gato_pos, profundidad)
            if np.array_equal(gato_pos, raton_pos):
                mostrar_pantalla_fin()
                break

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()