class AI:
    def __init__(self, board):
        self.board = board

    def make_turn(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board.entire_board[i][j] == self.board.EMPTY:
                    self.board.entire_board[i][j] = self.board.AI
                    return
