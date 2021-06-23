import sqlite3
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split

DB_FILE = '../data/uah-usd-data.db'
TEST_SIZE = 0.4
EPOCHS = 10


def main():
    exchange_rate, factors = load_data()
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(factors), np.array(exchange_rate), test_size=TEST_SIZE
    )
    model = get_model()
    model.fit(x_train, y_train, epochs=EPOCHS)
    model.evaluate(x_test,  y_test, verbose=2)


def load_data():
    exchange_rate = []
    factors = []
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    for row in cursor.execute('SELECT uah_usd, eur_usd, rub_usd, pln_usd, brent, steal, wheat, mvemsd FROM data_for_model'):
        exchange_rate.append(row[0])
        factors.append(row[1:])
    return exchange_rate, factors


def get_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(7,)),
        tf.keras.layers.Dense(8)])
    model.compile(optimizer='adam', loss='mse', metrics='mse')
    return model


if __name__ == '__main__':
    main()
