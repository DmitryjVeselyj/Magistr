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
    regressor = Sequential()

    regressor.add(Input(shape=(16,)))
    regressor.add(Dense(units=128, activation='tanh'))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units=128, activation='tanh'))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units=128, activation='tanh'))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units=128))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units=1))

    regressor.compile(optimizer='adam', loss='mean_absolute_error')

    return regressor



def generate_key(initial_key, n_incorrect_elements):
    random_symbols = random.sample(string.ascii_lowercase, n_incorrect_elements)
    generated_key = copy.deepcopy(initial_key)
    for symbol in random_symbols:
        generated_key[random.randint(0, len(initial_key) - 1)] = ord(symbol)

    return generated_key


def generate_dataset(initial_key, message):
    enc_message = AES(''.join(map(chr, initial_key))).encrypt(message)
    x_train = []
    y_train = []
    orig_msg = list(map(ord, message.decode('ascii')))
    orig_msg_binary = ''.join(map(lambda x: format(x, '08b'), map(ord, message.decode('ascii'))))
    for i in range(0, 3):
        for _ in range(0, len(initial_key)):
            generated_key = ''.join(map(chr, generate_key(initial_key, i)))
            aes = AES(generated_key)
            dec_msg = aes.decrypt(enc_message)

            dec_msg_binary = ''.join(map(lambda x: format(x, '08b'), dec_msg))
            from scipy.stats import pearsonr
            x_train.append(dec_msg)
            print(sum(x == y for x, y in zip(initial_key, list(map(ord, generated_key)))) / len(initial_key))
            y_train.append(sum(x == y for x, y in zip(initial_key, list(map(ord, generated_key)))) / len(initial_key))
    return x_train, y_train


def train_model(x, y):
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    m = model()
    m.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=16, epochs=40)
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'val'], loc='upper left')
    # plt.show()

    m.save('hoba.keras')
    #
    # model = LinearRegression().fit(x_train, y_train)
    # print(model.score(x_test, y_test))
    # print(model.coef_)



x, y = [], []
for i in range(100):
    print(i)
    msg = ''.join(random.choices(['c', 'd'], k=16)).encode('ascii')
    key = list(map(ord, random.choices(['a', 'b'], k=16)))
    print(msg, key)
    new_x, new_y = generate_dataset(key, msg)
    x += new_x
    y += new_y

# x, y = generate_dataset(key)
from sklearn.linear_model import LinearRegression

train_model(np.array(x), np.array(y))
