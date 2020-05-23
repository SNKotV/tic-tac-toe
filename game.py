import pygame
import os
import board
import random
import time


def wait_key_pressed():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return


class Game:
    def __init__(self):
        self.size = 300
        self.win = pygame.display.set_mode((self.size, self.size))
        self.board = board.Board(self.size / 3)
        random.seed(time.gmtime())
        self.turn = random.randint(0, 1)
        self.ai = None

    def run(self):
        self.choose_sign()
        self.draw()
        run = True
        while run:
            while self.turn == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        self.turn = 0
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.board.set_sign(pos[0], pos[1]):
                            self.turn = 0

            print("AI turn")
            self.turn = 1
            self.draw()
            if self.is_game_over():
                run = False

        pygame.quit()

    def draw(self):
        self.win.fill((255, 255, 255))
        self.board.draw(self.win)
        pygame.display.update()

    def choose_sign(self):
        sign = pygame.image.load(os.path.join('imgs', 'cross.png'))
        self.board.set_player_sign(sign)
        sign = pygame.image.load(os.path.join('imgs', 'nought.png'))
        self.board.set_ai_sign(sign)

    def is_game_over(self):
        winner = self.board.winner()
        if winner == self.board.PLAYER:
            self.draw_game_message('win.png')
            wait_key_pressed()
            return True
        elif winner == self.board.AI:
            self.draw_game_message('lose.png')
            wait_key_pressed()
            return True
        elif self.board.is_draw():
            self.draw_game_message('draw.png')
            wait_key_pressed()
            return True

    def draw_game_message(self, message_file_name):
        pos = (0, self.size // 4)
        message = pygame.image.load(os.path.join('imgs', message_file_name))
        message = pygame.transform.scale(message, (self.size, self.size // 2))
        self.win.blit(message, pos)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()