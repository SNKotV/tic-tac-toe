import random
from math import inf


def get_empty_cells(state):
    cells = []
    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == 0:
                cells.append((i, j))
    return cells


class AI:
    def __init__(self, board):
        self.board = board
        self.AI = -1
        self.PLAYER = 1

    def make_turn(self):
        depth = len(self.board.get_empty_cells())
        state = self.board.entire_board

        if depth == 0 or self.get_score(state) != 0:
            return

        if depth == 9:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        else:
            move = self.minimax(state, depth, self.AI)
            x, y = move[0], move[1]

        self.board.entire_board[x][y] = self.board.AI

    def minimax(self, state, depth, player):
        if player == self.AI:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]

        if depth == 0 or self.get_score(state) != 0:
            score = self.get_score(state)
            return [-1, -1, score]

        for cell in get_empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.AI:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best

    def get_score(self, state):
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [self.PLAYER, self.PLAYER, self.PLAYER] in win_state:
            return -1
        elif [self.AI, self.AI, self.AI] in win_state:
            return 1
        return 0
