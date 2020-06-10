import tensorflow as tf
import numpy as np
from players import player


class QLearningAI(player.Player):
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.training = True
        self.model = self.create_model()
        # self.model = self.load_model()
        self.model.compile(optimizer='sgd', loss='mean_squared_error')

    def create_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(self.size ** 4, input_shape=(self.size ** 2, ), activation='relu',
                                        kernel_initializer=tf.keras.initializers.zeros()))
        model.add(tf.keras.layers.Dense(self.size ** 4))
        model.add(tf.keras.layers.Dense(self.size ** 2))
        return model

    def load_model(self):
        json_file = open(self.name + 'model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = tf.keras.models.model_from_json(loaded_model_json)
        model.load_weights(self.name + 'model.h5')
        return model

    def save_model(self):
        model_json = self.model.to_json()
        with open(self.name + 'model.json', 'w') as json_file:
            json_file.write(model_json)
        self.model.save_weights(self.name + 'model.h5')

    def reset_state(self):
        self.last_move = None
        self.board_history = []
        self.q_history = []

    def predict_q(self, board):
        return self.model.predict(
            np.array([board.ravel()])).reshape(self.size, self.size)

    def fit_q(self, board, q_values):
        self.model.fit(
            np.array([board.ravel()]), np.array([q_values.ravel()]), verbose=1)

    def move(self, board):
        board = board.board
        q_values = self.predict_q(board)
        temp_q = q_values.copy()
        temp_q[board != 0] = temp_q.min() - 1
        move = np.unravel_index(np.argmax(temp_q), board.shape)
        value = temp_q.max()
        if self.training and self.last_move is not None:
            self.reward(value)
        self.board_history.append(board.copy())
        self.q_history.append(q_values)
        self.last_move = move
        return move

    def reward(self, reward_value):
        if not self.training:
            return
        new_q = self.q_history[-1].copy()
        new_q[self.last_move] = reward_value
        self.fit_q(self.board_history[-1], new_q)
