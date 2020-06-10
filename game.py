import pygame
import random
import time
import collections
import board
from players import player, human, randomai, qlearningai


class Game:
    def __init__(self, size, player_1, player_2):
        self.size = size
        self.width = self.size * 100
        self.win = pygame.display.set_mode((self.width, self.width))
        self.board = board.Board(self.size)
        self.players = {+1: player_1, -1: player_2}
        self.current_player = random.choice([-1, 1])

    def run(self):
        run = True
        for player_index in [-1, 1]:
            self.players[player_index].reset_state()
        while run:
            self.draw()
            self.move()
            if self.is_game_over():
                self.draw()
                time.sleep(3)
                for player_index in [-1, 1]:
                    self.players[player_index].reset_state()
                self.board.clear()
        pygame.quit()
        for player_index in [-1, 1]:
            self.players[player_index].save_model()

    def train(self, iterations):
        random.seed(time.gmtime())
        results = []
        for _ in range(iterations):
            print('Iteration ' + str(_))
            results.append(self.play())
        print(collections.Counter(results))
        for player_index in [-1, 1]:
            self.players[player_index].save_model()

    def play(self):
        self.board.clear()
        for player_index in [-1, 1]:
            self.players[player_index].reset_state()
        random.choice([-1, 1])
        game_end_state = self.board.check_game_end()
        while game_end_state is None:
            self.move()
            game_end_state = self.board.check_game_end()
        for player_index in [-1, 1]:
            reward_value = 1 if player == game_end_state else -1
            self.players[player_index].reward(reward_value)
        return game_end_state

    def move(self):
        move = self.players[self.current_player].move(self.board)
        self.board.set_sign(move, self.current_player)
        self.current_player *= -1

    def draw(self):
        self.win.fill((255, 255, 255))
        self.board.draw(self.win)
        pygame.display.update()

    def is_game_over(self):
        game_end_state = self.board.check_game_end()
        if game_end_state is None:
            return False
        for player_index in [-1, 1]:
            reward_value = 1 if player == game_end_state else -1
            self.players[player_index].reward(reward_value)
        return True


if __name__ == '__main__':
    size = 4
    game = Game(size, qlearningai.QLearningAI(size, 'q_1'), human.Human(size, 100))
    game.run()
