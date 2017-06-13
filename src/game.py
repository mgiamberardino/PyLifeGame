import tkinter as tk
from board import Board
from threading import Thread
import time

def print_board(board):
    for r in board:
        print(r)


class LifeGame(tk.Frame):

    def __init__(self, board, cell_size=20):
        super(LifeGame, self).__init__(tk.Tk())
        self.master.title('Juego de la vida')
        self.grid()
        self.board = board
        self.cell_size = cell_size
        self.create_widgets()
        self.draw_grid()
        self.cells_alive = {}
        self.create_events()
        self.running = False
        self.speed = 1
        self.mainloop()

    def create_widgets(self):
        width, height = self.board.size()
        kwargs = {
                  'width':  width * self.cell_size,
                  'height': height * self.cell_size,
                  'bg':     'white'
                }
        self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.grid()

    def draw_grid(self):
        self.draw_vertical_lines()
        self.draw_horizontal_lines()

    def draw_vertical_lines(self, color='gray'):
        width, height = self.board.size()
        for i in range(width - 1):
            x = (self.cell_size * i) +self.cell_size
            y0 = 0
            y1 = self.cell_size * height
            self.canvas.create_line(x,y0,x,y1, fill=color)

    def draw_horizontal_lines(self, color='gray'):
        width, height = self.board.size()
        for i in range(height - 1):
            y = (self.cell_size * i) +self.cell_size
            x0 = 0
            x1 = self.cell_size * width
            self.canvas.create_line(x0,y,x1,y, fill=color)

    def draw_cell(self, x, y, color='black'):
        x0 = x * self.cell_size
        y0 = y * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        args = (x0, y0, x1, y1)
        _id = self.canvas.create_rectangle(*args, width=0, fill=color)
        self.cells_alive[(x, y)] = _id
        self.board.set_alive(x, y)

    def del_cell(self, x, y):
        self.canvas.delete(self.cells_alive[(x,y)])
        del self.cells_alive[(x,y)]
        self.board.set_dead(x,y)

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if (x,y) in self.cells_alive:
            self.del_cell(x, y)
        else:
            self.draw_cell(x, y)

    def create_events(self):
        self.canvas.bind_all('<Button 1>', self.toggle_cell)
        self.canvas.bind_all('<space>', self.toggle_run)
        self.canvas.bind_all('a', self._accelerate)
        self.canvas.bind_all('z', self._deaccelerate)

    def _accelerate(self, event):
        self.speed += 1

    def _deaccelerate(self, event):
        self.speed = self.speed -1 if self.speed > 1 else 1

    def draw(self):
        self.clear()
        for cell_pos in self.board.get_cells_alive():
            self.draw_cell(*cell_pos)

    def clear(self):
        for _id in self.cells_alive.values():
            self.canvas.delete(_id)
        self.cells_alive = {}

    def toggle_run(self, event):
        if self.running:
            self.running = False
        else:
            self.running = True
            Thread(target=self.tick).start()

    def tick(self):
        while self.running:
            self.board.tick()
            self.draw()
            time.sleep(1/self.speed)

if __name__ == '__main__':
    import sys
    args = map(lambda x: x.split(','),sys.argv[1:])
    print(*args)
    b = Board(80, 50, (2,3), (3,6))
    l = LifeGame(b, cell_size=15)
