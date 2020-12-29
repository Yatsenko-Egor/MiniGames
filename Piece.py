class Piece:
    def __init__(self, shape, row, column):
        self.shape = shape
        self.row = row
        self.column = column
        self.rotate_state = 0
        self.size = len(self.shape[self.rotate_state])

    def get_shape(self):
        return self.shape[self.rotate_state]

    def rotate(self):
        next_state = self.rotate_state + 1
        rotate_count = len(self.shape)
        if next_state >= rotate_count:
            next_state = 0
        self.rotate_state = next_state

    def rotate_prev(self):
        next_state = self.rotate_state - 1
        rotate_count = len(self.shape)
        if next_state < 0:
            next_state = rotate_count - 1
        self.rotate_state = next_state

    def down(self):
        self.row += 1

    def up(self):
        self.row -= 1

    def left(self):
        self.column -= 1

    def right(self):
        self.column += 1
