import random

class Board:
    def __init__(self, rows, cols, mouse_pos, cat_pos):
        self.rows = rows
        self.cols = cols
        self.mouse_pos = mouse_pos
        self.cat_pos = cat_pos
        self.board = [['.'] * cols for _ in range(rows)]  # Inicializar el tablero con celdas vacías
        self.update_cell(mouse_pos, 'M')  # Colocar al ratón en su posición inicial
        self.update_cell(cat_pos, 'C')    # Colocar al gato en su posición inicial
        self.turns = 0

    def update_cell(self, pos, symbol):
        x, y = pos
        self.board[x][y] = symbol

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

    def move_mouse(self):
        best_move, _ = minimax(self, depth=3, maximizing_player=True)
        if best_move:
            self.update_cell(self.mouse_pos, '.')  # Limpiar la celda anterior del ratón
            self.mouse_pos = best_move
            self.update_cell(self.mouse_pos, 'M')  # Actualizar la nueva posición del ratón

    def move_cat(self):
        best_move, _ = minimax(self, depth=3, maximizing_player=False)
        if best_move:
            self.update_cell(self.cat_pos, '.')  # Limpiar la celda anterior del gato
            self.cat_pos = best_move
            self.update_cell(self.cat_pos, 'C')  # Actualizar la nueva posición del gato

def minimax(board, depth, maximizing_player):
    if depth == 0:
        return None, evaluate(board)
    
    if maximizing_player:  # Ratón maximiza
        max_eval = float('-inf')
        best_move = None
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_pos = (board.mouse_pos[0] + dx, board.mouse_pos[1] + dy)
                if board.is_valid(new_pos):
                    board.mouse_pos = new_pos
                    _, eval = minimax(board, depth - 1, False)
                    board.mouse_pos = (board.mouse_pos[0] - dx, board.mouse_pos[1] - dy)  # Undo move
                    if eval > max_eval:
                        max_eval = eval
                        best_move = new_pos
        return best_move, max_eval
    else:  # Gato minimiza
        min_eval = float('inf')
        best_move = None
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_pos = (board.cat_pos[0] + dx, board.cat_pos[1] + dy)
                if board.is_valid(new_pos):
                    board.cat_pos = new_pos
                    _, eval = minimax(board, depth - 1, True)
                    board.cat_pos = (board.cat_pos[0] - dx, board.cat_pos[1] - dy)  # Undo move
                    if eval < min_eval:
                        min_eval = eval
                        best_move = new_pos
        return best_move, min_eval

def evaluate(board):
    # Distancia Manhattan entre ratón y gato
    return abs(board.cat_pos[0] - board.mouse_pos[0]) + abs(board.cat_pos[1] - board.mouse_pos[1])

def main():
    rows = 8
    cols = 8
    mouse_pos = (0, 0)
    cat_pos = (7, 7)
    board = Board(rows, cols, mouse_pos, cat_pos)

    while True:
        # Imprimir el tablero
        for row in board.board:
            print(" ".join(row))
        print()  # Agregar una línea en blanco entre tableros

        if board.turns >= 15:
            print("Rat wins! Escaped from the cat for 15 turns!")
            break

        board.move_mouse()
        if board.mouse_pos == board.cat_pos:
            print("Cat caught the mouse! Cat wins!")
            break

        if board.turns >= 15:
            print("Cat wins! Caught the rat before 15 turns!")
            break

        board.move_cat()
        board.turns += 1

if __name__ == "__main__":
    main()