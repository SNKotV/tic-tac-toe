import pygame
import sys
from players import player


class Human(player.Player):
    def __init__(self, size, width):
        self.size = size
        self.width = width

    def move(self, board):
        turn = True
        while turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    move = self.get_indices(pos)
                    for indices in board.get_empty_cells():
                        if move == tuple(indices):
                            turn = False
        return move

    def get_indices(self, pos):
        return pos[1] // self.width, pos[0] // self.width
