import random

class Board:
    def __init__(self, rows, cols, mouse_pos, cat_pos):
        self.rows = rows
        self.cols = cols
        self.mouse_pos = mouse_pos  # Agregar mouse_pos como atributo
        self.cat_pos = cat_pos      # Agregar cat_pos como atributo
        self.board = [['.'] * cols for _ in range(rows)]  # Inicializar el tablero con celdas vacías
        self.update_cell(mouse_pos, 'M')  # Colocar al ratón en su posición inicial
        self.update_cell(cat_pos, 'C')    # Colocar al gato en su posición inicial

    def update_cell(self, pos, symbol):
        x, y = pos
        self.board[x][y] = symbol

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

    def move_mouse(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while True:
            direction = random.choice(directions)
            new_pos = (self.mouse_pos[0] + direction[0], self.mouse_pos[1] + direction[1])
            if self.is_valid(new_pos):
                self.update_cell(self.mouse_pos, '.')  # Limpiar la celda anterior del ratón
                self.mouse_pos = new_pos
                self.update_cell(self.mouse_pos, 'M')  # Actualizar la nueva posición del ratón
                break

    def move_cat(self):
        min_dist = float('inf')
        best_move = None
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_pos = (self.cat_pos[0] + dx, self.cat_pos[1] + dy)
                if self.is_valid(new_pos):
                    dist = abs(new_pos[0] - self.mouse_pos[0]) + abs(new_pos[1] - self.mouse_pos[1])
                    if dist < min_dist:
                        min_dist = dist
                        best_move = new_pos
        if best_move:
            self.update_cell(self.cat_pos, '.')  # Limpiar la celda anterior del gato
            self.cat_pos = best_move
            self.update_cell(self.cat_pos, 'C')  # Actualizar la nueva posición del gato

def minimax(board, depth, maximizing_player):
    if depth == 0:
        return None, evaluate(board)
    
    if maximizing_player:
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
    else:
        min_eval = float('inf')
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_pos = (board.cat_pos[0] + dx, board.cat_pos[1] + dy)
                if board.is_valid(new_pos):
                    board.cat_pos = new_pos
                    _, eval = minimax(board, depth - 1, True)
                    board.cat_pos = (board.cat_pos[0] - dx, board.cat_pos[1] - dy)  # Undo move
                    if eval < min_eval:
                        min_eval = eval
        return None, min_eval

def evaluate(board):
    return -(abs(board.cat_pos[0] - board.mouse_pos[0]) + abs(board.cat_pos[1] - board.mouse_pos[1]))

def main():
    rows = 5
    cols = 5
    mouse_pos = (0, 0)
    cat_pos = (4, 4)
    board = Board(rows, cols, mouse_pos, cat_pos)

    while True:
        # Imprimir el tablero
        for row in board.board:
            print(" ".join(row))

        board.move_mouse()
        if board.mouse_pos == board.cat_pos:
            print("Cat caught the mouse!")
            break

        best_move, _ = minimax(board, depth=3, maximizing_player=True)
        if best_move:
            board.move_cat()
        else:
            print("Mouse escaped!")
            break

if __name__ == "__main__":
    main()