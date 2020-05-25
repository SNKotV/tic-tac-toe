import pygame
import os
import board
import ai
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
        self.ai = ai.AI(self.board)

    def run(self):
        pygame.init()
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
                    if event.type == pygame.KEYDOWN:
                        pressed_keys = pygame.key.get_pressed()
                        if pressed_keys[pygame.K_LALT] and pressed_keys[pygame.K_F4]:
                            run = False
                            self.turn = 0

            self.ai.make_turn()
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
        sign_size = int(self.size / 3 - self.size / 60)
        cross = pygame.transform.scale(
            pygame.image.load(os.path.join('imgs', 'cross.png')),
            (sign_size, sign_size))
        nought = pygame.transform.scale(
            pygame.image.load(os.path.join('imgs', 'nought.png')),
            (sign_size, sign_size))

        top = self.size // 4
        text_font = pygame.font.SysFont('Arial', 32)
        label = text_font.render('Choose your sign', True, (0, 0, 0))
        label_width, label_height = text_font.size('Choose your sign')
        cross_rect = [(10, top + label_height),
                      (10 + sign_size, 10 + sign_size)]
        nought_rect = [(self.size - 20 - sign_size, top + label_height),
                       (10 + sign_size, 10 + sign_size)]
        chosen = False
        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if cross_rect[0][0] <= pos[0] <= cross_rect[0][0] + cross_rect[1][0] and \
                            cross_rect[0][1] <= pos[1] <= cross_rect[0][1] + cross_rect[1][1]:
                        self.board.set_player_sign(cross)
                        self.board.set_ai_sign(nought)
                        chosen = True
                    elif nought_rect[0][0] <= pos[0] <= nought_rect[0][0] + nought_rect[1][0] and \
                            nought_rect[0][1] <= pos[1] <= nought_rect[0][1] + nought_rect[1][1]:
                        self.board.set_player_sign(nought)
                        self.board.set_ai_sign(cross)
                        chosen = True
                        
            pygame.draw.rect(self.win, (255, 255, 255), pygame.Rect(0, top, self.size, self.size // 2))
            self.win.blit(label, (self.size // 2 - label_width // 2, top))
            pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect(cross_rect[0], cross_rect[1]))
            self.win.blit(cross, (cross_rect[0][0] + 5, cross_rect[0][1] + 5))
            pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect(nought_rect[0], nought_rect[1]))
            self.win.blit(nought, (nought_rect[0][0] + 5, nought_rect[0][1] + 5))
            pygame.display.update()

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
        elif len(self.board.get_empty_cells()) == 0:
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
