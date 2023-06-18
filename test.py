import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        '''
        self.assertEqual(
                len(m1._cells),
                num_cols,
        )
        self.assertEqual(len(m1._cells[0]),
                         num_rows,
        )
        '''
        v = True
        for i in range(m1.nrows):
            for j in range(m1.ncols):
                v = v and not m1._cells[i][j].visited

#    def test_maze_break_entrance_exit(self):
        self.assertEqual(m1._cells[0][0].has_top_wall,
                         False
        )
        self.assertEqual(m1._cells[m1.nrows-1][m1.ncols-1].has_bottom_wall,
                         False
        )


if __name__ == "__main__":
    unittest.main()
