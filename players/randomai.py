from players import player
import random


class RandomAI(player.Player):
    def __init__(self):
        # random.seed(seed)
        pass

    def move(self, board):
        return random.choice(board.get_empty_cells())
