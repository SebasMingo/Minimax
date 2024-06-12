import tkinter as tk
import random

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.mouse_pos = self.get_random_edge_position()
        self.cat_pos = self.get_random_edge_position()

    def get_random_edge_position(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            return (0, random.randint(0, self.cols - 1))
        elif edge == "bottom":
            return (self.rows - 1, random.randint(0, self.cols - 1))
        elif edge == "left":
            return (random.randint(0, self.rows - 1), 0)
        else:  # right
            return (random.randint(0, self.rows - 1), self.cols - 1)

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

    def move_mouse(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while True:
            direction = random.choice(directions)
            new_pos = (self.mouse_pos[0] + direction[0], self.mouse_pos[1] + direction[1])
            if self.is_valid(new_pos):
                self.mouse_pos = new_pos
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
            self.cat_pos = best_move

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

class GameGUI:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.board = Board(rows, cols)
        self.cell_size = 50
        self.canvas = tk.Canvas(master, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.draw_pieces()
        self.run_game()

    def draw_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

    def draw_pieces(self):
        x0, y0 = self.board.mouse_pos[1] * self.cell_size, self.board.mouse_pos[0] * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.mouse = self.canvas.create_oval(x0, y0, x1, y1, fill="blue")
        x0, y0 = self.board.cat_pos[1] * self.cell_size, self.board.cat_pos[0] * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.cat = self.canvas.create_rectangle(x0, y0, x1, y1, fill="red")

    def update_pieces(self):
        self.canvas.delete(self.mouse)
        self.canvas.delete(self.cat)
        x0, y0 = self.board.mouse_pos[1] * self.cell_size, self.board.mouse_pos[0] * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.mouse = self.canvas.create_oval(x0, y0, x1, y1, fill="blue")
        x0, y0 = self.board.cat_pos[1] * self.cell_size, self.board.cat_pos[0] * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.cat = self.canvas.create_rectangle(x0, y0, x1, y1, fill="red")
        self.master.update()

    def run_game(self):
        while True:
            self.board.move_mouse()
            if self.board.mouse_pos == self.board.cat_pos:
                print("Cat caught the mouse!")
                break
            best_move, _ = minimax(self.board, depth=3, maximizing_player=True)
            if best_move:
                self.board.cat_pos = best_move
            else:
                print("Mouse escaped!")
                break
            self.update_pieces()
            self.master.after(500)

def main():
    root = tk.Tk()
    root.title("Gato y Ratón")
    game = GameGUI(root, rows=5, cols=5)
    root.mainloop()

if __name__ == "__main__":
    main()
    