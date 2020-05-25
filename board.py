import pygame


class Board:
    def __init__(self, size):
        self.size = int(size)
        self.player_sign = None
        self.ai_sign = None
        self.entire_board = [[0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0]]
        self.EMPTY = 0
        self.PLAYER = 1
        self.AI = -1

    def set_player_sign(self, sign):
        size = int(self.size - self.size / 10)
        self.player_sign = pygame.transform.scale(sign, (size, size))

    def set_ai_sign(self, sign):
        size = int(self.size - self.size / 10)
        self.ai_sign = pygame.transform.scale(sign, (size, size))

    def draw(self, win):
        for i in range(1, 3):
            pygame.draw.line(win, (0, 0, 0), (0, self.size * i), (self.size * 3, self.size * i), 2)
            pygame.draw.line(win, (0, 0, 0), (self.size * i, 0), (self.size * i, self.size * 3), 2)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.entire_board[i][j] == self.PLAYER:
                    win.blit(self.player_sign, self.get_pos(i, j))
                elif self.entire_board[i][j] == self.AI:
                    win.blit(self.ai_sign, self.get_pos(i, j))

    def set_sign(self, x, y):
        i, j = self.get_indices(x, y)
        if self.entire_board[i][j] == self.EMPTY:
            self.entire_board[i][j] = self.PLAYER
            return True
        return False
    
    def winner(self):
        win_state = [
            [self.entire_board[0][0], self.entire_board[0][1], self.entire_board[0][2]],
            [self.entire_board[1][0], self.entire_board[1][1], self.entire_board[1][2]],
            [self.entire_board[2][0], self.entire_board[2][1], self.entire_board[2][2]],
            [self.entire_board[0][0], self.entire_board[1][0], self.entire_board[2][0]],
            [self.entire_board[0][1], self.entire_board[1][1], self.entire_board[2][1]],
            [self.entire_board[0][2], self.entire_board[1][2], self.entire_board[2][2]],
            [self.entire_board[0][0], self.entire_board[1][1], self.entire_board[2][2]],
            [self.entire_board[2][0], self.entire_board[1][1], self.entire_board[0][2]],
        ]
        if [self.PLAYER, self.PLAYER, self.PLAYER] in win_state:
            return self.PLAYER
        elif [self.AI, self.AI, self.AI] in win_state:
            return self.AI
        return None

    def get_empty_cells_number(self):
        count = 0
        for i in range(0, 3):
            for j in range(0,3):
                if self.entire_board[i][j] == self.EMPTY:
                    count += 1
        return count

    def get_pos(self, i, j):
        return self.size * i + self.size / 20, self.size * j + self.size / 20

    def get_indices(self, x, y):
        return x // self.size, y // self.size
