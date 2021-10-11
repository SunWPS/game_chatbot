from pathlib import Path
import pickle

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


def training_model():
    data_path = Path("prepare/data.pickle")
    model_path = Path("prepare/model")

    with open(data_path, "rb") as f:
        words, labels, training, output = pickle.load(f)

    tf.compat.v1.reset_default_graph()

    # define the keras model
    model = Sequential()
    model.add(Dense(8, activation="relu", input_shape=(len(training[0]),)))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(len(output[0]), activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(training, output, epochs=1000, batch_size=8)

    model.save(model_path)
