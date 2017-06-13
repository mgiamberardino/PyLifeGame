class Board():

    ALIVE = 1
    DEAD = 0

    def __init__(self, width=8, height=8, stay=(2,3), born=(3,)):
        self._width = width
        self._height = height
        self._stay=stay
        self._born=born
        self.set_board(self.get_empty_board_list())

    def get_empty_board_list(self):
        return [[self.DEAD] * self._width for _ in range(self._height)]

    def set_board(self, board):
        self._board = board;
        self._width = len(board[0])
        self._height = len(board)

    def get(self):
        return self._board

    def size(self):
        return (self._width, self._height)

    def count_neighbors_alive(self, x, y):
        x_left = x - 1 if x > 0 else self._width-1
        x_right = x + 1 if x < self._width-1 else 0
        y_up = y - 1 if y > 0 else self._height-1
        y_down = y + 1 if y < self._height-1 else 0

        return (
                self._board[y_up][x_left],
                self._board[y_up][x],
                self._board[y_up][x_right],
                self._board[y][x_left],
                self._board[y][x_right],
                self._board[y_down][x_left],
                self._board[y_down][x],
                self._board[y_down][x_right]
                ).count(self.ALIVE)

    def calculate_state(self, state, neighbors_alive):
        if ((state == self.ALIVE and neighbors_alive in self._stay) or
            (state == self.DEAD and neighbors_alive in self._born)):
            return self.ALIVE
        else:
            return self.DEAD

    def tick(self):
        board_ = self.get_empty_board_list()
        for i in range(self._width):
            for j in range(self._height):
                args = (self._board[j][i], self.count_neighbors_alive(i,j))
                board_[j][i]=self.calculate_state(*args)
        self.set_board(board_)

    def set_alive(self, x, y):
        self._board[y][x] = self.ALIVE

    def set_dead(self, x, y):
        self._board[y][x] = self.DEAD

    def get_cells_alive(self):
        cells = []
        for i in range(self._width):
            for j in range(self._height):
                if self._board[j][i] == self.ALIVE:
                    cells.append((i,j))
        return cells


