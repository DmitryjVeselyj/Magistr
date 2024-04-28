from src.cryptography_algorithms import AES
from sklearn.model_selection import train_test_split
import copy
import random
import string
import numpy as np
from matplotlib import pyplot as plt
from keras.src.models import Sequential
from keras.src.layers import Dense, Input
from keras.src.layers import SimpleRNN
from keras.src.layers import Dropout
import itertools
from difflib import SequenceMatcher


def model():
    # Initialize RNN:
    regressor = Sequential()

    # Adding the first RNN layer and some Dropout regularization
    regressor.add(Input(shape=(16, )))
    regressor.add(Dense(units=128, activation='tanh'))
    regressor.add(Dropout(0.2))

    # Adding the second RNN layer and some Dropout regularization
    regressor.add(Dense(units=128, activation='tanh'))
    regressor.add(Dropout(0.2))

    # Adding the third RNN layer and some Dropout regularization
    regressor.add(Dense(units=128, activation='tanh' ))
    regressor.add(Dropout(0.2))

    # Adding the fourth RNN layer and some Dropout regularization
    regressor.add(Dense(units=128))
    regressor.add(Dropout(0.2))

    # Adding the output layer
    regressor.add(Dense(units=1))

    # Compile the RNN
    regressor.compile(optimizer='adam', loss='mean_absolute_error')

    return regressor


message = b'hoba' * 4
key = [ord('a'), ord('b')] * 8
enc_message = AES(''.join(map(chr, key))).encrypt(message)

def generate_key(initial_key, n_incorrect_elements):
    random_symbols = random.sample(string.ascii_lowercase, n_incorrect_elements)
    generated_key = copy.deepcopy(initial_key)
    for symbol in random_symbols:
        generated_key[random.randint(0, len(initial_key) - 1)] = ord(symbol)

    return generated_key


def generate_dataset(initial_key):
    x_train = []
    y_train = []
    orig_msg_binary = ''.join(map(lambda x: format(x, '08b'), map(ord, message.decode('ascii'))))
    for i in range(0, len(initial_key)):
        for _ in range(1000):
            generated_key = ''.join(map(chr, generate_key(initial_key, i)))
            aes = AES(generated_key)
            dec_msg = aes.decrypt(enc_message)

            dec_msg_binary =''.join(map(lambda x: format(x, '08b'), dec_msg))
            x_train.append(dec_msg)
            y_train.append(SequenceMatcher(None, orig_msg_binary, dec_msg_binary).ratio())

    return np.array(x_train), np.array(y_train)


def train_model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    print(x_train)
    print(y_train)
    m = model()
    m.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=32, epochs=40)

    m.save('hoba.keras')


x, y = generate_dataset(key)
train_model(x, y)
