import numpy as np
import pygame
import os


class Board:
    def __init__(self, size):
        self.size = size
        self.board = np.zeros(shape=(self.size, self.size))
        self.width = 100
        self.first_player_sign = None
        self.second_player_sign = None
        self.set_players_signs(pygame.image.load(os.path.join('imgs', 'cross.png')),
                               pygame.image.load(os.path.join('imgs', 'nought.png')))

    def set_players_signs(self, first_sign, second_sign):
        size = int(self.width - self.width / 10)
        self.first_player_sign = pygame.transform.scale(first_sign, (size, size))
        self.second_player_sign = pygame.transform.scale(second_sign, (size, size))

    def clear(self):
        self.board = np.zeros(shape=(self.size, self.size))

    def get_empty_cells(self):
        return np.argwhere(self.board == 0)

    def set_sign(self, position, player_sign):
        self.board[tuple(position)] = player_sign

    def check_game_end(self):
        best = max(list(self.board.sum(axis=0)) +  # columns
                   list(self.board.sum(axis=1)) +  # rows
                   [self.board.trace()] +  # main diagonal
                   [np.fliplr(self.board).trace()],  # other diagonal
                   key=abs)
        if abs(best) == self.board.shape[0]:  # assumes square self.board
            return np.sign(best)  # winning player, +1 or -1
        if self.get_empty_cells().size == 0:
            return 0

    def draw(self, win):
        for i in range(1, self.size):
            pygame.draw.line(win, (0, 0, 0), (0, self.width * i), (self.size * self.width, self.width * i), 2)
            pygame.draw.line(win, (0, 0, 0), (self.width * i, 0), (self.width * i, self.size * self.width), 2)
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[i][j] == -1:
                    win.blit(self.first_player_sign, self.get_pos(i, j))
                elif self.board[i][j] == 1:
                    win.blit(self.second_player_sign, self.get_pos(i, j))

    def get_pos(self, i, j):
        return self.width * j + self.width / 20, self.width * i + self.width / 20
