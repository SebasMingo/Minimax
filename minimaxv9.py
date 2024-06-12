import random

# Dimensiones de la cuadrícula
grid_size = 8

# Posiciones iniciales aleatorias
gato_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
raton_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]

# Asegurarse de que el gato y el ratón no empiecen en la misma posición
while gato_pos == raton_pos:
    raton_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]

# Profundidad del algoritmo Minimax
profundidad = 3

# Contador de turnos del ratón
contador_turnos_ratón = 0

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

def imprimir_cuadricula(gato, raton):
    for i in range(grid_size):
        for j in range(grid_size):
            if [i, j] == gato:
                print("X", end=" ")
            elif [i, j] == raton:
                print("O", end=" ")
            else:
                print(".", end=" ")  # Espacio vacío
        print()  # Nueva línea al final de cada fila
    print()  # Espacio adicional al final de la matriz

def main():
    global contador_turnos_ratón
    print("¡Bienvenido a Gato y Ratón!")
    imprimir_cuadricula(gato_pos, raton_pos)
    
    while gato_pos != raton_pos:
        gato_pos[:] = mejor_movimiento_gato(gato_pos, raton_pos, profundidad)
        imprimir_cuadricula(gato_pos, raton_pos)
        if gato_pos == raton_pos:
            print("¡El gato atrapó al ratón!")
            break
        raton_pos[:] = mejor_movimiento_raton(raton_pos, gato_pos, profundidad)
        imprimir_cuadricula(gato_pos, raton_pos)
        if gato_pos == raton_pos:
            print("¡El gato atrapó al ratón!")
            break
        
        contador_turnos_ratón += 1
        if contador_turnos_ratón > 12:
            print("¡El ratón escapó por más de 12 turnos! ¡El ratón gana!")
            break

if __name__ == "__main__":
    main()