from tkinter import Tk, BOTH, Canvas
import time
import random


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title = "Maze Solver"
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root, width = self.width, height = self.height)
        self.canvas.configure(bg='white')
        self.canvas.pack()
        self.is_running = False


    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack()


class Cell:
    def __init__(self,
                 point1, point2, window=None,
                 has_lwall=True,
                 has_rwall=True,
                 has_twall=True,
                 has_bwall=True):
        self.has_left_wall = has_lwall
        self.has_right_wall = has_rwall
        self.has_top_wall = has_twall
        self.has_bottom_wall = has_bwall
        self._x1 = point1.x
        self._x2 = point2.x
        self._y1 = point1.y
        self._y2 = point2.y
        self._win = window
        self.visited = False

    @property
    def top_left_point(self):
        x = self._x1 if self._x1 < self._x2 else self._x2
        y = self._y1 if self._y1 < self._y2 else self._y2
        return Point(x, y)

    @property
    def bottom_right_point(self):
        x = self._x1 if self._x1 > self._x2 else self._x2
        y = self._y1 if self._y1 > self._y2 else self._y2
        return Point(x, y)

    @property
    def top_right_point(self):
        x = self._x1 if self._x1 > self._x2 else self._x2
        y = self._y1 if self._y1 < self._y2 else self._y2
        return Point(x, y)

    @property
    def bottom_left_point(self):
        x = self._x1 if self._x1 < self._x2 else self._x2
        y = self._y1 if self._y1 > self._y2 else self._y2
        return Point(x, y)

    @property
    def centre_point(self):
        x = self.bottom_left_point.x + abs(self.bottom_left_point.x - self.top_right_point.x)//2
        y = self.bottom_left_point.y - abs(self.bottom_left_point.y - self.top_right_point.y)//2
        return Point(x, y)

    def draw(self):
        b_line = Line(self.bottom_left_point, self.bottom_right_point)
        t_line = Line(self.top_left_point, self.top_right_point)
        l_line = Line(self.top_left_point, self.bottom_left_point)
        r_line = Line(self.top_right_point, self.bottom_right_point)
        if self.has_top_wall:
            t_line.draw(self._win.canvas, "black")
        else:
            t_line.draw(self._win.canvas, "white")
        if self.has_bottom_wall:
            b_line.draw(self._win.canvas, "black")
        else:
            b_line.draw(self._win.canvas, "white")
        if self.has_left_wall:
            l_line.draw(self._win.canvas, "black")
        else:
            l_line.draw(self._win.canvas, "white")
        if self.has_right_wall:
            r_line.draw(self._win.canvas, "black")
        else:
            r_line.draw(self._win.canvas, "white")


    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        p1 = self.centre_point
        p2 = to_cell.centre_point
        line = Line(p1, p2)
        line.draw(self._win.canvas, color)
    


class Maze:
    def __init__(self,
                 x1, y1, num_rows, num_cols,
                 cell_size_x, cell_size_y,
                 win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.nrows = num_rows
        self.ncols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        if seed is not None:
            random.seed(seed)
        if win is not None:
            self._break_walls_r(0,0)
            self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(
            Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y),
            Point(self.x1 + (i+1) * self.cell_size_x, self.y1 + (j+1) * self.cell_size_y),
            self._win) for i in range(self.ncols)] for j in range(self.nrows)]
        if self._win is not None:
            for i in range(self.nrows):
                for j in range(self.ncols):
                    self._draw_cell(i, j)
                    self._animate()
                
    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.nrows-1][self.ncols-1].has_bottom_wall = False
        if self._win is not None:
            self._draw_cell(0, 0)
            self._draw_cell(self.nrows-1, self.ncols-1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = [(-1,0), (1,0), (0,-1), (0,1)]
            directions = []
            for (x, y) in possible_directions:
                if i+x < 0 or i+x >= self.nrows or j+y < 0 or j+y >= self.ncols:
                    continue
                elif self._cells[i+x][j+y].visited:
                    continue
                else:
                    directions.append((i+x, j+y))
            if len(directions) == 0:
                self._draw_cell(i, j)
                return
            direction = directions[random.randint(0, len(directions)-1)]
            if direction == (i-1, j):
                self._cells[i][j].has_top_wall = False
                directions.remove((i-1, j))
                self._break_walls_r(i-1, j)
            elif direction == (i+1, j):
                self._cells[i][j].has_bottom_wall = False
                directions.remove((i+1, j))
                self._break_walls_r(i+1, j)
            elif direction == (i, j-1):
                self._cells[i][j].has_left_wall = False
                directions.remove((i, j-1))
                self._break_walls_r(i, j-1)
            elif direction == (i, j+1):
                self._cells[i][j].has_right_wall = False
                directions.remove((i, j+1))
                self._break_walls_r(i, j+1)

    def _reset_cells_visited(self):
        for x in range(self.nrows):
            for y in range(self.ncols):
                self._cells[x][y].visited = False
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.nrows-1 and j == self.ncols-1:
            return True
        current = self._cells[i][j]
        if i-1 >= 0 and not (current.has_top_wall or self._cells[i-1][j].visited):
            current.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            current.draw_move(self._cells[i-1][j], undo=True)
        if i+1 < self.nrows and not (current.has_bottom_wall or self._cells[i+1][j].visited):
            current.draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            current.draw_move(self._cells[i+1][j], undo=True)
        if j-1 >= 0 and not (current.has_left_wall or self._cells[i][j-1].visited):
            current.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            current.draw_move(self._cells[i][j-1], undo=True)
        if j+1 < self.ncols and not (current.has_right_wall or self._cells[i][j+1].visited):
            current.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            current.draw_move(self._cells[i][j+1], undo=True)
        return False

    def solve(self):
        self._solve_r(0, 0)


def main():
    win = Window(800, 600)
    maze = Maze(25, 25, 11, 15, 50, 50, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
